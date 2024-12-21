// ChatInterface.jsx
import React, { useState, useRef, useEffect } from 'react';
import { Container, Navbar, Form, Button, InputGroup } from 'react-bootstrap';
import { Upload } from 'lucide-react';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [currentDocument, setCurrentDocument] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const messageEndRef = useRef(null);

  const scrollToBottom = () => {
    messageEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/documents/upload', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }
      
      const data = await response.json();
      setCurrentDocument(data);
      setMessages(prev => [...prev, {
        type: 'system',
        content: `Successfully uploaded ${file.name}`
      }]);
    } catch (error) {
      console.error('Error uploading file:', error);
      setMessages(prev => [...prev, {
        type: 'system',
        content: `Error uploading file: ${error.message}`
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || !currentDocument) return;

    const userMessage = {
      type: 'user',
      content: inputMessage
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/qa/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: inputMessage,
          file_id: currentDocument.file_id
        }),
      });

      if (!response.ok) {
        throw new Error(`Request failed: ${response.statusText}`);
      }

      const data = await response.json();
      setMessages(prev => [...prev, {
        type: 'ai',
        content: data.answer
      }]);
    } catch (error) {
      console.error('Error getting response:', error);
      setMessages(prev => [...prev, {
        type: 'system',
        content: `Error: ${error.message}`
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="d-flex flex-column vh-100">
      <Navbar bg="light" className="border-bottom">
        <Container fluid className="d-flex justify-content-between align-items-center">
          <Navbar.Brand>
            <img src="/ai-planet-logo.png" alt="AI Planet Logo" height="30" />
            <Navbar.Brand href="#home">planet</Navbar.Brand>          </Navbar.Brand>
            <div className="d-flex align-items-center">
              <span className={`me-2 ${currentDocument ? 'text-success' : 'text-secondary'}`}>
                {currentDocument ? 'Uploaded' : 'No file selected'}
              </span>
              <Form.Label className="mb-0 cursor-pointer" style={{ cursor: 'pointer' }}>
                <Upload className={`${isLoading ? 'text-secondary' : 'text-primary'}`} size={24} />
                <Form.Control
                  type="file"
                  accept=".pdf"
                  onChange={handleFileUpload}
                  className="d-none"
                  disabled={isLoading}
                />
              </Form.Label>
            </div>
        </Container>
      </Navbar>

      <Container fluid className="flex-grow-1 overflow-auto p-3">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`d-flex align-items-start mb-3 ${
              message.type === 'user' ? 'justify-content-end' : 'justify-content-start'
            }`}
          >
            {message.type === 'ai' && (
              <div className="rounded-circle bg-success text-white p-2 me-2 d-flex align-items-center justify-content-center" 
                style={{ width: '40px', height: '40px', minWidth: '40px' }}>
                AI
              </div>
            )}
            <div
              className={`p-3 rounded-3 ${
                message.type === 'user'
                  ? 'bg-primary text-white'
                  : message.type === 'system'
                  ? 'bg-light text-secondary'
                  : 'bg-light'
              }`}
              style={{ maxWidth: '70%', wordBreak: 'break-word' }}
            >
              {message.content}
            </div>
            {message.type === 'user' && (
              <div className="rounded-circle bg-primary text-white p-2 ms-2 d-flex align-items-center justify-content-center" 
                style={{ width: '40px', height: '40px', minWidth: '40px' }}>
                U
              </div>
            )}
          </div>
        ))}
        <div ref={messageEndRef} />
      </Container>

      <Container fluid className="p-3 border-top">
        <Form onSubmit={handleSubmit}>
          <InputGroup>
            <Form.Control
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder={currentDocument ? "Send a message..." : "Upload a document to start chatting"}
              disabled={!currentDocument || isLoading}
            />
            <Button 
              type="submit" 
              variant="primary"
              disabled={!currentDocument || isLoading}
            >
              {isLoading ? 'Sending...' : 'Send'}
            </Button>
          </InputGroup>
        </Form>
      </Container>
    </div>
  );
};

export default ChatInterface;