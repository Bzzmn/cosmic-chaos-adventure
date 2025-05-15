import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { artifactService } from '@/lib/api/services';
import { Artifact, Character } from '@/lib/api/types';

// Keys para React Query
const ARTIFACTS_KEY = 'artifacts';
const CHARACTER_KEY = 'characters';

// Función auxiliar para verificar si el usuario está autenticado
const isAuthenticated = () => {
  return !!localStorage.getItem('auth_token');
};

/**
 * Hook personalizado para gestionar los artefactos
 */
export const useArtifacts = () => {
  const queryClient = useQueryClient();

  // Consulta para obtener todos los artefactos disponibles
  const {
    data: artifacts = [],
    isLoading: isLoadingArtifacts,
    error: artifactsError,
    refetch: refetchArtifacts
  } = useQuery({
    queryKey: [ARTIFACTS_KEY],
    queryFn: () => artifactService.getAllArtifacts(),
    enabled: isAuthenticated(),
    staleTime: 10 * 60 * 1000, // 10 minutos
  });

  // Mutación para agregar un artefacto a un personaje
  const addArtifactMutation = useMutation({
    mutationFn: ({ characterId, artifactId }: { characterId: string; artifactId: string }) => 
      artifactService.addArtifactToCharacter(characterId, artifactId),
    onSuccess: (updatedCharacter) => {
      // Actualizar la caché del personaje
      queryClient.setQueryData(
        [CHARACTER_KEY, updatedCharacter.id],
        updatedCharacter
      );
      
      // Actualizar la lista de personajes
      queryClient.invalidateQueries({ queryKey: [CHARACTER_KEY] });
      
      toast.success('Artefacto agregado con éxito');
    },
    onError: (error: Error) => {
      console.error('Error al agregar artefacto:', error);
      toast.error(`Error al agregar artefacto: ${error.message}`);
    }
  });
  
  // Mutación para actualizar un artefacto de un personaje
  const updateArtifactMutation = useMutation({
    mutationFn: ({ 
      characterId, 
      artifactId, 
      isActive 
    }: { 
      characterId: string; 
      artifactId: string; 
      isActive: boolean 
    }) => artifactService.updateCharacterArtifact(characterId, artifactId, isActive),
    onSuccess: (updatedCharacter) => {
      // Actualizar la caché del personaje
      queryClient.setQueryData(
        [CHARACTER_KEY, updatedCharacter.id],
        updatedCharacter
      );
      
      // Actualizar la lista de personajes
      queryClient.invalidateQueries({ queryKey: [CHARACTER_KEY] });
      
      toast.success('Artefacto actualizado con éxito');
    },
    onError: (error: Error) => {
      console.error('Error al actualizar artefacto:', error);
      toast.error(`Error al actualizar artefacto: ${error.message}`);
    }
  });

  // Funciones para usar en componentes
  const addArtifactToCharacter = (characterId: string, artifactId: string) => {
    return addArtifactMutation.mutateAsync({ characterId, artifactId });
  };

  const updateCharacterArtifact = (characterId: string, artifactId: string, isActive: boolean) => {
    return updateArtifactMutation.mutateAsync({ characterId, artifactId, isActive });
  };

  return {
    artifacts,
    isLoadingArtifacts,
    artifactsError,
    refetchArtifacts,
    addArtifactToCharacter,
    updateCharacterArtifact,
    isAddingArtifact: addArtifactMutation.isPending,
    isUpdatingArtifact: updateArtifactMutation.isPending
  };
};

export default useArtifacts; 