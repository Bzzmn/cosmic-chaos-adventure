import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { toast } from 'sonner';
import { useTranslation } from 'react-i18next';
import StarryBackground from '@/components/StarryBackground';
import CosmicParticles from '@/components/CosmicParticles';
import CosmicButton from '@/components/CosmicButton';
import NeonTitle from '@/components/NeonTitle';
import GalaxyCard from '@/components/GalaxyCard';
import TypewriterText from '@/components/TypewriterText';
import { ArrowRight, ArrowLeft } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { usePersonalityStore } from '@/lib/store';
import { PersonalityQuestion, PersonalityTestResults } from '@/lib/api/types/personality.types';
import { usePersonality } from '@/hooks/usePersonality';

const POINTS_PER_OPTION_VALUE = 10; // Each option value (1-4) gives 10-40 points

const PersonalityTest: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useTranslation();
  const { isAuthenticated, user } = useAuth();
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [showFeedback, setShowFeedback] = useState<string | null>(null);
  
  // Custom hook para obtener las preguntas desde el API
  const { questions: questionsFromApi, submitAnswers } = usePersonality(user?.id);
  
  // Zustand store para gestionar el estado del test
  const {
    questions: storedQuestions,
    setQuestions,
    answers,
    addAnswer,
    setAnswers,
    isTestCompleted,
    setTestCompleted,
    resetStore
  } = usePersonalityStore();
  
  // Las preguntas vendrán del store o del API
  const questions = storedQuestions.length > 0 ? storedQuestions : questionsFromApi;
  
  // Cargar preguntas cuando estén disponibles desde el API
  useEffect(() => {
    if (questionsFromApi.length > 0 && storedQuestions.length === 0) {
      setQuestions(questionsFromApi);
    }
  }, [questionsFromApi, storedQuestions.length, setQuestions]);
  
  // Efecto para manejar al completar todas las preguntas
  useEffect(() => {
    // Si completamos el test y tenemos todas las respuestas
    if (isTestCompleted && answers.length === questions.length) {
      if (isAuthenticated && user?.id) {
        // Calculamos los resultados para enviar al API
        const apiAnswers = [...answers];
        
        // Enviar al API y redirigir
        submitAnswers(user.id, apiAnswers)
          .then(() => {
            navigate('/character-creation');
          })
          .catch((error) => {
            console.error('Error al enviar respuestas:', error);
            toast.error(t('common.error'));
          });
      } else {
        // Si no hay usuario, guardamos en storage y vamos a auth
        navigate('/auth', { 
          state: { 
            fromTest: true 
          } 
        });
      }
    }
  }, [isTestCompleted, answers, questions.length, isAuthenticated, user, navigate, submitAnswers, t]);
  
  const handleAnswer = (answerIndex: number) => {
    if (!questions[currentQuestion]) return;
    
    const answer = questions[currentQuestion].options[answerIndex];
    
    // Guardar respuesta en el store
    addAnswer(currentQuestion, answerIndex);
    
    // Mostrar feedback
    if (answer.feedback) {
      setShowFeedback(answer.feedback);
    }
    
    // Mostrar toast
    toast.success(t('personalityTest.pointsGained', { 
      points: answer.value * POINTS_PER_OPTION_VALUE,
      effect: translateEffect(answer.effect)
    }), {
      icon: answer.emoji,
    });
    
    // Después de un delay, ir a la siguiente pregunta o finalizar
    setTimeout(() => {
      setShowFeedback(null);
      if (currentQuestion < questions.length - 1) {
        setCurrentQuestion(currentQuestion + 1);
      } else {
        // Test completado, marcar como completado en el store
        setTestCompleted(true);
      }
    }, 3000);
  };
  
  const translateEffect = (effect: Record<string, number>) => {
    // Encontrar la propiedad con el valor más alto
    const [mainEffect] = Object.entries(effect).sort((a, b) => b[1] - a[1])[0] || ['', 0];
    
    // Usar las traducciones para el efecto
    const traitKey = `personalityTest.traits.${mainEffect}`;
    return t(traitKey, mainEffect); // Usar el mainEffect como fallback si no hay traducción
  };
  
  const handleBack = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    } else {
      navigate('/');
    }
  };
  
  // Si no hay preguntas, mostrar indicador de carga
  if (questions.length === 0) {
    return (
      <div className="relative min-h-screen flex flex-col items-center justify-center">
        <StarryBackground />
        <CosmicParticles />
        <div className="text-center">
          <div className="relative w-20 h-20 mx-auto mb-4">
            <div className="absolute inset-0 rounded-full border-4 border-t-cosmic-magenta border-r-cosmic-cyan border-b-cosmic-green border-l-transparent animate-cosmic-spin"></div>
          </div>
          <p className="text-lg text-white/80">{t('personalityTest.loading')}</p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center px-4 py-20">
      <StarryBackground />
      <CosmicParticles />
      
      <div className="max-w-3xl w-full mx-auto z-10">
        <div className="mb-8 text-center">
          <NeonTitle variant="cyan" size="lg">{t('personalityTest.title')}</NeonTitle>
          <div className="mt-4 mb-6">
            <div className="flex justify-center items-center">
              {questions.map((_, index) => (
                <div 
                  key={index}
                  className={`h-2 w-12 mx-1 rounded-full ${index === currentQuestion ? 'bg-cosmic-cyan' : index < currentQuestion ? 'bg-cosmic-green' : 'bg-white/20'}`}
                />
              ))}
            </div>
            <p className="mt-2 text-white/70 text-sm">
              {t('personalityTest.question', { current: currentQuestion + 1, total: questions.length })}
            </p>
          </div>
        </div>
        
        <GalaxyCard hasGlow glowColor="cyan" className="mb-6 min-h-[12rem]">
          <div className="h-full flex flex-col justify-center">
            {showFeedback ? (
              <div className="text-center p-4">
                <TypewriterText 
                  text={showFeedback} 
                  className="text-lg text-cosmic-green italic"
                />
              </div>
            ) : (
              <>
                {questions[currentQuestion]?.context_image && (
                  <div className="mb-4 flex justify-center">
                    <img 
                      src={questions[currentQuestion].context_image} 
                      alt="Contexto"
                      className="rounded-lg max-h-60 object-contain"
                    />
                  </div>
                )}
                {questions[currentQuestion]?.question && (
                  <h3 className="text-lg text-center font-medium mb-4 text-pretty">
                    {questions[currentQuestion].question}
                  </h3>
                )}
                {questions[currentQuestion]?.scenario_description && (
                  <div className="mb-4 px-4 text-white/90">
                    <TypewriterText 
                      text={questions[currentQuestion].scenario_description}
                      className="text-base italic"
                    />
                  </div>
                )}
              </>
            )}
          </div>
        </GalaxyCard>
        
        {!showFeedback && questions[currentQuestion]?.options && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {questions[currentQuestion].options.map((option, index) => (
              <button 
                key={index} 
                onClick={() => handleAnswer(index)}
                className="bg-black/40 backdrop-blur-sm border border-white/10 rounded-lg p-4 text-left hover:bg-white/5 transition-colors"
              >
                <div className="flex items-center">
                  <span className="text-2xl mr-3">{option.emoji}</span>
                  <span>{option.text}</span>
                </div>
              </button>
            ))}
          </div>
        )}
        
        <div className="mt-8 flex justify-between">
          <CosmicButton variant="secondary" onClick={handleBack}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            {t('personalityTest.buttonBack')}
          </CosmicButton>
          
          <div className="flex-grow" />
        </div>
      </div>
    </div>
  );
};

export default PersonalityTest;
