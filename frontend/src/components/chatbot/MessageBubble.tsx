import React from 'react';
import { ChatMessage } from '@/types/chat';
import { User, Bot } from 'lucide-react';

interface MessageBubbleProps {
  message: ChatMessage;
  isLast?: boolean;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  // Handle new data structure: sender_type instead of role
  const isUser = message.sender_type === 'user' || message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`flex items-start gap-3 max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser ? 'bg-blue-500' : 'bg-gray-500'
        }`}>
          {isUser ? (
            <User className="w-5 h-5 text-white" />
          ) : (
            <Bot className="w-5 h-5 text-white" />
          )}
        </div>

        {/* Message Content */}
        <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
          <div className={`px-4 py-3 rounded-2xl ${
            isUser 
              ? 'bg-blue-500 text-white rounded-br-md' 
              : 'bg-gray-100 text-gray-800 rounded-bl-md'
          }`}>
            <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">
              {message.message_text || message.response_text || message.content || ''}
            </p>
          </div>
          
          {/* Timestamp */}
          <span className={`text-xs text-gray-500 mt-1 ${
            isUser ? 'text-right' : 'text-left'
          }`}>
            {new Date(message.timestamp || message.created_at || Date.now()).toLocaleTimeString([], { 
              hour: '2-digit', 
              minute: '2-digit' 
            })}
          </span>
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;
