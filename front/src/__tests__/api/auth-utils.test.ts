import { describe, it, expect, beforeEach } from 'vitest';
import { 
  setAuthToken, 
  getAuthToken, 
  removeAuthToken, 
  setAuthUser, 
  getAuthUser, 
  removeAuthUser, 
  clearAuth 
} from '../../lib/api';

describe('Auth Utilities', () => {
  beforeEach(() => {
    // Limpiar localStorage antes de cada test
    localStorage.clear();
  });

  describe('Token Functions', () => {
    it('should set and get auth token', () => {
      const token = 'test-token-123';
      setAuthToken(token);
      expect(getAuthToken()).toBe(token);
      expect(localStorage.getItem('auth_token')).toBe(token);
    });

    it('should remove auth token', () => {
      setAuthToken('test-token');
      removeAuthToken();
      expect(getAuthToken()).toBeNull();
      expect(localStorage.getItem('auth_token')).toBeNull();
    });
  });

  describe('User Functions', () => {
    it('should set and get auth user', () => {
      const user = { id: '123', name: 'Test User', email: 'test@example.com' };
      setAuthUser(user);
      expect(getAuthUser()).toEqual(user);
      expect(JSON.parse(localStorage.getItem('auth_user') || '{}')).toEqual(user);
    });

    it('should return null if user does not exist', () => {
      expect(getAuthUser()).toBeNull();
    });

    it('should return null if user is not valid JSON', () => {
      localStorage.setItem('auth_user', 'invalid-json');
      expect(getAuthUser()).toBeNull();
    });

    it('should remove auth user', () => {
      setAuthUser({ id: '123', name: 'Test User' });
      removeAuthUser();
      expect(getAuthUser()).toBeNull();
      expect(localStorage.getItem('auth_user')).toBeNull();
    });
  });

  describe('Clear Auth', () => {
    it('should clear both token and user', () => {
      setAuthToken('test-token');
      setAuthUser({ id: '123', name: 'Test User' });
      
      clearAuth();
      
      expect(getAuthToken()).toBeNull();
      expect(getAuthUser()).toBeNull();
      expect(localStorage.getItem('auth_token')).toBeNull();
      expect(localStorage.getItem('auth_user')).toBeNull();
    });
  });
}); 