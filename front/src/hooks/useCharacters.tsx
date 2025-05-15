import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { characterService } from '@/lib/api/services';
import { Character, CharacterCreate, CharacterUpdate } from '@/lib/api/types';

// Keys para React Query
const CHARACTERS_KEY = 'characters';

// Función auxiliar para verificar si el usuario está autenticado
const isAuthenticated = () => {
  return !!localStorage.getItem('auth_token');
};

/**
 * Hook personalizado para obtener un personaje específico
 */
export const useCharacter = (characterId: string | undefined) => {
  return useQuery({
    queryKey: [CHARACTERS_KEY, characterId],
    queryFn: () => characterId ? characterService.getCharacter(characterId) : Promise.reject('ID no proporcionado'),
    enabled: !!characterId && isAuthenticated(),
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
};

/**
 * Hook personalizado para gestionar los personajes
 */
export const useCharacters = () => {
  const queryClient = useQueryClient();

  // Consulta para obtener todos los personajes del usuario
  const {
    data: characters = [],
    isLoading: isLoadingCharacters,
    error: charactersError,
    refetch: refetchCharacters
  } = useQuery({
    queryKey: [CHARACTERS_KEY],
    queryFn: () => characterService.getUserCharacters(),
    enabled: isAuthenticated(),
    staleTime: 5 * 60 * 1000, // 5 minutos
  });

  // Mutación para crear un personaje
  const createCharacterMutation = useMutation({
    mutationFn: (characterData: CharacterCreate) => 
      characterService.createCharacter(characterData),
    onSuccess: (newCharacter) => {
      // Actualizar la cache de personajes
      queryClient.setQueryData<Character[]>(
        [CHARACTERS_KEY],
        (oldCharacters = []) => [...oldCharacters, newCharacter]
      );
      toast.success('¡Personaje creado con éxito!');
    },
    onError: (error: Error) => {
      console.error('Error al crear personaje:', error);
      toast.error(`Error al crear personaje: ${error.message}`);
    }
  });

  // Mutación para actualizar un personaje
  const updateCharacterMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: CharacterUpdate }) => 
      characterService.updateCharacter(id, data),
    onSuccess: (updatedCharacter) => {
      // Actualizar la cache del personaje específico
      queryClient.setQueryData(
        [CHARACTERS_KEY, updatedCharacter.id], 
        updatedCharacter
      );
      
      // Actualizar la lista de personajes
      queryClient.setQueryData<Character[]>(
        [CHARACTERS_KEY],
        (oldCharacters = []) => 
          oldCharacters.map(char => 
            char.id === updatedCharacter.id ? updatedCharacter : char
          )
      );
      
      toast.success('¡Personaje actualizado con éxito!');
    },
    onError: (error: Error) => {
      console.error('Error al actualizar personaje:', error);
      toast.error(`Error al actualizar personaje: ${error.message}`);
    }
  });
  
  // Mutación para eliminar un personaje
  const deleteCharacterMutation = useMutation({
    mutationFn: (characterId: string) => 
      characterService.deleteCharacter(characterId),
    onSuccess: (_, deletedId) => {
      // Eliminar personaje de la cache
      queryClient.setQueryData<Character[]>(
        [CHARACTERS_KEY],
        (oldCharacters = []) => 
          oldCharacters.filter(char => char.id !== deletedId)
      );
      
      // Invalidar la consulta del personaje específico
      queryClient.removeQueries({ queryKey: [CHARACTERS_KEY, deletedId] });
      
      toast.success('Personaje eliminado con éxito');
    },
    onError: (error: Error) => {
      console.error('Error al eliminar personaje:', error);
      toast.error(`Error al eliminar personaje: ${error.message}`);
    }
  });

  // Funciones para usar en componentes
  const createCharacter = (characterData: CharacterCreate) => {
    return createCharacterMutation.mutateAsync(characterData);
  };

  const updateCharacter = (id: string, data: CharacterUpdate) => {
    return updateCharacterMutation.mutateAsync({ id, data });
  };

  const deleteCharacter = (characterId: string) => {
    return deleteCharacterMutation.mutateAsync(characterId);
  };

  return {
    characters,
    isLoadingCharacters,
    charactersError,
    refetchCharacters,
    createCharacter,
    updateCharacter,
    deleteCharacter,
    isCreating: createCharacterMutation.isPending,
    isUpdating: updateCharacterMutation.isPending,
    isDeleting: deleteCharacterMutation.isPending
  };
};

export default useCharacters; 