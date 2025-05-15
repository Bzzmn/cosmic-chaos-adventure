/**
 * Tests para el servicio de autenticación
 */
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { authService } from '../../../lib/api/services';
import { mockUser, mockUserWithToken } from './setup';
import { LoginCredentials, SocialLoginData, UserCreate, UserUpdate } from '../../../lib/api/types';
import { fetchWithRetry } from '../../../lib/api/client';
import * as authUtils from '../../../lib/api';

// Mock para fetchWithRetry
vi.mock('../../../lib/api/client', () => ({
  fetchWithRetry: vi.fn(),
  default: {
    request: vi.fn()
  }
}));

// Mock para funciones de autenticación
vi.mock('../../../lib/api', async () => {
  const actual = await vi.importActual('../../../lib/api');
  return {
    ...actual as object,
    setAuthToken: vi.fn(),
    setAuthUser: vi.fn(),
    removeAuthToken: vi.fn(),
    removeAuthUser: vi.fn(),
    clearAuth: vi.fn()
  };
});

describe('AuthService', () => {
  beforeEach(() => {
    // Limpiar localStorage y resetear mocks
    localStorage.clear();
    vi.mocked(fetchWithRetry).mockClear();
    vi.mocked(authUtils.setAuthToken).mockClear();
    vi.mocked(authUtils.setAuthUser).mockClear();
    vi.mocked(authUtils.removeAuthToken).mockClear();
    vi.mocked(authUtils.removeAuthUser).mockClear();
    vi.mocked(authUtils.clearAuth).mockClear();
  });
  
  afterEach(() => {
    vi.restoreAllMocks();
  });
  
  describe('register', () => {
    it('should register a new user and store token', async () => {
      const userData: UserCreate = {
        name: 'Usuario Test',
        email: 'test@example.com',
        password: 'password123'
      };
      
      // Mock de respuesta
      vi.mocked(fetchWithRetry).mockResolvedValueOnce(mockUserWithToken);
      
      const result = await authService.register(userData);
      
      // Verificar resultado
      expect(result).toEqual(mockUserWithToken);
      
      // Verificar petición
      expect(fetchWithRetry).toHaveBeenCalledWith(expect.objectContaining({
        method: 'POST',
        url: '/api/auth/register',
        data: userData
      }));
      
      // Verificar que se guardó el token y el usuario
      expect(authUtils.setAuthToken).toHaveBeenCalledWith(mockUserWithToken.token);
      expect(authUtils.setAuthUser).toHaveBeenCalledWith(mockUserWithToken);
    });
  });
  
  describe('login', () => {
    it('should login and store token', async () => {
      const credentials: LoginCredentials = {
        username: 'test@example.com',
        password: 'password123'
      };
      
      // Mock de respuesta
      vi.mocked(fetchWithRetry).mockResolvedValueOnce(mockUserWithToken);
      
      const result = await authService.login(credentials);
      
      // Verificar resultado
      expect(result).toEqual(mockUserWithToken);
      
      // Verificar petición
      expect(fetchWithRetry).toHaveBeenCalledWith(expect.objectContaining({
        method: 'POST',
        url: '/api/auth/login',
        data: expect.any(URLSearchParams),
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        }
      }));
      
      // Verificar que se guardó el token y el usuario
      expect(authUtils.setAuthToken).toHaveBeenCalledWith(mockUserWithToken.token);
      expect(authUtils.setAuthUser).toHaveBeenCalledWith(mockUserWithToken);
    });
  });
  
  describe('socialLogin', () => {
    it('should login with social provider and store token', async () => {
      const providerData: SocialLoginData = {
        provider: 'google',
        token: 'google-token-123'
      };
      
      // Mock de respuesta
      vi.mocked(fetchWithRetry).mockResolvedValueOnce(mockUserWithToken);
      
      const result = await authService.socialLogin(providerData);
      
      // Verificar resultado
      expect(result).toEqual(mockUserWithToken);
      
      // Verificar petición
      expect(fetchWithRetry).toHaveBeenCalledWith(expect.objectContaining({
        method: 'POST',
        url: '/api/auth/social-login',
        data: providerData
      }));
      
      // Verificar que se guardó el token y el usuario
      expect(authUtils.setAuthToken).toHaveBeenCalledWith(mockUserWithToken.token);
      expect(authUtils.setAuthUser).toHaveBeenCalledWith(mockUserWithToken);
    });
  });
  
  describe('getProfile', () => {
    it('should get the user profile', async () => {
      // Mock de respuesta
      vi.mocked(fetchWithRetry).mockResolvedValueOnce(mockUser);
      
      const result = await authService.getProfile();
      
      // Verificar resultado
      expect(result).toEqual(mockUser);
      
      // Verificar petición
      expect(fetchWithRetry).toHaveBeenCalledWith(expect.objectContaining({
        method: 'GET',
        url: '/api/users/profile'
      }));
    });
  });
  
  describe('updateProfile', () => {
    it('should update the user profile and update localStorage', async () => {
      const userData: UserUpdate = {
        name: 'Usuario Actualizado'
      };
      
      const updatedUser = {
        ...mockUser,
        name: 'Usuario Actualizado'
      };
      
      // Mock de respuesta
      vi.mocked(fetchWithRetry).mockResolvedValueOnce(updatedUser);
      
      // Simular usuario con token en localStorage
      localStorage.setItem('auth_user', JSON.stringify(mockUserWithToken));
      
      const result = await authService.updateProfile(userData);
      
      // Verificar resultado
      expect(result).toEqual(updatedUser);
      
      // Verificar petición
      expect(fetchWithRetry).toHaveBeenCalledWith(expect.objectContaining({
        method: 'PUT',
        url: '/api/users/profile',
        data: userData
      }));
      
      // Verificar que se actualizó el usuario en localStorage
      expect(authUtils.setAuthUser).toHaveBeenCalledWith({
        ...updatedUser,
        token: mockUserWithToken.token
      });
    });
  });
  
  describe('logout', () => {
    it('should clear localStorage on logout', () => {
      // Ejecutar logout
      authService.logout();
      
      // Verificar que se llamó a clearAuth
      expect(authUtils.clearAuth).toHaveBeenCalled();
    });
  });
  
  describe('isAuthenticated', () => {
    it('should return true when token exists', () => {
      // Establecer token en localStorage
      localStorage.setItem('auth_token', mockUserWithToken.token);
      
      // Verificar que isAuthenticated devuelve true
      expect(authService.isAuthenticated()).toBe(true);
    });
    
    it('should return false when token does not exist', () => {
      // Verificar que isAuthenticated devuelve false
      expect(authService.isAuthenticated()).toBe(false);
    });
  });
}); 