import axios, { AxiosError } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:4000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface User {
  _id: string;
  name: string;
  email: string;
}

export interface Course {
  _id: string;
  title: string;
  description: string;
  tags: string[];
  level: 'beginner' | 'intermediate' | 'advanced';
  durationMinutes?: number;
  prerequisites?: string[];
  createdAt: string;
}

export interface Interaction {
  _id: string;
  user: string;
  course: string | Course;
  action: 'view' | 'enroll' | 'complete';
  metadata?: Record<string, unknown>;
  createdAt: string;
}

export interface AuthResponse {
  token: string;
}

export interface RecommendationsResponse {
  recommendations: Course[];
}

export const authApi = {
  signup: async (name: string, email: string, password: string): Promise<AuthResponse> => {
    const { data } = await api.post<AuthResponse>('/api/auth/signup', { name, email, password });
    return data;
  },
  login: async (email: string, password: string): Promise<AuthResponse> => {
    const { data } = await api.post<AuthResponse>('/api/auth/login', { email, password });
    return data;
  },
  getMe: async (): Promise<User> => {
    const { data } = await api.get<User>('/api/auth/me');
    return data;
  },
};

export const coursesApi = {
  list: async (params?: { tag?: string; level?: string; q?: string }): Promise<Course[]> => {
    const { data } = await api.get<Course[]>('/api/courses', { params });
    return data;
  },
  get: async (id: string): Promise<Course> => {
    const { data } = await api.get<Course>(`/api/courses/${id}`);
    return data;
  },
  create: async (course: Partial<Course>): Promise<Course> => {
    const { data } = await api.post<Course>('/api/courses', course);
    return data;
  },
};

export const interactionsApi = {
  record: async (
    course: string,
    action: 'view' | 'enroll' | 'complete',
    metadata?: Record<string, unknown>
  ): Promise<Interaction> => {
    const { data } = await api.post<Interaction>('/api/interactions/record', {
      course,
      action,
      metadata,
    });
    return data;
  },
  getMyInteractions: async (): Promise<Interaction[]> => {
    const { data } = await api.get<Interaction[]>('/api/interactions/me');
    return data;
  },
};

export const recommendationsApi = {
  get: async (): Promise<Course[]> => {
    const { data } = await api.get<RecommendationsResponse>('/api/recommendations');
    return data.recommendations;
  },
};

export const handleApiError = (error: unknown): string => {
  if (error instanceof AxiosError) {
    if (error.response?.data?.error) {
      return error.response.data.error;
    }
    if (error.response?.data?.errors) {
      return error.response.data.errors.map((e: { msg: string }) => e.msg).join(', ');
    }
    if (error.message) {
      return error.message;
    }
  }
  return 'An unexpected error occurred';
};

export default api;
