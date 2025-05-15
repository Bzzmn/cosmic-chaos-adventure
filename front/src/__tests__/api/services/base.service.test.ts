/**
 * Tests para el servicio base
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { BaseService } from '../../../lib/api/services';
import { fetchWithRetry } from '../../../lib/api/client';

// Definir una interfaz para probar
interface TestEntity {
  id: string;
  name: string;
  value: number;
}

// Mock para fetchWithRetry
vi.mock('../../../lib/api/client', () => ({
  fetchWithRetry: vi.fn(),
  default: {
    request: vi.fn()
  }
}));

// Crear una clase de servicio concreta para pruebas
class TestService extends BaseService<TestEntity> {
  constructor() {
    super('/api/test');
  }
}

describe('BaseService', () => {
  let service: TestService;
  
  // Datos de prueba
  const testEntity: TestEntity = {
    id: '123',
    name: 'Test Entity',
    value: 42
  };
  
  beforeEach(() => {
    // Crear instancia de servicio para pruebas
    service = new TestService();
    
    // Resetear mocks
    vi.mocked(fetchWithRetry).mockClear();
  });
  
  describe('getAll', () => {
    it('should fetch all entities', async () => {
      // Mock de respuesta
      vi.mocked(fetchWithRetry).mockResolvedValueOnce([testEntity]);
      
      const result = await service.getAll();
      
      // Verificar resultado
      expect(result).toEqual([testEntity]);
      
      // Verificar que se llamó fetchWithRetry correctamente
      expect(fetchWithRetry).toHaveBeenCalledWith(expect.objectContaining({
        method: 'GET',
        url: '/api/test'
      }));
    });
    
    it('should fetch all entities with pagination', async () => {
      // Mock de respuesta
      vi.mocked(fetchWithRetry).mockResolvedValueOnce([testEntity]);
      
      const result = await service.getAll({ skip: 10, limit: 20 });
      
      // Verificar resultado
      expect(result).toEqual([testEntity]);
      
      // Verificar que se llamó fetchWithRetry correctamente
      expect(fetchWithRetry).toHaveBeenCalledWith(expect.objectContaining({
        method: 'GET',
        url: '/api/test',
        params: { skip: 10, limit: 20 }
      }));
    });
    
    it('should handle errors in getAll', async () => {
      // Mock de error
      const error = new Error('Test error');
      vi.mocked(fetchWithRetry).mockRejectedValueOnce(error);
      
      // Espiar console.error
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
      
      // Verificar que el error se propaga
      await expect(service.getAll()).rejects.toThrow(error);
      
      // Verificar que se registró el error
      expect(consoleSpy).toHaveBeenCalled();
      
      // Restaurar console.error
      consoleSpy.mockRestore();
    });
  });
  
  describe('getById', () => {
    it('should fetch entity by id', async () => {
      // Mock de respuesta
      vi.mocked(fetchWithRetry).mockResolvedValueOnce(testEntity);
      
      const result = await service.getById('123');
      
      // Verificar resultado
      expect(result).toEqual(testEntity);
      
      // Verificar que se llamó fetchWithRetry correctamente
      expect(fetchWithRetry).toHaveBeenCalledWith(expect.objectContaining({
        method: 'GET',
        url: '/api/test/123'
      }));
    });
  });
  
  describe('create', () => {
    it('should create a new entity', async () => {
      // Mock de respuesta
      vi.mocked(fetchWithRetry).mockResolvedValueOnce(testEntity);
      
      const data = { name: 'New Entity', value: 99 };
      const result = await service.create(data);
      
      // Verificar resultado
      expect(result).toEqual(testEntity);
      
      // Verificar que se llamó fetchWithRetry correctamente
      expect(fetchWithRetry).toHaveBeenCalledWith(expect.objectContaining({
        method: 'POST',
        url: '/api/test',
        data
      }));
    });
  });
  
  describe('update', () => {
    it('should update an existing entity', async () => {
      // Mock de respuesta
      const updatedEntity = { ...testEntity, name: 'Updated Entity' };
      vi.mocked(fetchWithRetry).mockResolvedValueOnce(updatedEntity);
      
      const data = { name: 'Updated Entity' };
      const result = await service.update('123', data);
      
      // Verificar resultado
      expect(result).toEqual(updatedEntity);
      
      // Verificar que se llamó fetchWithRetry correctamente
      expect(fetchWithRetry).toHaveBeenCalledWith(expect.objectContaining({
        method: 'PUT',
        url: '/api/test/123',
        data
      }));
    });
  });
  
  describe('delete', () => {
    it('should delete an entity', async () => {
      // Mock de respuesta
      vi.mocked(fetchWithRetry).mockResolvedValueOnce(undefined);
      
      await service.delete('123');
      
      // Verificar que se llamó fetchWithRetry correctamente
      expect(fetchWithRetry).toHaveBeenCalledWith(expect.objectContaining({
        method: 'DELETE',
        url: '/api/test/123'
      }));
    });
  });
}); 