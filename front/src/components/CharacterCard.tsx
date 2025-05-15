import React, { useState } from 'react';
import { cn } from '@/lib/utils';
import GalaxyCard from './GalaxyCard';
import { AspectRatio } from '@/components/ui/aspect-ratio';
import { Star, ChevronDown, ChevronUp } from 'lucide-react';
import { useTranslation } from 'react-i18next';

export interface CharacterStats {
  quantumCharisma: number;
  absurdityResistance: number;
  sarcasmLevel: number;
  timeWarping: number;
  cosmicLuck: number;
}

export interface Artifact {
  id: string;
  name: string;
  description: string;
  imageUrl?: string;
  effect: {
    stat: keyof CharacterStats;
    bonus: number;
    duration: number; // Number of adventures
  };
  isActive: boolean;
  remainingUses?: number;
}

export interface CharacterType {
  name: string;
  class: string;
  imageUrl: string;
  stats: CharacterStats;
  artifacts: (Artifact | null)[];
  experience?: number;
}

interface CharacterCardProps {
  character: CharacterType;
  className?: string;
  onActivateArtifact?: (index: number) => void;
}

const POINTS_PER_LEVEL = 10; // Every 10 points equals 1 level

const CharacterCard: React.FC<CharacterCardProps> = ({ 
  character, 
  className,
  onActivateArtifact
}) => {
  const [artifactsExpanded, setArtifactsExpanded] = useState(false);
  const { t } = useTranslation();
  
  const getStatLevel = (points: number) => {
    return Math.floor(points / POINTS_PER_LEVEL);
  };
  
  const getStatColor = (points: number) => {
    const level = getStatLevel(points);
    if (level > 8) return 'text-cosmic-green';
    if (level > 6) return 'text-cosmic-cyan';
    if (level > 4) return 'text-yellow-400';
    if (level > 2) return 'text-orange-500';
    return 'text-red-500';
  };
  
  const renderStatBar = (points: number) => {
    const level = getStatLevel(points);
    const progress = (points % POINTS_PER_LEVEL) / POINTS_PER_LEVEL;
    
    return (
      <div className="flex items-center space-x-2">
        <div className="flex-grow">
          <div className="h-2 w-full bg-gray-700 rounded-full overflow-hidden">
            <div 
              className={cn("h-full rounded-full", getStatColor(points))}
              style={{ width: `${progress * 100}%`, opacity: 0.7 }} 
            />
          </div>
        </div>
        <div className={cn("text-sm font-medium", getStatColor(points))}>
          {t('characterDetail.level')} {level}
        </div>
      </div>
    );
  };

  const renderLevelStars = (points: number) => {
    const level = getStatLevel(points);
    const stars = [];
    
    for (let i = 0; i < level; i++) {
      stars.push(
        <Star 
          key={i} 
          className={cn("h-3 w-3 fill-current", getStatColor(points))} 
        />
      );
    }
    
    return (
      <div className="flex">
        {stars.length === 0 ? (
          <span className="text-xs text-gray-400">{t('characterDetail.level')} 0</span>
        ) : (
          stars
        )}
      </div>
    );
  };

  return (
    <GalaxyCard 
      className={cn("max-w-4xl w-full mx-auto", className)}
      hasGlow
      glowColor="cyan"
    >
      <div className="flex flex-col md:flex-row gap-6">
        {/* Left Column: Character Image, Name, Experience and Description */}
        <div className="w-full md:w-2/5 flex flex-col">
          {/* Character Image with overlay text */}
          <div className="relative w-full rounded-lg overflow-hidden border-2 border-cosmic-cyan/30 shadow-lg shadow-cosmic-cyan/20">
            <AspectRatio ratio={1/1}>
              <div className="absolute inset-0 bg-gradient-to-t from-black to-transparent z-10" />
              <img 
                src={character.imageUrl || "/placeholder.svg"} 
                alt={character.name}
                className="w-full h-full object-cover"
              />
              <div className="absolute bottom-2 left-0 right-0 text-center z-20">
                <h2 className="text-2xl font-bold text-white text-shadow-md px-2">{character.name}</h2>
                <p className="text-cosmic-cyan font-medium text-shadow-sm">{character.class}</p>
              </div>
            </AspectRatio>
          </div>
          
          {/* Character Experience */}
          {character.experience !== undefined && (
            <div className="bg-black/60 backdrop-blur-sm my-4 p-2 rounded border border-cosmic-green/20">
              <div className="flex justify-between items-center">
                <p className="text-sm text-cosmic-green/70">{t('characterDetail.experience')}:</p>
                <p className="text-sm font-bold text-cosmic-green">{character.experience} XP</p>
              </div>
            </div>
          )}
          
          {/* Character Description */}
          <div className="mt-2 p-3 bg-cosmic-dark/40 rounded-lg border border-cosmic-magenta/20">
            <p className="text-sm text-white/90 italic">
              {t('latestCharacters.characterDescription')}
            </p>
          </div>
        </div>
        
        {/* Right Column: Character Stats and Artifacts */}
        <div className="flex-1 flex flex-col">
          {/* Character Stats */}
          <div className="space-y-3 mb-6">
            <h3 className="text-sm font-semibold mb-2 text-cosmic-cyan">{t('characterDetail.stats')}</h3>
            
            <div className="bg-black/20 p-3 rounded-md border border-white/5 hover:border-cosmic-cyan/30 transition-colors">
              <div className="flex justify-between mb-1">
                <span className="text-sm font-semibold">{t('personalityTest.traits.quantum_charisma')}</span>
                {renderLevelStars(character.stats.quantumCharisma)}
              </div>
              {renderStatBar(character.stats.quantumCharisma)}
            </div>
            
            <div className="bg-black/20 p-3 rounded-md border border-white/5 hover:border-cosmic-cyan/30 transition-colors">
              <div className="flex justify-between mb-1">
                <span className="text-sm font-semibold">{t('personalityTest.traits.absurdity_resistance')}</span>
                {renderLevelStars(character.stats.absurdityResistance)}
              </div>
              {renderStatBar(character.stats.absurdityResistance)}
            </div>
            
            <div className="bg-black/20 p-3 rounded-md border border-white/5 hover:border-cosmic-cyan/30 transition-colors">
              <div className="flex justify-between mb-1">
                <span className="text-sm font-semibold">{t('personalityTest.traits.sarcasm_level')}</span>
                {renderLevelStars(character.stats.sarcasmLevel)}
              </div>
              {renderStatBar(character.stats.sarcasmLevel)}
            </div>
            
            <div className="bg-black/20 p-3 rounded-md border border-white/5 hover:border-cosmic-cyan/30 transition-colors">
              <div className="flex justify-between mb-1">
                <span className="text-sm font-semibold">{t('personalityTest.traits.time_warping')}</span>
                {renderLevelStars(character.stats.timeWarping)}
              </div>
              {renderStatBar(character.stats.timeWarping)}
            </div>
            
            <div className="bg-black/20 p-3 rounded-md border border-white/5 hover:border-cosmic-cyan/30 transition-colors">
              <div className="flex justify-between mb-1">
                <span className="text-sm font-semibold">{t('personalityTest.traits.cosmic_luck')}</span>
                {renderLevelStars(character.stats.cosmicLuck)}
              </div>
              {renderStatBar(character.stats.cosmicLuck)}
            </div>
          </div>
          
          {/* Artifact Slots as Collapsible */}
          <div className="border-t border-white/10 pt-4">
            <button 
              onClick={() => setArtifactsExpanded(!artifactsExpanded)}
              className="w-full flex items-center justify-between mb-2 text-left bg-black/20 p-2 rounded hover:bg-black/30 transition-colors"
            >
              <h3 className="text-sm font-semibold">{t('characterDetail.artifacts')}</h3>
              {artifactsExpanded ? 
                <ChevronUp className="h-4 w-4 text-cosmic-cyan" /> : 
                <ChevronDown className="h-4 w-4 text-cosmic-cyan" />
              }
            </button>
            
            {artifactsExpanded && (
              <div className="grid grid-cols-2 gap-2 mt-3 animate-fadeIn">
                {[0, 1, 2, 3].map((index) => (
                  <div 
                    key={index}
                    onClick={() => {
                      if (character.artifacts[index] && onActivateArtifact) {
                        onActivateArtifact(index);
                      }
                    }}
                    className={cn(
                      "border rounded-md aspect-square p-2 flex flex-col items-center justify-center text-center",
                      character.artifacts[index] 
                        ? "border-cosmic-cyan/50 bg-black/30 cursor-pointer hover:bg-black/50 transition-colors" 
                        : "border-white/10 bg-black/10"
                    )}
                  >
                    {character.artifacts[index] ? (
                      <>
                        <div className="mb-1 text-xs font-medium text-cosmic-cyan truncate w-full">
                          {character.artifacts[index]?.name}
                        </div>
                        {character.artifacts[index]?.isActive ? (
                          <span className="text-[9px] bg-cosmic-green/20 text-cosmic-green px-1 rounded">
                            {t('characterDetail.active')}
                          </span>
                        ) : (
                          <span className="text-[9px] text-white/40">
                            {t('characterDetail.clickToActivate')}
                          </span>
                        )}
                      </>
                    ) : (
                      <span className="text-xs text-white/30">{t('characterDetail.empty')}</span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </GalaxyCard>
  );
};

export default CharacterCard;
