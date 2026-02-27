
import React, { useState, useEffect } from "react";
import "./App.css";

type Tab = "upload" | "chat" | "research" | "notes";

interface Note {
  id: string;
  text: string;
  timestamp: string;
}

export default function App() {
  const [activeTab, setActiveTab] = useState<Tab>("upload");
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");

  // Chat state
  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState<Array<{ role: string; content: string }>>([]);
  const [chatLoading, setChatLoading] = useState(false);

  // Research state
  const [researchTopic, setResearchTopic] = useState("");
  const [researchResult, setResearchResult] = useState("");
  const [researchLoading, setResearchLoading] = useState(false);

  // Notes state
  const [noteText, setNoteText] = useState("");
  const [notes, setNotes] = useState<Note[]>([]);
  const [notesLoading, setNotesLoading] = useState(false);

  useEffect(() => {
    loadNotes();
  }, []);

  // File Upload Handler
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setMessage("");
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a file first.");
      return;
    }

    setIsLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/api/documents/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        setMessage("Document uploaded successfully!");
        setFile(null);
      } else {
        setMessage("Error uploading document. Please try again.");
      }
    } catch (error) {
      setMessage("Error connecting to backend. Make sure the server is running.");
    } finally {
      setIsLoading(false);
    }
  };

  // Chat Handler
  const handleChat = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    const newHistory = [...chatHistory, { role: "user", content: question }];
    setChatHistory(newHistory);
    setQuestion("");
    setChatLoading(true);
    
    // Add a loading indicator
    const historyWithLoading = [...newHistory, { role: "assistant", content: "⏳ Processing... This may take up to 30 seconds." }];
    setChatHistory(historyWithLoading);

    try {
      const response = await fetch("http://localhost:8000/api/chat/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();
      const assistantMessage = data.answer || data.response || "No response received";
      setChatHistory([...newHistory, { role: "assistant", content: assistantMessage }]);
    } catch (error) {
      setChatHistory([...newHistory, { role: "assistant", content: "❌ Error connecting to chat service. Make sure the backend is running on http://localhost:8000" }]);
    } finally {
      setChatLoading(false);
    }
  };

  // Research Handler
  const handleResearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!researchTopic.trim()) return;

    setResearchLoading(true);
    setResearchResult("");

    try {
      const response = await fetch("http://localhost:8000/api/research/topic", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: researchTopic }),
      });

      const data = await response.json();
      let result = "";
      
      if (data.result) {
        result = typeof data.result === "string" ? data.result : JSON.stringify(data.result, null, 2);
      } else if (data.research) {
        if (Array.isArray(data.research)) {
          result = data.research.map((r: any) => 
            typeof r === "string" ? r : JSON.stringify(r, null, 2)
          ).join("\n\n---\n\n");
        } else {
          result = typeof data.research === "string" ? data.research : JSON.stringify(data.research, null, 2);
        }
      } else {
        result = JSON.stringify(data, null, 2);
      }
      
      setResearchResult(result);
    } catch (error) {
      setResearchResult("Error connecting to research service. Make sure the backend is running.");
    } finally {
      setResearchLoading(false);
    }
  };

  // Notes Handlers
  const loadNotes = async () => {
    setNotesLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/notes/list");
      const data = await response.json();
      if (Array.isArray(data)) {
        setNotes(data);
      } else if (data.notes && Array.isArray(data.notes)) {
        setNotes(data.notes);
      } else {
        setNotes([]);
      }
    } catch (error) {
      console.error("Error loading notes");
      setNotes([]);
    } finally {
      setNotesLoading(false);
    }
  };

  const handleAddNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!noteText.trim()) return;

    try {
      const response = await fetch("http://localhost:8000/api/notes/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: noteText }),
      });

      if (response.ok) {
        setNoteText("");
        await loadNotes();
      }
    } catch (error) {
      console.error("Error creating note");
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🎓 Enterprise NotebookLM</h1>
        <p className="subtitle">AI-powered document research and analytics platform</p>
      </header>

      <nav className="app-nav">
        <button
          className={`nav-btn ${activeTab === "upload" ? "active" : ""}`}
          onClick={() => setActiveTab("upload")}
        >
          📄 Upload
        </button>
        <button
          className={`nav-btn ${activeTab === "chat" ? "active" : ""}`}
          onClick={() => setActiveTab("chat")}
        >
          💬 Chat
        </button>
        <button
          className={`nav-btn ${activeTab === "research" ? "active" : ""}`}
          onClick={() => setActiveTab("research")}
        >
          🔍 Research
        </button>
        <button
          className={`nav-btn ${activeTab === "notes" ? "active" : ""}`}
          onClick={() => setActiveTab("notes")}
        >
          📝 Notes
        </button>
      </nav>

      <main className="app-main">
        {/* Upload Tab */}
        {activeTab === "upload" && (
          <div className="tab-content">
            <div className="upload-section">
              <h2>📄 Upload Documents</h2>
              <form onSubmit={handleUpload} className="upload-form">
                <div className="file-input-wrapper">
                  <input
                    type="file"
                    id="file-input"
                    onChange={handleFileChange}
                    accept=".pdf,.doc,.docx,.txt"
                    className="file-input"
                  />
                  <label htmlFor="file-input" className="file-label">
                    {file ? file.name : "Choose a file (PDF, DOC, DOCX, TXT)"}
                  </label>
                </div>

                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={isLoading || !file}
                >
                  {isLoading ? "Uploading..." : "Upload Document"}
                </button>
              </form>

              {message && (
                <div className={`message ${message.includes("Error") ? "error" : "success"}`}>
                  {message}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Chat Tab */}
        {activeTab === "chat" && (
          <div className="tab-content">
            <div className="chat-section">
              <h2>💬 Interactive Chat</h2>
              <div className="chat-box">
                <div className="chat-messages">
                  {chatHistory.length === 0 ? (
                    <div className="chat-empty">
                      <p>Ask questions about your uploaded documents.</p>
                      <p>Start a conversation to get intelligent insights!</p>
                    </div>
                  ) : (
                    chatHistory.map((msg, idx) => (
                      <div key={idx} className={`chat-message ${msg.role}`}>
                        <span className="message-role">{msg.role === "user" ? "You" : "AI"}</span>
                        <p className="message-text">{msg.content}</p>
                      </div>
                    ))
                  )}
                </div>

                <form onSubmit={handleChat} className="chat-form">
                  <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask a question about your documents..."
                    disabled={chatLoading}
                    className="chat-input"
                  />
                  <button
                    type="submit"
                    disabled={chatLoading || !question.trim()}
                    className="btn btn-primary"
                  >
                    {chatLoading ? "..." : "Send"}
                  </button>
                </form>
              </div>
            </div>
          </div>
        )}

        {/* Research Tab */}
        {activeTab === "research" && (
          <div className="tab-content">
            <div className="research-section">
              <h2>🔍 Research Tools</h2>
              <form onSubmit={handleResearch} className="research-form">
                <input
                  type="text"
                  value={researchTopic}
                  onChange={(e) => setResearchTopic(e.target.value)}
                  placeholder="Enter a topic to research..."
                  disabled={researchLoading}
                  className="research-input"
                />
                <button
                  type="submit"
                  disabled={researchLoading || !researchTopic.trim()}
                  className="btn btn-primary"
                >
                  {researchLoading ? "Researching..." : "Research"}
                </button>
              </form>

              {researchResult && (
                <div className="research-result">
                  <h3>Research Results</h3>
                  <div className="result-content">{researchResult}</div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Notes Tab */}
        {activeTab === "notes" && (
          <div className="tab-content">
            <div className="notes-section">
              <h2>📝 My Notes</h2>
              <form onSubmit={handleAddNote} className="notes-form">
                <textarea
                  value={noteText}
                  onChange={(e) => setNoteText(e.target.value)}
                  placeholder="Add a new note..."
                  disabled={notesLoading}
                  className="note-input"
                  rows={4}
                />
                <button
                  type="submit"
                  disabled={notesLoading || !noteText.trim()}
                  className="btn btn-primary"
                >
                  Save Note
                </button>
              </form>

              <div className="notes-list">
                {notes.length === 0 ? (
                  <p className="no-notes">No notes yet. Create your first note above!</p>
                ) : (
                  notes.map((note) => (
                    <div key={note.id} className="note-item">
                      <p>{note.text}</p>
                      <small>{note.timestamp}</small>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>&copy; 2026 Enterprise NotebookLM. Powered by AI.</p>
      </footer>
    </div>
  );
}
