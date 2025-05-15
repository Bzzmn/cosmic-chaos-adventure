import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { useTranslation } from 'react-i18next';
import { personalityService } from '@/lib/api/services';
import { PersonalityQuestion, PersonalityTestResults } from '@/lib/api/types';

// Keys para React Query
const PERSONALITY_QUESTIONS_KEY = 'personality-questions';
const PERSONALITY_RESULTS_KEY = 'personality-results';

// Función auxiliar para verificar si el usuario está autenticado
const isAuthenticated = () => {
  return !!localStorage.getItem('auth_token');
};

/**
 * Hook personalizado para gestionar el test de personalidad
 */
export const usePersonality = (userId?: string) => {
  const queryClient = useQueryClient();
  const { t, i18n } = useTranslation();
  
  // Obtener el idioma actual
  const currentLanguage = i18n.language || 'en';

  // Consulta para obtener las preguntas del test
  const {
    data: questions = [],
    isLoading: isLoadingQuestions,
    error: questionsError,
    refetch: refetchQuestions
  } = useQuery({
    queryKey: [PERSONALITY_QUESTIONS_KEY, currentLanguage],
    queryFn: () => personalityService.getQuestions(),
    staleTime: 24 * 60 * 60 * 1000, // 24 horas (las preguntas cambian poco)
  });

  // Consulta para obtener resultados existentes (si los hay)
  const {
    data: results,
    isLoading: isLoadingResults,
    error: resultsError,
    refetch: refetchResults
  } = useQuery({
    queryKey: [PERSONALITY_RESULTS_KEY, userId, currentLanguage],
    queryFn: async () => {
      // Aquí podríamos agregar un endpoint para obtener resultados guardados
      // Por ahora dejamos esto como placeholder
      return null as PersonalityTestResults | null;
    },
    enabled: isAuthenticated() && !!userId,
    staleTime: 10 * 60 * 1000, // 10 minutos
  });

  // Mutación para enviar respuestas del test
  const submitAnswersMutation = useMutation({
    mutationFn: ({ userId, answers }: { userId: string; answers: number[] }) => 
      personalityService.submitAnswers(userId, answers),
    onSuccess: (data) => {
      // Guardar resultados en caché
      queryClient.setQueryData(
        [PERSONALITY_RESULTS_KEY, userId, currentLanguage],
        data
      );
      
      toast.success(t('personalityTest.success'));
    },
    onError: (error: Error) => {
      console.error('Error al enviar respuestas del test:', error);
      toast.error(t('personalityTest.error', { message: error.message }));
    }
  });

  // Función para enviar respuestas
  const submitAnswers = (userId: string, answers: number[]) => {
    return submitAnswersMutation.mutateAsync({ userId, answers });
  };

  return {
    questions,
    isLoadingQuestions,
    questionsError,
    refetchQuestions,
    results,
    isLoadingResults,
    resultsError,
    refetchResults,
    submitAnswers,
    isSubmitting: submitAnswersMutation.isPending
  };
};

export default usePersonality; 