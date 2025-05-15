import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { useTranslation } from 'react-i18next';
import StarryBackground from '@/components/StarryBackground';
import CosmicParticles from '@/components/CosmicParticles';
import CosmicButton from '@/components/CosmicButton';
import NeonTitle from '@/components/NeonTitle';
import CharacterCard, { CharacterType, CharacterStats, Artifact } from '@/components/CharacterCard';
import { ArrowLeft, ArrowRight, Star } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { usePersonalityStore } from '@/lib/store';
import { usePersonality } from '@/hooks/usePersonality';
import { useCharacters } from '@/hooks/useCharacters';

// Array of absurd character classes in Spanish
const characterClassesES = [
  "Camarero Cuántico",
  "Poeta del Caos",
  "Abogado Interdimensional",
  "Buceador de Agujeros Negros",
  "Crítico de Restaurantes Extintos",
  "Piloto de Bebidas",
  "Psicólogo de Paradojas",
  "Contador de Estrellas",
  "Bailarín de Cometas",
  "DJ de Ruido Cósmico",
  "Embajador del Absurdo",
  "Coleccionista de Momentos",
];

// Array of absurd character classes in English
const characterClassesEN = [
  "Quantum Waiter",
  "Chaos Poet",
  "Interdimensional Lawyer",
  "Black Hole Diver",
  "Extinct Restaurant Critic",
  "Beverage Pilot",
  "Paradox Psychologist",
  "Star Counter",
  "Comet Dancer",
  "Cosmic Noise DJ",
  "Ambassador of Absurdity",
  "Moment Collector",
];

// Array of first name parts
const firstNames = [
  "Zap", "Blip", "Zort", "Bleep", "Frood", "Zax", "Quib", "Plim", "Vorp", 
  "Nib", "Glib", "Trax", "Zilch", "Blob", "Quirk", "Glip", "Flib", "Zim",
];

// Array of second name parts
const lastNames = [
  "tron", "blat", "glot", "frob", "wack", "oid", "zoid", "ston", "quax",
  "blob", "pop", "wiz", "fuzz", "bop", "plex", "ton", "tastic", "zap",
];

const placeholderImageUrl = "/placeholder.svg";
const characterImageUrls = [
  "http://localhost:8080/images/zortblob.webp",
  "http://localhost:8080/images/blopzoid.webp",
  "http://localhost:8080/images/quirkton.webp",
];

const POINTS_PER_OPTION_VALUE = 10; // Each option value (1-4) gives 10-40 points

