import axios from 'axios';
import { Venue, Booking, BookingRequest } from '@/types/chat';

const API_BASE_URL = import.meta.env.VITE_BOOKING_API_URL || 'http://localhost:8000/api/booking';

const bookingService = {
  async getVenues(filters?: { min_capacity?: number; max_rate?: number }): Promise<Venue[]> {
    try {
      const params = new URLSearchParams();
      if (filters?.min_capacity) params.append('min_capacity', filters.min_capacity.toString());
      if (filters?.max_rate) params.append('max_rate', filters.max_rate.toString());

      const response = await axios.get(`${API_BASE_URL}/venues/`, { params });
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to fetch venues');
      }
      throw new Error('Network error occurred');
    }
  },

  async getVenue(venueId: number): Promise<Venue> {
    try {
      const response = await axios.get(`${API_BASE_URL}/venues/${venueId}/`);
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to fetch venue');
      }
      throw new Error('Network error occurred');
    }
  },

  async createVenue(venueData: Partial<Venue>): Promise<Venue> {
    try {
      const response = await axios.post(`${API_BASE_URL}/venues/`, venueData);
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to create venue');
      }
      throw new Error('Network error occurred');
    }
  },

  async updateVenue(venueId: number, venueData: Partial<Venue>): Promise<Venue> {
    try {
      const response = await axios.put(`${API_BASE_URL}/venues/${venueId}/`, venueData);
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to update venue');
      }
      throw new Error('Network error occurred');
    }
  },

  async deleteVenue(venueId: number): Promise<void> {
    try {
      await axios.delete(`${API_BASE_URL}/venues/${venueId}/`);
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to delete venue');
      }
      throw new Error('Network error occurred');
    }
  },

  async checkVenueAvailability(venueId: number, startTime: string, endTime: string): Promise<any> {
    try {
      const params = new URLSearchParams({
        start_time: startTime,
        end_time: endTime
      });
      const response = await axios.get(`${API_BASE_URL}/venues/${venueId}/availability/`, { params });
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to check venue availability');
      }
      throw new Error('Network error occurred');
    }
  },

  async getBookings(filters?: { user_id?: string; status?: string }): Promise<Booking[]> {
    try {
      const params = new URLSearchParams();
      if (filters?.user_id) params.append('user_id', filters.user_id);
      if (filters?.status) params.append('status', filters.status);

      const response = await axios.get(`${API_BASE_URL}/bookings/`, { params });
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to fetch bookings');
      }
      throw new Error('Network error occurred');
    }
  },

  async getBooking(bookingId: number): Promise<Booking> {
    try {
      const response = await axios.get(`${API_BASE_URL}/bookings/${bookingId}/`);
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to fetch booking');
      }
      throw new Error('Network error occurred');
    }
  },

  async createBooking(bookingData: BookingRequest): Promise<Booking> {
    try {
      const response = await axios.post(`${API_BASE_URL}/bookings/`, bookingData);
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to create booking');
      }
      throw new Error('Network error occurred');
    }
  },

  async updateBooking(bookingId: number, bookingData: Partial<Booking>): Promise<Booking> {
    try {
      const response = await axios.put(`${API_BASE_URL}/bookings/${bookingId}/`, bookingData);
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to update booking');
      }
      throw new Error('Network error occurred');
    }
  },

  async cancelBooking(bookingId: number): Promise<{ message: string }> {
    try {
      const response = await axios.delete(`${API_BASE_URL}/bookings/${bookingId}/`);
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to cancel booking');
      }
      throw new Error('Network error occurred');
    }
  },

  async getUserBookings(userId: string): Promise<Booking[]> {
    try {
      const response = await axios.get(`${API_BASE_URL}/users/${userId}/bookings/`);
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        throw new Error(error.response.data.error || 'Failed to fetch user bookings');
      }
      throw new Error('Network error occurred');
    }
  }
};

export default bookingService;