import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { adventureService } from '@/lib/api/services';
import { StoryStep, CharacterProgressResponse } from '@/lib/api/types';

// Keys para React Query
const ADVENTURE_STORY_KEY = 'adventure-story';
const ADVENTURE_PROGRESS_KEY = 'adventure-progress';

// Función auxiliar para verificar si el usuario está autenticado
const isAuthenticated = () => {
  return !!localStorage.getItem('auth_token');
};

/**
 * Hook personalizado para gestionar aventuras
 */
export const useAdventure = (adventureId?: string, characterId?: string) => {
  const queryClient = useQueryClient();

  // Consulta para obtener los pasos de la historia
  const {
    data: storySteps = [],
    isLoading: isLoadingStory,
    error: storyError,
    refetch: refetchStory
  } = useQuery({
    queryKey: [ADVENTURE_STORY_KEY, adventureId],
    queryFn: () => adventureId ? adventureService.getStory(adventureId) : Promise.resolve([]),
    enabled: isAuthenticated() && !!adventureId,
    staleTime: 30 * 60 * 1000, // 30 minutos
  });

  // Mutación para guardar el progreso
  const saveProgressMutation = useMutation({
    mutationFn: ({ 
      characterId, 
      currentStep, 
      choices 
    }: { 
      characterId: string; 
      currentStep: number; 
      choices: number[] 
    }) => adventureService.saveProgress(characterId, currentStep, choices),
    onSuccess: (data) => {
      // Guardar el progreso en caché
      queryClient.setQueryData(
        [ADVENTURE_PROGRESS_KEY, data.character_id, adventureId],
        data
      );
      
      toast.success('Progreso guardado con éxito');
    },
    onError: (error: Error) => {
      console.error('Error al guardar progreso:', error);
      toast.error(`Error al guardar progreso: ${error.message}`);
    }
  });

  // Función para guardar el progreso
  const saveProgress = (characterId: string, currentStep: number, choices: number[]) => {
    return saveProgressMutation.mutateAsync({ characterId, currentStep, choices });
  };

  return {
    storySteps,
    isLoadingStory,
    storyError,
    refetchStory,
    saveProgress,
    isSavingProgress: saveProgressMutation.isPending
  };
};

export default useAdventure; 