const CharacterCreation: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { t, i18n } = useTranslation();
  const { user } = useAuth();
  const [isGenerating, setIsGenerating] = useState<boolean>(true);
  const [character, setCharacter] = useState<CharacterType | null>(null);
  
  // Get the current language
  const currentLanguage = i18n.language;
  // Choose the character classes based on the current language
  const characterClasses = currentLanguage === 'es' ? characterClassesES : characterClassesEN;
  
  // Usar el Zustand store
  const { questions, answers, results, resetStore } = usePersonalityStore();
  
  // Hooks personalizados
  const { results: apiResults } = usePersonality(user?.id);
  const { createCharacter } = useCharacters();
  
  useEffect(() => {
    // Si no tenemos respuestas en el store, volvemos al test
    if (answers.length === 0 && !apiResults) {
      navigate("/personality");
      return;
    }
    
    const generateCharacter = async () => {
      setIsGenerating(true);
      
      // Simular tiempo de carga
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Usamos resultados del API o calculamos basados en las respuestas
      let stats: CharacterStats;
      
      if (apiResults && apiResults.stats) {
        // Si tenemos resultados del API, los usamos
        stats = {
          quantumCharisma: apiResults.stats.quantum_charisma,
          absurdityResistance: apiResults.stats.absurdity_resistance,
          sarcasmLevel: apiResults.stats.sarcasm_level,
          timeWarping: apiResults.stats.time_warping,
          cosmicLuck: apiResults.stats.cosmic_luck,
        };
      } else {
        // Calcular estadísticas basadas en respuestas guardadas
        stats = {
          quantumCharisma: 0,
          absurdityResistance: 0,
          sarcasmLevel: 0,
          timeWarping: 0,
          cosmicLuck: 0,
        };
        
        // Procesar respuestas para modificar estadísticas
        answers.forEach((answerIndex: number, questionIndex: number) => {
          if (questions[questionIndex] && questions[questionIndex].options[answerIndex]) {
            const option = questions[questionIndex].options[answerIndex];
            
            // Aplicar los efectos a las estadísticas
            Object.entries(option.effect).forEach(([stat, value]) => {
              switch(stat) {
                case 'quantum_charisma':
                  stats.quantumCharisma += value * POINTS_PER_OPTION_VALUE;
                  break;
                case 'absurdity_resistance':
                  stats.absurdityResistance += value * POINTS_PER_OPTION_VALUE;
                  break;
                case 'sarcasm_level':
                  stats.sarcasmLevel += value * POINTS_PER_OPTION_VALUE;
                  break;
                case 'time_warping':
                  stats.timeWarping += value * POINTS_PER_OPTION_VALUE;
                  break;
                case 'cosmic_luck':
                  stats.cosmicLuck += value * POINTS_PER_OPTION_VALUE;
                  break;
              }
            });
          }
        });
      }
      
      // Generar nombre aleatorio
      const firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
      const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
      const name = `${firstName}${lastName}`;
      
      // Generar clase aleatoria
      const characterClass = characterClasses[Math.floor(Math.random() * characterClasses.length)];
      
      // Obtener imagen aleatoria del array
      const imageUrl = characterImageUrls[Math.floor(Math.random() * characterImageUrls.length)];
      
      // Crear personaje con slots de artefactos vacíos
      const newCharacter: CharacterType = {
        name,
        class: characterClass,
        imageUrl,
        stats,
        artifacts: [null, null, null, null],
        experience: 0,
      };
      
      setCharacter(newCharacter);
      setIsGenerating(false);
      
      toast.success(t('characterCreation.successToast'), {
        icon: <Star className="h-5 w-5" />,
      });
    };
    
    generateCharacter();
  }, [apiResults, answers, questions, navigate, user, t, characterClasses]);
  
  const handleBack = () => {
    navigate("/personality");
  };
  
  const handleContinue = () => {
    if (character && user) {
      // Si el usuario está autenticado y tenemos un personaje, lo guardamos en la BD
      createCharacter({
        name: character.name,
        character_class: character.class,
        image_url: character.imageUrl,
        stats: {
          quantumCharisma: character.stats.quantumCharisma,
          absurdityResistance: character.stats.absurdityResistance,
          sarcasmLevel: character.stats.sarcasmLevel,
          timeWarping: character.stats.timeWarping,
          cosmicLuck: character.stats.cosmicLuck
        },
        user_id: user.id
      })
        .then(() => {
          // Limpiar el store después de guardar
          resetStore();
          // Navegar a la aventura con indicación de que es la primera aventura
          navigate("/adventure", { 
            state: { 
              character,
              fromCharacterCreation: true
            } 
          });
        })
        .catch((error) => {
          console.error("Error al guardar el personaje:", error);
          toast.error(t('characterCreation.errorSaving'));
        });
    } else {
      // Si no hay usuario autenticado, solo navegamos
      navigate("/adventure", { 
        state: { 
          character,
          fromCharacterCreation: true
        } 
      });
    }
  };
  
  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center px-4 py-20">
      <StarryBackground />
      <CosmicParticles />
      
      <div className="max-w-4xl w-full mx-auto z-10">
        <div className="mb-8 text-center">
          <NeonTitle variant="green" size="lg">{t('characterCreation.title')}</NeonTitle>
          <p className="text-white/70 mt-2">
            {t('characterCreation.subtitle')}
          </p>
        </div>
        
        <div className="flex flex-col items-center justify-center min-h-[500px]">
          {isGenerating ? (
            <div className="text-center p-10">
              <div className="relative w-20 h-20 mx-auto mb-4">
                <div className="absolute inset-0 rounded-full border-4 border-t-cosmic-magenta border-r-cosmic-cyan border-b-cosmic-green border-l-transparent animate-cosmic-spin"></div>
                <Star className="absolute inset-0 m-auto h-8 w-8 text-white animate-pulse-glow" />
              </div>
              <p className="text-lg text-white/80">{t('characterCreation.generating')}</p>
            </div>
          ) : character ? (
            <div className="animate-[scale-in_0.5s_ease_forwards]">
              <CharacterCard character={character} />
            </div>
          ) : (
            <div className="text-center">
              <p className="text-lg text-red-400">{t('characterCreation.error')}</p>
              <p className="mt-2">{t('characterCreation.tryAgain')}</p>
            </div>
          )}
        </div>
        
        <div className="mt-8 flex justify-between">
          <CosmicButton variant="secondary" onClick={handleBack}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            {t('common.back')}
          </CosmicButton>
          
          {character && !isGenerating && (
            <CosmicButton variant="primary" onClick={handleContinue}>
              {t('characterCreation.startAdventure')}
              <ArrowRight className="ml-2 h-4 w-4" />
            </CosmicButton>
          )}
        </div>
      </div>
    </div>
  );
};

export default CharacterCreation;
