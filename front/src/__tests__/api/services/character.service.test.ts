/**
 * Tests para el servicio de personajes
 */
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { server } from '../../setup';
import { characterService } from '../../../lib/api/services';
import { mockCharacter, serviceHandlers } from './setup';
import { CharacterCreate, CharacterUpdate } from '../../../lib/api/types';
import { fetchWithRetry } from '../../../lib/api/client';

// Mock para fetchWithRetry
vi.mock('../../../lib/api/client', () => ({
  fetchWithRetry: vi.fn(),
  default: {
    request: vi.fn()
  }
}));

describe('CharacterService', () => {
  beforeEach(() => {
    // Limpiar localStorage y establecer los handlers para servicios
    localStorage.clear();
    localStorage.setItem('auth_token', 'mock-token');
    server.use(...serviceHandlers);
    
    // Resetear mocks
    vi.mocked(fetchWithRetry).mockClear();
  });
  
  afterEach(() => {
    vi.restoreAllMocks();
  });
  
  describe('getUserCharacters', () => {
    it('should get all user characters', async () => {
      // Mock de respuesta
      vi.mocked(fetchWithRetry).mockResolvedValueOnce([mockCharacter]);
      
      const result = await characterService.getUserCharacters();
      
      // Verificar resultado
      expect(result).toEqual([mockCharacter]);
      expect(result.length).toBe(1);
      expect(result[0].name).toBe(mockCharacter.name);
      
      // Verificar que se llamó fetchWithRetry correctamente
      expect(fetchWithRetry).toHaveBeenCalledWith(expect.objectContaining({
        method: 'GET',
        url: expect.stringContaining('/api/characters')
      }));
    });
  });
  
  describe('getCharacter', () => {
    it('should get a character by id', async () => {
      // Mock de respuesta
      vi.mocked(fetchWithRetry).mockResolvedValueOnce(mockCharacter);
      
      const result = await characterService.getCharacter(mockCharacter.id);
      
      // Verificar resultado
      expect(result).toEqual(mockCharacter);
      expect(result.id).toBe(mockCharacter.id);
      
      // Verificar que se llamó fetchWithRetry correctamente
      expect(fetchWithRetry).toHaveBeenCalledWith(expect.objectContaining({
        method: 'GET',
        url: expect.stringContaining(mockCharacter.id)
      }));
    });
  });
  
  describe('createCharacter', () => {
    it('should create a new character', async () => {
      // Mock de respuesta
      vi.mocked(fetchWithRetry).mockResolvedValueOnce(mockCharacter);
      
      const characterData: CharacterCreate = {
        name: 'Nuevo Personaje',
        character_class: 'Camarero Cuántico',
        stats: {
          quantumCharisma: 50,
          absurdityResistance: 40,
          sarcasmLevel: 70,
          timeWarping: 30,
          cosmicLuck: 60
        }
      };
      
      const result = await characterService.createCharacter(characterData);
      
      // Verificar resultado
      expect(result).toEqual(mockCharacter);
      
      // Verificar que se llamó fetchWithRetry correctamente
      expect(fetchWithRetry).toHaveBeenCalledWith(expect.objectContaining({
        method: 'POST',
        url: expect.stringContaining('/api/characters'),
        data: characterData
      }));
    });
  });
  
  describe('updateCharacter', () => {
    it('should update an existing character', async () => {
      // Mock de respuesta con el personaje actualizado
      const updatedCharacter = {
        ...mockCharacter,
        name: 'Personaje Actualizado',
        experience: 200
      };
      
      vi.mocked(fetchWithRetry).mockResolvedValueOnce(updatedCharacter);
      
      const updateData: CharacterUpdate = {
        name: 'Personaje Actualizado',
        experience: 200
      };
      
      const result = await characterService.updateCharacter(mockCharacter.id, updateData);
      
      // Verificar resultado
      expect(result.name).toBe('Personaje Actualizado');
      expect(result.experience).toBe(200);
      
      // Verificar que se llamó fetchWithRetry correctamente
      expect(fetchWithRetry).toHaveBeenCalledWith(expect.objectContaining({
        method: 'PUT',
        url: expect.stringContaining(mockCharacter.id),
        data: updateData
      }));
    });
  });
  
  describe('deleteCharacter', () => {
    it('should delete a character', async () => {
      // Mock de respuesta
      vi.mocked(fetchWithRetry).mockResolvedValueOnce(undefined);
      
      await characterService.deleteCharacter(mockCharacter.id);
      
      // Verificar que se llamó fetchWithRetry correctamente
      expect(fetchWithRetry).toHaveBeenCalledWith(expect.objectContaining({
        method: 'DELETE',
        url: expect.stringContaining(mockCharacter.id)
      }));
    });
  });
}); 