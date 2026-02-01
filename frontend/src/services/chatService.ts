/**
 * Service for handling chat-related API calls
 */

interface ChatMessage {
  message: string;
  conversation_id?: string;
}

interface TodoTask {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: string;
  tags?: string;
  due_date?: string;
  created_at: string;
}

interface ChatResponse {
  response: string;
  conversation_id: string;
  action_performed: boolean;
  tasks?: TodoTask[];
  tool_calls?: any[];
  error?: string;
}

export class ChatService {
  private baseUrl: string;
  private token: string | null;

  constructor() {
    this.baseUrl = `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1`;  // Use same base URL as main API service, append /api/v1
    // Note: We don't rely on constructor token storage anymore, we get it fresh for each request
    this.token = typeof window !== 'undefined' ? localStorage.getItem('authToken') : null;
  }

  async sendMessage(userId: string, message: ChatMessage): Promise<ChatResponse> {
    try {
      // Get token fresh for each request - use the correct key from apiService
      const token = typeof window !== 'undefined' ? localStorage.getItem('authToken') : null;

      // Log token for debugging
      console.log('ChatService token:', token);

      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      // Only add Authorization header if token exists
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${this.baseUrl}/chat/send`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
          message: message.message,
          conversation_id: message.conversation_id || null
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();
      return data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  async getConversations(userId: string): Promise<any[]> {
    try {
      const response = await fetch(`${this.baseUrl}/chat/conversations/${userId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.token}`
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data.conversations || [];
    } catch (error) {
      console.error('Error getting conversations:', error);
      throw error;
    }
  }

  async getConversationMessages(conversationId: string): Promise<any[]> {
    try {
      const response = await fetch(`${this.baseUrl}/chat/conversations/${conversationId}/messages`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.token}`
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data.messages || [];
    } catch (error) {
      console.error('Error getting conversation messages:', error);
      throw error;
    }
  }
}

// Create a singleton instance
export const chatService = new ChatService();

export default chatService;