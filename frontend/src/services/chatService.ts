import axios from 'axios';
import { ChatRequest, ChatResponse, ChatSession } from '@/types/chat';

const API_BASE_URL = import.meta.env.VITE_CHATBOT_API_URL || 'http://localhost:8000/api/chatbot';

const chatService = {
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response = await axios.post(`${API_BASE_URL}/chat/`, request);
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to send message');
      }
      throw new Error('Network error occurred');
    }
  },

  async getChatSessions(userId: string): Promise<ChatSession[]> {
    try {
      const response = await axios.get(`${API_BASE_URL}/users/${userId}/sessions/`);
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to fetch chat sessions');
      }
      throw new Error('Network error occurred');
    }
  },

  async deleteChatSession(sessionId: number): Promise<void> {
    try {
      await axios.delete(`${API_BASE_URL}/sessions/delete/${sessionId}/`);
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to delete chat session');
      }
      throw new Error('Network error occurred');
    }
  },

  async getVenues(): Promise<any[]> {
    try {
      const response = await axios.get(`${API_BASE_URL}/venues/`);
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to fetch venues');
      }
      throw new Error('Network error occurred');
    }
  },

  async getVenueRecommendations(message: string): Promise<string> {
    try {
      const response = await axios.post(`${API_BASE_URL}/venues/recommendations/`, { message });
      return response.data.recommendations;
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to get venue recommendations');
      }
      throw new Error('Network error occurred');
    }
  },

  async healthCheck(): Promise<{ status: string }> {
    try {
      const response = await axios.get(`${API_BASE_URL}/health/`);
      return response.data;
    } catch (error: any) {
      throw new Error('Health check failed');
    }
  }
};

export default chatService;