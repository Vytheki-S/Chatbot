import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatPage from './pages/chat/ChatPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/chat" element={<ChatPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;