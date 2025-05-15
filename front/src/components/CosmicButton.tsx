
import React from 'react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

interface CosmicButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'accent';
  size?: 'sm' | 'md' | 'lg';
  hasGlow?: boolean;
  children: React.ReactNode;
}

const CosmicButton: React.FC<CosmicButtonProps> = ({
  className,
  variant = 'primary',
  size = 'md',
  hasGlow = true,
  children,
  ...props
}) => {
  const variantStyles = {
    primary: 'bg-cosmic-magenta hover:bg-opacity-90 text-white',
    secondary: 'bg-cosmic-cyan hover:bg-opacity-90 text-white',
    accent: 'bg-cosmic-green hover:bg-opacity-90 text-white',
  };
  
  const sizeStyles = {
    sm: 'text-sm px-4 py-1',
    md: 'text-base px-6 py-2',
    lg: 'text-lg px-8 py-3',
  };
  
  const glowColors = {
    primary: 'bg-cosmic-magenta',
    secondary: 'bg-cosmic-cyan',
    accent: 'bg-cosmic-green',
  };
  
  return (
    <div className="relative group">
      {hasGlow && (
        <div className={cn(
          "absolute inset-0 blur-xl opacity-30 group-hover:opacity-50 transition-opacity",
          glowColors[variant]
        )} />
      )}
      <Button
        className={cn(
          "relative font-space font-bold transition-all duration-300 hover:scale-105 active:scale-95",
          variantStyles[variant],
          sizeStyles[size],
          className
        )}
        {...props}
      >
        {children}
      </Button>
    </div>
  );
};

export default CosmicButton;
