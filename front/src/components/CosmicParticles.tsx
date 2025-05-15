
import React, { useEffect, useRef } from 'react';

type Particle = {
  x: number;
  y: number;
  size: number;
  color: string;
  speedX: number;
  speedY: number;
  life: number;
  maxLife: number;
};

const CosmicParticles: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const particlesRef = useRef<Particle[]>([]);
  const animationRef = useRef<number>();
  
  const colors = [
    '#D946EF', // magenta
    '#06B6D4', // cyan
    '#84CC16', // green
  ];
  
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    const resizeCanvas = () => {
      if (canvas) {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
      }
    };
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    const addParticle = (x: number, y: number) => {
      const color = colors[Math.floor(Math.random() * colors.length)];
      const size = 3 + Math.random() * 5;
      const speedX = (Math.random() - 0.5) * 1;
      const speedY = (Math.random() - 0.5) * 1;
      const maxLife = 100 + Math.random() * 100;
      
      particlesRef.current.push({
        x,
        y,
        size,
        color,
        speedX,
        speedY,
        life: 0,
        maxLife
      });
    };
    
    // Spawn particles at random
    const spawnInterval = setInterval(() => {
      addParticle(
        Math.random() * canvas.width,
        Math.random() * canvas.height
      );
    }, 500);
    
    // Animate particles
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      particlesRef.current.forEach((p, i) => {
        p.x += p.speedX;
        p.y += p.speedY;
        p.life += 1;
        
        const alpha = 1 - (p.life / p.maxLife);
        
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `${p.color}${Math.floor(alpha * 255).toString(16).padStart(2, '0')}`;
        ctx.fill();
        
        if (p.life >= p.maxLife) {
          particlesRef.current.splice(i, 1);
        }
      });
      
      animationRef.current = requestAnimationFrame(animate);
    };
    
    animate();
    
    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
      clearInterval(spawnInterval);
      window.removeEventListener('resize', resizeCanvas);
    };
  }, []);
  
  return (
    <canvas 
      ref={canvasRef} 
      className="fixed inset-0 z-[-1] opacity-50 pointer-events-none"
      aria-hidden="true"
    />
  );
};

export default CosmicParticles;
