import React from 'react';
import { useTranslation } from 'react-i18next';
import { Coffee, LucideIcon, Rocket, Sparkles } from 'lucide-react';
import GalaxyCard from './GalaxyCard';

// Definir la interfaz para una tarjeta de característica
interface FeatureCard {
  icon: LucideIcon;
  colorClass: string;
  titleKey: string;
  descriptionKey: string;
}

interface FeatureCardsProps {
  className?: string;
}

const FeatureCards: React.FC<FeatureCardsProps> = ({ className = '' }) => {
  const { t } = useTranslation();

  // Definir las características
  const features: FeatureCard[] = [
    {
      icon: Rocket,
      colorClass: 'bg-cosmic-magenta/20 text-cosmic-magenta',
      titleKey: 'featureCards.cosmicAdventure.title',
      descriptionKey: 'featureCards.cosmicAdventure.description'
    },
    {
      icon: Sparkles,
      colorClass: 'bg-cosmic-cyan/20 text-cosmic-cyan',
      titleKey: 'featureCards.uniqueCharacters.title',
      descriptionKey: 'featureCards.uniqueCharacters.description'
    },
    {
      icon: Coffee,
      colorClass: 'bg-cosmic-green/20 text-cosmic-green',
      titleKey: 'featureCards.multiverse.title',
      descriptionKey: 'featureCards.multiverse.description'
    }
  ];

  return (
    <div className={`grid grid-cols-1 md:grid-cols-3 gap-6 mt-16 ${className}`}>
      {features.map((feature, index) => {
        const Icon = feature.icon;
        
        return (
          <GalaxyCard 
            key={index} 
            className="transform hover:scale-105 transition-transform"
          >
            <div className="flex flex-col items-center text-center p-4">
              <div className={`w-12 h-12 flex items-center justify-center ${feature.colorClass.split(' ')[0]} rounded-full mb-4`}>
                <Icon className={`h-6 w-6 ${feature.colorClass.split(' ')[1]}`} />
              </div>
              <h3 className="font-space font-medium text-lg mb-2">
                {t(feature.titleKey)}
              </h3>
              <p className="text-sm text-white/70">
                {t(feature.descriptionKey)}
              </p>
            </div>
          </GalaxyCard>
        );
      })}
    </div>
  );
};

export default FeatureCards; 