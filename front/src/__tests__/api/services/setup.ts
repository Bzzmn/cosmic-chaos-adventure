/**
 * Configuración para pruebas de servicios
 */
import { http, HttpResponse } from 'msw';
import { API_BASE_URL, API_ROUTES } from '../../../lib/api/config';
import { User, UserWithToken } from '../../../lib/api/types';

// Datos de prueba para usuario
export const mockUser: User = {
  id: '123e4567-e89b-12d3-a456-426614174000',
  name: 'Usuario Prueba',
  email: 'test@example.com',
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString()
};

// Datos de prueba para usuario con token
export const mockUserWithToken: UserWithToken = {
  ...mockUser,
  token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test-token-mock'
};

// Handlers para autenticación
export const authHandlers = [
  // Login
  http.post(`${API_BASE_URL}${API_ROUTES.auth.login}`, async () => {
    return HttpResponse.json(mockUserWithToken, { status: 200 });
  }),
  
  // Registro
  http.post(`${API_BASE_URL}${API_ROUTES.auth.register}`, async () => {
    return HttpResponse.json(mockUserWithToken, { status: 201 });
  }),
  
  // Social Login
  http.post(`${API_BASE_URL}${API_ROUTES.auth.socialLogin}`, async () => {
    return HttpResponse.json(mockUserWithToken, { status: 200 });
  }),
  
  // Perfil de usuario
  http.get(`${API_BASE_URL}${API_ROUTES.auth.profile}`, async () => {
    return HttpResponse.json(mockUser, { status: 200 });
  }),
  
  // Actualizar perfil
  http.put(`${API_BASE_URL}${API_ROUTES.auth.profile}`, async () => {
    return HttpResponse.json({
      ...mockUser,
      name: 'Usuario Actualizado'
    }, { status: 200 });
  })
];

// Datos de prueba para personajes
export const mockCharacter = {
  id: '123e4567-e89b-12d3-a456-426614174001',
  name: 'Personaje Prueba',
  character_class: 'Camarero Cuántico',
  stats: {
    quantumCharisma: 50,
    absurdityResistance: 40,
    sarcasmLevel: 70,
    timeWarping: 30,
    cosmicLuck: 60
  },
  user_id: mockUser.id,
  image_url: 'https://example.com/character.jpg',
  experience: 100,
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
  artifacts: []
};

// Handlers para personajes
export const characterHandlers = [
  // Obtener todos los personajes
  http.get(`${API_BASE_URL}${API_ROUTES.characters.base}`, async () => {
    return HttpResponse.json([mockCharacter], { status: 200 });
  }),
  
  // Obtener un personaje específico
  http.get(`${API_BASE_URL}${API_ROUTES.characters.detail(mockCharacter.id)}`, async () => {
    return HttpResponse.json(mockCharacter, { status: 200 });
  }),
  
  // Crear personaje
  http.post(`${API_BASE_URL}${API_ROUTES.characters.base}`, async () => {
    return HttpResponse.json(mockCharacter, { status: 201 });
  }),
  
  // Actualizar personaje
  http.put(`${API_BASE_URL}${API_ROUTES.characters.detail(mockCharacter.id)}`, async () => {
    return HttpResponse.json({
      ...mockCharacter,
      name: 'Personaje Actualizado'
    }, { status: 200 });
  }),
  
  // Eliminar personaje
  http.delete(`${API_BASE_URL}${API_ROUTES.characters.detail(mockCharacter.id)}`, async () => {
    return new HttpResponse(null, { status: 204 });
  })
];

// Exportar todos los handlers juntos
export const serviceHandlers = [
  ...authHandlers,
  ...characterHandlers
]; 