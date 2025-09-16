export interface ChatMessage {
  message_id: number;
  sender_type: 'user' | 'admin' | 'system';
  user_id: number;
  message_text: string;
  response_text?: string;
  timestamp: string;
  booking_reference?: string;
  resolved: boolean;
  // Legacy fields for backward compatibility
  id?: number;
  role?: 'user' | 'assistant' | 'system';
  content?: string;
  created_at?: string;
}

export interface ChatSession {
  id: number;
  user_id: string;
  messages: ChatMessage[];
  created_at: string;
  updated_at: string;
}

export interface ChatRequest {
  message: string;
  user_id: string;
  session_id?: number;
}

export interface ChatResponse {
  response: string;
  session_id: number;
  message_id: number;
}

export interface Venue {
  id: number;
  name: string;
  description: string;
  capacity: number;
  hourly_rate: number;
  is_available: boolean;
}

export interface Booking {
  id: number;
  venue: Venue;
  user_id: string;
  start_time: string;
  end_time: string;
  total_cost: number;
  status: 'pending' | 'confirmed' | 'cancelled' | 'completed';
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface BookingRequest {
  venue_id: number;
  user_id: string;
  start_time: string;
  end_time: string;
  notes?: string;
}

export interface ApiError {
  error: string;
  message?: string;
}