import React, { ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface ButtonGlowProps {
  children: ReactNode;
  color?: 'magenta' | 'cyan' | 'green';
  className?: string;
}

const ButtonGlow: React.FC<ButtonGlowProps> = ({ 
  children, 
  color = 'cyan',
  className 
}) => {
  return (
    <div className={cn("relative", className)}>
      {/* Glow effect */}
      <div 
        className={cn(
          "absolute inset-0 blur-md rounded-full opacity-70", 
          "animate-slow-pulse",
          {
            "bg-cosmic-cyan": color === 'cyan',
            "bg-cosmic-magenta": color === 'magenta',
            "bg-cosmic-green": color === 'green',
          }
        )}
        style={{ transform: 'scale(1.15)' }} 
      />
      
      {/* Actual button */}
      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
};

export default ButtonGlow; 