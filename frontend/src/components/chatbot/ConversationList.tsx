import React, { useState, useEffect } from 'react';
import { ChatSession } from '@/types/chat';
import { MessageSquare, Trash2, Plus, RefreshCw } from 'lucide-react';
import chatService from '@/services/chatService';

interface ConversationListProps {
  userId: string;
  currentSessionId: number | null;
  onSessionSelect: (sessionId: number) => void;
  onNewChat: () => void;
}

const ConversationList: React.FC<ConversationListProps> = ({
  userId,
  currentSessionId,
  onSessionSelect,
  onNewChat
}) => {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadSessions();
  }, [userId]);

  // Refresh sessions when currentSessionId changes (new chat started)
  useEffect(() => {
    if (currentSessionId === null) {
      loadSessions();
    }
  }, [currentSessionId]);

  const loadSessions = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await chatService.getChatSessions(userId);
      setSessions(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const deleteSession = async (sessionId: number) => {
    try {
      await chatService.deleteChatSession(sessionId);
      setSessions(prev => prev.filter(s => s.id !== sessionId));
      
      // If we deleted the current session, clear it
      if (currentSessionId === sessionId) {
        onNewChat();
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    return date.toLocaleDateString();
  };

  const getSessionPreview = (session: ChatSession) => {
    const lastMessage = session.messages[session.messages.length - 1];
    if (!lastMessage) return 'No messages yet';
    
    // Handle new data structure: message_text and response_text
    const content = lastMessage.message_text || lastMessage.response_text || lastMessage.content || '';
    return content.length > 50 ? `${content.substring(0, 50)}...` : content;
  };

  const getSessionTitle = (session: ChatSession) => {
    const firstMessage = session.messages[0];
    if (!firstMessage) return `Session ${session.id}`;
    
    const content = firstMessage.message_text || firstMessage.response_text || firstMessage.content || '';
    if (content.length > 30) {
      return content.substring(0, 30) + '...';
    }
    return content || `Session ${session.id}`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-32">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 text-red-500 text-sm">
        Error: {error}
        <button 
          onClick={loadSessions}
          className="ml-2 text-blue-500 hover:underline"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <button
          onClick={onNewChat}
          className="w-full flex items-center justify-center gap-2 bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors mb-2"
        >
          <Plus className="w-4 h-4" />
          New Chat
        </button>
        <button
          onClick={loadSessions}
          className="w-full flex items-center justify-center gap-2 bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors text-sm"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh History
        </button>
      </div>

      {/* Sessions List */}
      <div className="flex-1 overflow-y-auto">
        {sessions.length === 0 ? (
          <div className="p-4 text-center text-gray-500 text-sm">
            No conversations yet
          </div>
        ) : (
          <div className="p-2">
            {sessions.map((session) => (
              <div
                key={session.id}
                className={`group relative p-3 rounded-lg cursor-pointer transition-colors ${
                  currentSessionId === session.id
                    ? 'bg-blue-50 border border-blue-200'
                    : 'hover:bg-gray-50'
                }`}
                onClick={() => onSessionSelect(session.id)}
              >
                {/* Session Info */}
                <div className="flex items-start gap-3">
                  <MessageSquare className="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium text-gray-900 truncate">
                      {getSessionTitle(session)}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      {formatDate(session.updated_at)}
                    </div>
                    <div className="text-xs text-gray-600 mt-1 truncate">
                      {getSessionPreview(session)}
                    </div>
                  </div>
                </div>

                {/* Delete Button */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteSession(session.id);
                  }}
                  className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity p-1 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded"
                  title="Delete conversation"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ConversationList;
