import React from 'react';
import { useTranslation } from 'react-i18next';
import { Award, BookOpen, Dices, LucideIcon } from 'lucide-react';

// Definir la interface para un paso de aventura
interface AdventureStep {
  icon: LucideIcon;
  colorClass: string;
  titleKey: string;
  descriptionKey: string;
}

interface AdventureStepsProps {
  className?: string;
}

const AdventureSteps: React.FC<AdventureStepsProps> = ({ className = '' }) => {
  const { t } = useTranslation('adventure');

  // Definir los pasos de la aventura
  const steps: AdventureStep[] = [
    {
      icon: Dices,
      colorClass: 'bg-cosmic-magenta/20 text-cosmic-magenta',
      titleKey: 'steps.step1.title',
      descriptionKey: 'steps.step1.description',
    },
    {
      icon: BookOpen,
      colorClass: 'bg-cosmic-cyan/20 text-cosmic-cyan',
      titleKey: 'steps.step2.title',
      descriptionKey: 'steps.step2.description',
    },
    {
      icon: Award,
      colorClass: 'bg-cosmic-green/20 text-cosmic-green',
      titleKey: 'steps.step3.title',
      descriptionKey: 'steps.step3.description',
    },
  ];

  return (
    <div className={`py-10 ${className}`}>
      <h3 className="text-2xl font-space font-medium text-cosmic-green mb-8">
        {t('steps.title')}
      </h3>

      <div className="flex flex-col md:flex-row gap-3 justify-center items-center md:items-start mb-10 px-4">
        {steps.map((step, index) => {
          const Icon = step.icon;
          
          return (
            <React.Fragment key={index}>
              {/* Step card */}
              <div className="flex flex-col items-center max-w-[200px]">
                <div className={`w-14 h-14 ${step.colorClass.split(' ')[0]} rounded-full flex items-center justify-center mb-3`}>
                  <Icon className={`h-7 w-7 ${step.colorClass.split(' ')[1]}`} />
                </div>
                <h4 className="font-space font-medium mb-1">
                  {t(step.titleKey, `Step ${index + 1}`)}
                </h4>
                <p className="text-center text-sm text-white/70">
                  {t(step.descriptionKey)}
                </p>
              </div>

              {/* Separator line (not for the last step) */}
              {index < steps.length - 1 && (
                <div className="hidden md:block w-10 h-0.5 bg-cosmic-cyan/30 my-8" />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};

export default AdventureSteps; 