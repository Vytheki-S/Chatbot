import React, { useState } from 'react';
import { ChatInterface, ConversationList } from '@/components/chatbot';
import { useChat } from '@/hooks/useChat';
import { Menu, X } from 'lucide-react';

const ChatPage: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [userId] = useState('user-123'); // In a real app, this would come from auth
  
  const {
    messages,
    isLoading,
    error,
    sessionId,
    sendMessage,
    clearChat,
    loadSession
  } = useChat(userId);

  const handleNewChat = () => {
    clearChat();
    setSidebarOpen(false);
  };

  const handleSessionSelect = (sessionId: number) => {
    loadSession(sessionId);
    setSidebarOpen(false);
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 z-50 w-80 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex items-center justify-between p-4 border-b border-gray-200 lg:hidden">
          <h1 className="text-lg font-semibold text-gray-900">Chat History</h1>
          <button
            onClick={() => setSidebarOpen(false)}
            className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <ConversationList
          userId={userId}
          currentSessionId={sessionId}
          onSessionSelect={handleSessionSelect}
          onNewChat={handleNewChat}
        />
      </div>

      {/* Main chat area */}
      <div className="flex-1 flex flex-col">
        {/* Mobile header */}
        <div className="lg:hidden flex items-center justify-between p-4 border-b border-gray-200 bg-white">
          <button
            onClick={() => setSidebarOpen(true)}
            className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg"
          >
            <Menu className="w-5 h-5" />
          </button>
          <h1 className="text-lg font-semibold text-gray-900">Venue Booking Chatbot</h1>
          <div className="w-10"></div> {/* Spacer for centering */}
        </div>

        {/* Chat interface */}
        <div className="flex-1 min-h-0">
          <ChatInterface
            messages={messages}
            isLoading={isLoading}
            error={error}
            onSendMessage={sendMessage}
            onClearChat={clearChat}
          />
        </div>
      </div>
    </div>
  );
};

export default ChatPage;