import { afterAll, afterEach, beforeAll } from 'vitest';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

// Mock del localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Crear servidor MSW para interceptar peticiones HTTP
export const server = setupServer(
  // Mock para endpoint de salud
  http.get('*/api/health', () => {
    return HttpResponse.json(
      { status: 'ok', message: 'API running' },
      { status: 200 }
    );
  }),
);

// Configurar server antes de todos los tests
beforeAll(() => server.listen());

// Resetear handlers después de cada test
afterEach(() => {
  server.resetHandlers();
  localStorageMock.clear();
});

// Cerrar server después de todos los tests
afterAll(() => server.close()); 