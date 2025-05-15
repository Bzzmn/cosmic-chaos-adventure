
import React from "react";
import { useLocation, Link } from "react-router-dom";
import { useEffect } from "react";
import StarryBackground from '@/components/StarryBackground';
import NeonTitle from '@/components/NeonTitle';
import CosmicButton from '@/components/CosmicButton';

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error(
      "404 Error: User attempted to access non-existent route:",
      location.pathname
    );
  }, [location.pathname]);

  return (
    <div className="min-h-screen flex items-center justify-center relative">
      <StarryBackground />
      
      <div className="text-center z-10 p-8">
        <NeonTitle variant="cyan" size="xl" className="mb-6">
          404
        </NeonTitle>
        <p className="text-xl text-cosmic-magenta mb-8">
          Oops! Este sector galáctico no existe
        </p>
        <p className="mb-8 text-white/70 max-w-md mx-auto">
          Parece que te has aventurado demasiado lejos en el espacio.
          Esta coordenada cósmica no figura en nuestros mapas estelares.
        </p>
        <Link to="/">
          <CosmicButton variant="primary">
            Volver a la Estación Espacial
          </CosmicButton>
        </Link>
      </div>
    </div>
  );
};

export default NotFound;
