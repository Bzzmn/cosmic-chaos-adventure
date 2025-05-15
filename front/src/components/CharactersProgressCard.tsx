import React from 'react';
import { Progress } from '@/components/ui/progress';
import { Users } from 'lucide-react';
import GalaxyCard from './GalaxyCard';
import NeonTitle from './NeonTitle';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { useTranslation } from 'react-i18next';
import TranslatedHTML from './TranslatedHTML';


// Mock API function to get character count
const getCharacterCount = () => {
  // For demonstration purposes, return a random number between 30-70
  return Math.floor(Math.random() * 40) + 30;
};

interface CharactersProgressCardProps {
  className?: string;
}

const CharactersProgressCard: React.FC<CharactersProgressCardProps> = ({ 
  className 
}) => {

  const { t } = useTranslation();
  const [characterCount, setCharacterCount] = React.useState(0);
  const goal = 100; // Changed from 500 to 100
  
  React.useEffect(() => {
    // Simulate API call to get character count
    const count = getCharacterCount();
    setCharacterCount(count);
  }, []);
  
  const progressPercentage = Math.min(Math.round((characterCount / goal) * 100), 100);
  
  const handleInfoClick = () => {
    toast.info("¡Los Desarrolladores Cósmicos te necesitan!", {
      description: "Crea tu personaje para desbloquear la próxima aventura.",
    });
  };
  
  return (
    <GalaxyCard 
      className={cn("text-center py-8 px-6 max-w-3xl mx-auto", className)}
      hasGlow 
      glowColor="green"
    >
      <div className="relative">
        <div className="space-y-8">
          <NeonTitle variant="green" size="lg" className="mb-2">
            {t('charactersProgressCard.title')}
          </NeonTitle>

          <div className="grid md:grid-cols-1 gap-6 mb-6">
            <div className="bg-black/30 rounded-lg overflow-hidden h-100 flex items-center justify-center border border-white/10">
              <div className="text-white/50 text-sm">
                <img src="/onstrike.webp" alt="Developers" className="w-full h-full object-cover" />
              </div>
            </div>
          </div>
          
          <TranslatedHTML
            i18nKey="charactersProgressCard.description"
            values={{ goal }}
            className="text-white/80 text-md md:text-xl"
          />
          
          <TranslatedHTML
            i18nKey="charactersProgressCard.strikeQuote"
            values={{ goal }}
            className="text-white/80 text-md md:text-xl"
          />
        </div>
        
        <div className="my-10 relative ">
          <div className="flex justify-between mb-4">
            <div 
              className="text-3xl font-bold text-cosmic-green"
              style={{ 
                textShadow: `0 0 10px rgba(132, 204, 22, 0.7), 0 0 20px rgba(132, 204, 22, 0.5)` 
              }}
            >
              {characterCount} {t('charactersProgressCard.characters')}
            </div>
            <div 
              className="text-2xl font-space text-cosmic-cyan"
              style={{ 
                textShadow: `0 0 8px rgba(6, 182, 212, 0.7), 0 0 16px rgba(6, 182, 212, 0.5)` 
              }}
            >
              {t('charactersProgressCard.goal')}: {goal}
            </div>
          </div>
          
          <Progress 
            value={progressPercentage} 
            className="h-4 bg-cosmic-dark/60 rounded-full" 
          />
        </div>
        
        <div className="bg-cosmic-dark/40 p-4 rounded-lg border border-cosmic-green/20 mt-4">
          <TranslatedHTML
            i18nKey="charactersProgressCard.nextUpdate"
            values={{ goal }}
            className="text-cosmic-green italic text-md md:text-xl"
          />
        </div>
      </div>
    </GalaxyCard>
  );
};

export default CharactersProgressCard;
