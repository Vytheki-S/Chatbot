// API Configuration
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  CHATBOT_URL: import.meta.env.VITE_CHATBOT_API_URL || 'http://localhost:8000/api/chatbot',
  BOOKING_URL: import.meta.env.VITE_BOOKING_API_URL || 'http://localhost:8000/api/booking',
  TIMEOUT: 30000, // 30 seconds
};

// App Configuration
export const APP_CONFIG = {
  NAME: import.meta.env.VITE_APP_NAME || 'Venue Booking Chatbot',
  VERSION: import.meta.env.VITE_APP_VERSION || '1.0.0',
  DEBUG: import.meta.env.VITE_DEBUG === 'true',
};

// Chat Configuration
export const CHAT_CONFIG = {
  MAX_MESSAGE_LENGTH: 1000,
  TYPING_INDICATOR_DELAY: 1000,
  AUTO_SCROLL_DELAY: 100,
  MAX_SESSIONS_DISPLAY: 50,
};

// UI Configuration
export const UI_CONFIG = {
  SIDEBAR_WIDTH: 320,
  MOBILE_BREAKPOINT: 1024,
  ANIMATION_DURATION: 300,
  DEBOUNCE_DELAY: 300,
};

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error occurred. Please check your connection.',
  UNAUTHORIZED: 'You are not authorized to perform this action.',
  NOT_FOUND: 'The requested resource was not found.',
  SERVER_ERROR: 'Server error occurred. Please try again later.',
  VALIDATION_ERROR: 'Please check your input and try again.',
  TIMEOUT_ERROR: 'Request timed out. Please try again.',
};

// Success Messages
export const SUCCESS_MESSAGES = {
  MESSAGE_SENT: 'Message sent successfully.',
  SESSION_CLEARED: 'Chat session cleared.',
  SESSION_LOADED: 'Chat session loaded.',
  BOOKING_CREATED: 'Booking created successfully.',
  BOOKING_UPDATED: 'Booking updated successfully.',
  BOOKING_CANCELLED: 'Booking cancelled successfully.',
};

// Date Formats
export const DATE_FORMATS = {
  DISPLAY: 'MMM dd, yyyy',
  TIME: 'HH:mm',
  DATETIME: 'MMM dd, yyyy HH:mm',
  ISO: 'yyyy-MM-dd',
  ISO_DATETIME: "yyyy-MM-dd'T'HH:mm:ss",
};
