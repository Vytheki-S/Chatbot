import { useState, useCallback, useRef } from 'react';
import { ChatMessage, ChatRequest } from '@/types/chat';
import chatService from '@/services/chatService';

interface UseChatReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  sessionId: number | null;
  sendMessage: (content: string) => Promise<void>;
  clearChat: () => void;
  loadSession: (sessionId: number) => Promise<void>;
}

export const useChat = (userId: string): UseChatReturn => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<number | null>(null);
  
  const abortControllerRef = useRef<AbortController | null>(null);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    setIsLoading(true);
    setError(null);

    // Cancel previous request if it exists
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    // Create new abort controller for this request
    abortControllerRef.current = new AbortController();

    try {
      // Add user message to UI immediately
      const userMessage: ChatMessage = {
        message_id: Date.now(), // Temporary ID
        sender_type: 'user',
        user_id: parseInt(userId),
        message_text: content.trim(),
        timestamp: new Date().toISOString(),
        resolved: false
      };

      setMessages(prev => [...prev, userMessage]);

      // Prepare request
      const request: ChatRequest = {
        message: content.trim(),
        user_id: userId,
        session_id: sessionId || undefined
      };

      // Send message to backend
      const response = await chatService.sendMessage(request);

      // Update session ID if this is a new session
      if (response.session_id && !sessionId) {
        setSessionId(response.session_id);
      }

      // Add assistant response
      const assistantMessage: ChatMessage = {
        message_id: response.message_id,
        sender_type: 'admin',
        user_id: parseInt(userId),
        message_text: '',
        response_text: response.response,
        timestamp: new Date().toISOString(),
        resolved: false
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (err: any) {
      if (err.name === 'AbortError') {
        // Request was cancelled, do nothing
        return;
      }
      
      setError(err.message || 'Failed to send message');
      
      // Remove the user message if there was an error
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  }, [userId, sessionId]);

  const clearChat = useCallback(() => {
    setMessages([]);
    setSessionId(null);
    setError(null);
    
    // Cancel any ongoing request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
  }, []);

  const loadSession = useCallback(async (sessionId: number) => {
    try {
      setIsLoading(true);
      setError(null);
      
      const sessions = await chatService.getChatSessions(userId);
      const session = sessions.find(s => s.id === sessionId);
      
      if (session) {
        setMessages(session.messages);
        setSessionId(session.id);
      } else {
        setError('Session not found');
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load session');
    } finally {
      setIsLoading(false);
    }
  }, [userId]);

  return {
    messages,
    isLoading,
    error,
    sessionId,
    sendMessage,
    clearChat,
    loadSession
  };
};
