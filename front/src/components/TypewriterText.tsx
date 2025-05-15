
import React, { useState, useEffect, useRef } from 'react';
import { cn } from '@/lib/utils';

interface TypewriterTextProps {
  text: string;
  speed?: number;
  className?: string;
  onComplete?: () => void;
}

const TypewriterText: React.FC<TypewriterTextProps> = ({
  text,
  speed = 40,
  className,
  onComplete,
}) => {
  const [displayedText, setDisplayedText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const completed = useRef(false);
  
  useEffect(() => {
    // Reset when text changes
    setDisplayedText('');
    setCurrentIndex(0);
    completed.current = false;
  }, [text]);
  
  useEffect(() => {
    if (currentIndex < text.length) {
      const timeout = setTimeout(() => {
        setDisplayedText(prev => prev + text[currentIndex]);
        setCurrentIndex(prev => prev + 1);
      }, speed);
      
      return () => clearTimeout(timeout);
    } else if (!completed.current) {
      completed.current = true;
      onComplete?.();
    }
  }, [currentIndex, text, speed, onComplete]);
  
  return (
    <span className={cn('', className)}>
      {displayedText}
      {currentIndex < text.length && (
        <span className="opacity-0">.</span>
      )}
    </span>
  );
};

export default TypewriterText;
