import os
from typing import List, Dict, Any
import logging
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from config import settings

logger = logging.getLogger(__name__)

class QAService:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY
        )

    async def create_vector_store(self, text_chunks: List[str], file_id: str) -> str:
        """
        Create and save a vector store for the given text chunks.
        """
        try:
            vectorstore = FAISS.from_texts(
                texts=text_chunks,
                embedding=self.embeddings
            )
            
            vector_store_path = os.path.join(settings.VECTOR_STORE_DIR, f"faiss_index_{file_id}")
            vectorstore.save_local(vector_store_path)
            return vector_store_path
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise

    async def get_qa_chain(self, vector_store_path: str):
        """
        Create a QA chain using the saved vector store.
        """
        try:
            vectorstore = FAISS.load_local(
                vector_store_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            
            llm = ChatGoogleGenerativeAI(
                model=settings.MODEL_NAME,
                google_api_key=settings.GOOGLE_API_KEY,
                temperature=0.7,
                top_k=40,
                top_p=0.95,
            )
            
            return ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=vectorstore.as_retriever(
                    search_kwargs={"k": 4}
                ),
                return_source_documents=True,
                verbose=True
            )
        except Exception as e:
            logger.error(f"Error creating QA chain: {str(e)}")
            raise

    async def get_answer(self, question: str, file_id: str, chat_history: List = None) -> Dict[str, Any]:
        """
        Get an answer for the given question using the specified vector store.
        """
        try:
            vector_store_path = os.path.join(settings.VECTOR_STORE_DIR, f"faiss_index_{file_id}")
            if not os.path.exists(vector_store_path):
                raise FileNotFoundError("Vector store not found")
            
            qa_chain = await self.get_qa_chain(vector_store_path)
            result = await qa_chain.ainvoke({
                "question": question,
                "chat_history": chat_history or []
            })
            
            return {
                "answer": result["answer"],
                "sources": [doc.page_content for doc in result.get("source_documents", [])]
            }
        except Exception as e:
            logger.error(f"Error getting answer: {str(e)}")
            raise