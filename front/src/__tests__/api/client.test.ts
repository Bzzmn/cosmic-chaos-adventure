import { describe, it, expect, beforeEach, vi } from 'vitest';
import apiClient, { fetchWithRetry } from '../../lib/api/client';
import { API_BASE_URL, API_ROUTES } from '../../lib/api/config';
import { server } from '../setup';
import { http, HttpResponse } from 'msw';
import axios, { AxiosResponse } from 'axios';

describe('API Client', () => {
  it('should have the correct base URL', () => {
    expect(apiClient.defaults.baseURL).toBe(API_BASE_URL);
  });

  it('should have the correct default headers', () => {
    expect(apiClient.defaults.headers.common['Content-Type']).toBe('application/json');
    expect(apiClient.defaults.headers.common['Accept']).toBe('application/json');
  });

  // Test fetchWithRetry con mock de response
  it('should return data when fetchWithRetry is successful', async () => {
    // Configurar mock
    server.use(
      http.get(`${API_BASE_URL}${API_ROUTES.health}`, () => {
        return HttpResponse.json({ status: 'ok', message: 'API is running' });
      })
    );

    // Ejecutar fetchWithRetry
    const data = await fetchWithRetry({
      method: 'GET',
      url: API_ROUTES.health,
    });

    // Verificar resultado
    expect(data).toEqual({ status: 'ok', message: 'API is running' });
  });

  // Test fetchWithRetry con retry (simulando un error 500)
  it('should retry on server errors', async () => {
    let attempts = 0;

    // Mock para Axios
    const axiosRequestSpy = vi.spyOn(apiClient, 'request');
    axiosRequestSpy.mockImplementation(async () => {
      attempts++;
      if (attempts === 1) {
        // Crear un error de Axios
        const error = new axios.AxiosError(
          'Service Unavailable',
          '503',
          { url: '/test' } as Record<string, string>,
          {},
          { 
            status: 503,
            statusText: 'Service Unavailable',
            headers: {},
            config: { url: '/test' } as Record<string, unknown>,
            data: { message: 'Service unavailable' }
          } as AxiosResponse
        );
        throw error;
      }
      return { data: { success: true } };
    });

    // Ejecutar fetchWithRetry (debería reintentar y tener éxito en el segundo intento)
    const result = await fetchWithRetry({ url: '/test' }, 2);
    
    // Verificar resultado
    expect(attempts).toBe(2);
    expect(result).toEqual({ success: true });
    
    // Restaurar spy
    axiosRequestSpy.mockRestore();
  });
});

// Test de autenticación
describe('Auth Token in Request', () => {
  beforeEach(() => {
    // Limpiar localStorage antes de cada test
    localStorage.clear();
  });

  it('should add authorization header when token exists', async () => {
    // Preparar
    localStorage.setItem('auth_token', 'test-token');
    
    // Configurar mock
    let headers: Record<string, string> = {};
    server.use(
      http.get(`${API_BASE_URL}/test-auth`, ({ request }) => {
        headers = Object.fromEntries(request.headers) as Record<string, string>;
        return HttpResponse.json({ success: true });
      })
    );

    // Ejecutar
    await apiClient.get('/test-auth');

    // Verificar
    expect(headers.authorization).toBe('Bearer test-token');
  });

  it('should not add authorization header when token does not exist', async () => {
    // Configurar mock
    let headers: Record<string, string> = {};
    server.use(
      http.get(`${API_BASE_URL}/test-auth`, ({ request }) => {
        headers = Object.fromEntries(request.headers) as Record<string, string>;
        return HttpResponse.json({ success: true });
      })
    );

    // Ejecutar
    await apiClient.get('/test-auth');

    // Verificar que no hay header de autorización
    expect(headers.authorization).toBeFalsy();
  });
}); 