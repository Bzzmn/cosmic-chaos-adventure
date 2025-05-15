
import React, { useEffect, useRef } from 'react';

type Star = {
  x: number;
  y: number;
  size: 'small' | 'medium' | 'large';
  opacity: number;
  speed: number;
  twinkleSpeed: number;
  twinkleDelay: number;
};

const StarryBackground: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const starsRef = useRef<Star[]>([]);
  const requestRef = useRef<number>();
  
  // Generate random stars
  useEffect(() => {
    if (!containerRef.current) return;
    
    const generateStars = () => {
      const stars: Star[] = [];
      const starCount = Math.floor(window.innerWidth / 3); // Responsive star count
      
      for (let i = 0; i < starCount; i++) {
        stars.push({
          x: Math.random() * window.innerWidth,
          y: Math.random() * window.innerHeight,
          size: Math.random() < 0.7 ? 'small' : Math.random() < 0.9 ? 'medium' : 'large',
          opacity: 0.2 + Math.random() * 0.8,
          speed: 0.05 + Math.random() * 0.1,
          twinkleSpeed: 0.003 + Math.random() * 0.01,
          twinkleDelay: Math.random() * 100,
        });
      }
      
      starsRef.current = stars;
      renderStars();
    };
    
    const handleResize = () => {
      if (containerRef.current) {
        containerRef.current.innerHTML = '';
        generateStars();
      }
    };
    
    generateStars();
    window.addEventListener('resize', handleResize);
    
    return () => {
      window.removeEventListener('resize', handleResize);
      if (requestRef.current) {
        cancelAnimationFrame(requestRef.current);
      }
    };
  }, []);
  
  // Render stars into DOM
  const renderStars = () => {
    if (!containerRef.current) return;
    
    containerRef.current.innerHTML = '';
    
    starsRef.current.forEach(star => {
      const starElement = document.createElement('div');
      starElement.classList.add('star', `star-${star.size}`);
      starElement.style.left = `${star.x}px`;
      starElement.style.top = `${star.y}px`;
      starElement.style.opacity = star.opacity.toString();
      containerRef.current?.appendChild(starElement);
    });
  };
  
  return (
    <div 
      ref={containerRef} 
      className="fixed inset-0 z-[-1] overflow-hidden pointer-events-none"
      aria-hidden="true"
    />
  );
};

export default StarryBackground;
