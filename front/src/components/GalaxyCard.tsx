
import React from 'react';
import { cn } from '@/lib/utils';

interface GalaxyCardProps {
  className?: string;
  children: React.ReactNode;
  hasGlow?: boolean;
  glowColor?: 'magenta' | 'cyan' | 'green';
  variant?: 'solid' | 'glass';
}

const GalaxyCard: React.FC<GalaxyCardProps> = ({
  className,
  children,
  hasGlow = false,
  glowColor = 'magenta',
  variant = 'glass',
  ...props
}) => {
  const glowColorMap = {
    magenta: 'bg-cosmic-magenta',
    cyan: 'bg-cosmic-cyan',
    green: 'bg-cosmic-green',
  };
  
  const variantStyles = {
    glass: 'bg-black/40 backdrop-blur-md',
    solid: 'bg-cosmic-dark',
  };
  
  return (
    <div className="relative">
      {hasGlow && (
        <div 
          className={cn(
            "absolute inset-0 -z-10 blur-xl opacity-20",
            glowColorMap[glowColor]
          )}
        />
      )}
      <div
        className={cn(
          "rounded-xl border border-white/10 p-6 overflow-hidden",
          variantStyles[variant],
          className
        )}
        {...props}
      >
        {children}
      </div>
    </div>
  );
};

export default GalaxyCard;
