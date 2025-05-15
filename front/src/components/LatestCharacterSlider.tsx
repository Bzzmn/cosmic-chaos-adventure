import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useLatestCharacters, LatestCharacter } from '@/hooks/useLatestCharacters';
import { ArrowLeft, ArrowRight, ExternalLink } from 'lucide-react';
import GalaxyCard from './GalaxyCard';
import { cn } from '@/lib/utils';

interface LatestCharacterSliderProps {
  className?: string;
}

const POINTS_PER_LEVEL = 10; // Cada 10 puntos es un nivel

const LatestCharacterSlider: React.FC<LatestCharacterSliderProps> = ({ 
  className 
}) => {
  const { t } = useTranslation();
  const { characters, loading, error } = useLatestCharacters();
  const [currentIndex, setCurrentIndex] = useState(0);
  const navigate = useNavigate();
  
  const handlePrevious = () => {
    if (characters.length === 0) return;
    setCurrentIndex((prev) => (prev === 0 ? characters.length - 1 : prev - 1));
  };
  
  const handleNext = () => {
    if (characters.length === 0) return;
    setCurrentIndex((prev) => (prev === characters.length - 1 ? 0 : prev + 1));
  };
  
  const handleViewCharacter = (character: LatestCharacter) => {
    // Navigate to the character detail page with the character data
    navigate(`/character/${character.address}`, { state: { character } });
  };

  // Función para calcular el nivel a partir de puntos
  const getStatLevel = (points: number) => {
    return Math.floor(points / POINTS_PER_LEVEL);
  };
  
  // Función para obtener el color basado en el nivel
  const getStatColor = (points: number) => {
    const level = getStatLevel(points);
    if (level > 8) return 'bg-cosmic-green text-cosmic-green';
    if (level > 6) return 'bg-cosmic-cyan text-cosmic-cyan';
    if (level > 4) return 'bg-yellow-400 text-yellow-400';
    if (level > 2) return 'bg-orange-500 text-orange-500';
    return 'bg-red-500 text-red-500';
  };

  // Obtener solo el color del texto para el nivel
  const getLevelTextColor = (points: number) => {
    const colors = getStatColor(points).split(' ')[1];
    return colors || 'text-white';
  };
  
  if (loading) {
    return (
      <div className={cn("max-w-4xl mx-auto py-8", className)}>
        <GalaxyCard className="p-8 text-center">
          <div className="flex items-center justify-center space-x-2">
            <div className="w-4 h-4 rounded-full bg-cosmic-cyan animate-pulse" />
            <div className="w-4 h-4 rounded-full bg-cosmic-magenta animate-pulse delay-150" />
            <div className="w-4 h-4 rounded-full bg-cosmic-green animate-pulse delay-300" />
          </div>
          <p className="text-cosmic-cyan mt-4">{t('latestCharacters.loading')}</p>
        </GalaxyCard>
      </div>
    );
  }
  
  if (error || characters.length === 0) {
    return (
      <div className={cn("max-w-4xl mx-auto py-8", className)}>
        <GalaxyCard className="p-8 text-center">
          <p className="text-cosmic-magenta">
            {error || t('latestCharacters.noCharacters')}
          </p>
        </GalaxyCard>
      </div>
    );
  }
  
  const currentCharacter = characters[currentIndex];
  
  return (
    <div className={cn("max-w-4xl mx-auto py-8", className)}>
      <h3 className="text-2xl font-space font-medium text-cosmic-cyan text-center mb-6">
        {t('latestCharacters.title')}
      </h3>
      
      <div className="relative pb-6">
        <GalaxyCard 
          hasGlow 
          glowColor="magenta"
          className="p-6 transition-all duration-300"
        >
          <div className="flex flex-col md:flex-row gap-8">
            {/* Character Image and Info Column */}
            <div className="w-full md:w-2/5 flex flex-col">
              {/* Character Image - Made Larger */}
              <div className="relative w-full aspect-square rounded-lg overflow-hidden border-2 border-cosmic-magenta/30 shadow-lg shadow-cosmic-magenta/20">
                <div className="absolute inset-0 bg-gradient-to-t from-black to-transparent z-10" />
                <img 
                  src={currentCharacter.imageUrl} 
                  alt={currentCharacter.name}
                  className="w-full h-full object-cover"
                />
                <div className="absolute bottom-2 left-0 right-0 text-center z-20">
                  <h4 className="text-2xl font-bold text-white text-shadow-md px-2">
                    {currentCharacter.name}
                  </h4>
                  <p className="text-cosmic-cyan font-medium text-shadow-sm">
                    {currentCharacter.class}
                  </p>
                </div>
              </div>
              
              {/* NFT Address */}
              <div className="bg-black/60 backdrop-blur-sm mt-4 p-2 rounded border border-cosmic-cyan/20 break-all">
                <p className="text-xs mb-1 text-cosmic-cyan/70">{t('latestCharacters.nftAddress')}:</p>
                <p className="text-xs text-cosmic-cyan font-mono">
                  {currentCharacter.address}
                </p>
              </div>
              
              {/* Character Description - Added */}
              <div className="mt-4 p-3 bg-cosmic-dark/40 rounded-lg border border-cosmic-magenta/20">
                <p className="text-sm text-white/90 italic">
                  {t('latestCharacters.characterDescription')}
                </p>
              </div>
            </div>
            
            {/* Character Stats Column */}
            <div className="flex-1 flex flex-col">
              <div className="flex-1 space-y-4">
                {Object.entries(currentCharacter.stats).map(([key, value]) => {
                  const formattedKey = key
                    .replace(/([A-Z])/g, ' $1')
                    .replace(/^./, str => str.toUpperCase());
                  
                  // Calcular el nivel y progreso
                  const level = getStatLevel(value);
                  const progress = (value % POINTS_PER_LEVEL) / POINTS_PER_LEVEL * 100;
                  const levelColor = getLevelTextColor(value);
                  
                  return (
                    <div key={key} className="bg-black/20 p-3 rounded-md border border-white/5 hover:border-cosmic-cyan/30 transition-colors">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium text-sm">{formattedKey}</span>
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-white/70">{t('latestCharacters.level')}:</span>
                          <span className={`font-bold text-lg ${levelColor}`}>{level}</span>
                        </div>
                      </div>
                      
                      <div className="h-3 w-full bg-gray-700 rounded-full overflow-hidden">
                        <div 
                          className={cn("h-full rounded-full", getStatColor(value).split(' ')[0])}
                          style={{ width: `${progress}%`, opacity: 0.8 }} 
                        />
                      </div>
                      
                      <div className="flex justify-between mt-2 text-xs">
                        <span className="text-white/50">
                          {value} pts
                        </span>
                        <span className="text-white/50">
                          {level < 10 ? `${POINTS_PER_LEVEL * (level + 1) - value} pts to lvl ${level + 1}` : 'Max Level'}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
              
            </div>
          </div>
        </GalaxyCard>
        
        {/* Pagination dots */}
        <div className="flex justify-center mt-4 gap-2">
          {characters.map((_, index) => (
            <button 
              key={index}
              onClick={() => setCurrentIndex(index)}
              className={cn(
                "w-3 h-3 rounded-full transition-all",
                index === currentIndex 
                  ? "bg-cosmic-magenta scale-110" 
                  : "bg-cosmic-magenta/30 hover:bg-cosmic-magenta/50"
              )}
              aria-label={`Go to character ${index + 1}`}
            />
          ))}
        </div>
        
        {/* Navigation arrows */}
        <button 
          onClick={handlePrevious}
          className="absolute top-1/2 -left-3 transform -translate-y-1/2 w-10 h-10 rounded-full bg-cosmic-dark border border-cosmic-cyan/30 flex items-center justify-center hover:bg-cosmic-cyan/20 transition-colors z-20"
          aria-label={t('latestCharacters.previousCharacter')}
        >
          <ArrowLeft className="h-5 w-5 text-cosmic-cyan" />
        </button>
        
        <button 
          onClick={handleNext}
          className="absolute top-1/2 -right-3 transform -translate-y-1/2 w-10 h-10 rounded-full bg-cosmic-dark border border-cosmic-cyan/30 flex items-center justify-center hover:bg-cosmic-cyan/20 transition-colors z-20"
          aria-label={t('latestCharacters.nextCharacter')}
        >
          <ArrowRight className="h-5 w-5 text-cosmic-cyan" />
        </button>
      </div>
    </div>
  );
};

export default LatestCharacterSlider; 