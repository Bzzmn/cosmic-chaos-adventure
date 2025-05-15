
import React from 'react';
import { cn } from '@/lib/utils';

interface NeonTitleProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'magenta' | 'cyan' | 'green';
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

const NeonTitle: React.FC<NeonTitleProps> = ({
  children,
  className,
  variant = 'magenta',
  size = 'lg',
}) => {
  const variantClasses = {
    magenta: 'text-cosmic-magenta shadow-cosmic-magenta',
    cyan: 'text-cosmic-cyan shadow-cosmic-cyan',
    green: 'text-cosmic-green shadow-cosmic-green',
  };
  
  const sizeClasses = {
    sm: 'text-xl md:text-2xl',
    md: 'text-2xl md:text-3xl',
    lg: 'text-3xl md:text-4xl',
    xl: 'text-4xl md:text-6xl',
  };

  return (
    <h1 
      className={cn(
        'font-space font-bold tracking-wider',
        sizeClasses[size],
        variantClasses[variant],
        className
      )}
      style={{ 
        textShadow: `0 0 5px currentColor, 0 0 10px currentColor, 0 0 20px currentColor` 
      }}
    >
      {children}
    </h1>
  );
};

export default NeonTitle;
