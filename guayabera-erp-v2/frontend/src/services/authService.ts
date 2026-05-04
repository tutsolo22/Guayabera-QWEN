import axios from 'axios';
import { createAsyncThunk } from '@reduxjs/toolkit';

// Create axios instance
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
});

// Request interceptor to add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle common errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const login = createAsyncThunk(
  'auth/login',
  async ({ email, password }: { email: string; password: string }, { rejectWithValue }) => {
    try {
      const response = await api.post('/auth/login', { email, password });
      return {
        user: response.data.user,
        token: response.data.access_token,
      };
    } catch (error: any) {
      return rejectWithValue(error.response.data.detail || 'Error de autenticación');
    }
  }
);

export const register = createAsyncThunk(
  'auth/register',
  async (
    { email, password, nombre_completo }: { email: string; password: string; nombre_completo: string },
    { rejectWithValue }
  ) => {
    try {
      const response = await api.post('/auth/solicitar-registro', { email, nombre_completo });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response.data.detail || 'Error en el registro');
    }
  }
);

export const recoverPassword = async (email: string) => {
  try {
    const response = await api.post('/auth/solicitar-recuperacion', { email });
    return response.data;
  } catch (error: any) {
    throw new Error(error.response.data.detail || 'Error al recuperar la contraseña');
  }
};

export const confirmRegistration = async (token: string, newPassword: string) => {
  try {
    const response = await api.post(`/auth/confirmar-registro/${token}`, { nueva_contrasena: newPassword });
    return response.data;
  } catch (error: any) {
    throw new Error(error.response.data.detail || 'Error al confirmar el registro');
  }
};

// API functions for managing tenants, users, and licenses
export const getTenants = async () => {
  try {
    const response = await api.get('/tenants/');
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Error al obtener tenants');
  }
};

export const getUsers = async () => {
  try {
    const response = await api.get('/users/');
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Error al obtener usuarios');
  }
};

export const getLicenses = async () => {
  try {
    const response = await api.get('/licencias/');
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Error al obtener licencias');
  }
};