import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { useTranslation } from 'react-i18next';
import StarryBackground from '@/components/StarryBackground';
import CosmicParticles from '@/components/CosmicParticles';
import CosmicButton from '@/components/CosmicButton';
import NeonTitle from '@/components/NeonTitle';
import GalaxyCard from '@/components/GalaxyCard';
import TypewriterText from '@/components/TypewriterText';
import CharacterCard, { CharacterType } from '@/components/CharacterCard';
import CharactersProgressCard from '@/components/CharactersProgressCard';
import LatestCharacterSlider from '@/components/LatestCharacterSlider';
import { Sparkles, Coffee, BookOpen, Dices, Award, Rocket } from 'lucide-react';
import { Dialog, DialogContent } from '@/components/ui/dialog';
import { AspectRatio } from '@/components/ui/aspect-ratio';
import { useAuth } from '@/hooks/useAuth';
import ButtonGlow from '@/components/ButtonGlow';
import TranslatedHTML from '@/components/TranslatedHTML';
import AdventureSteps from '@/components/AdventureSteps';
import FeatureCards from '@/components/FeatureCards';

const AdventureQuotes = [
  "¡Enfréntate a un camarero de cinco cabezas en el Bar Milliways!",
  "Discute sobre filosofía con un colchón inteligente de Squornshellous Zeta",
  "Huye de la Bestia Voraz de Traal sin una toalla",
  "Negocia con un Vogon para evitar que lea su poesía",
  "Descubre el significado de la vida, el universo y todo lo demás"
];

const Landing: React.FC = () => {
  const { t } = useTranslation();
  const [showQuote, setShowQuote] = useState(false);
  const [quoteIndex, setQuoteIndex] = useState(0);
  const [typingComplete, setTypingComplete] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  
  // Sample character for preview
  const sampleCharacter: CharacterType = {
    name: "Zaphod Tralfamadoriano",
    class: "Astronauta Absurdo",
    imageUrl: "/placeholder.svg",
    stats: {
      quantumCharisma: 85,
      absurdityResistance: 70,
      sarcasmLevel: 92,
      timeWarping: 60,
      cosmicLuck: 78
    },
    artifacts: [
      {
        id: "artifact-1",
        name: "Toalla Multiversal",
        description: "Una toalla que sabe dónde está en el universo",
        effect: {
          stat: "cosmicLuck",
          bonus: 10,
          duration: 3
        },
        isActive: true
      },
      null,
      null,
      null
    ]
  };
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setShowQuote(true);
    }, 1000);
    
    return () => clearTimeout(timer);
  }, []);
  
  useEffect(() => {
    if (typingComplete && quoteIndex < AdventureQuotes.length - 1) {
      const timer = setTimeout(() => {
        setQuoteIndex(prev => prev + 1);
        setTypingComplete(false);
      }, 2000);
      
      return () => clearTimeout(timer);
    }
  }, [typingComplete, quoteIndex]);
  
  const handleCheckGalaxy = () => {
    toast.info("No hay otra cosa en el universo como el Restaurante del Fin del Mundo", {
      description: "¡Conecta tu wallet para acceder a la galaxia!",
      icon: <Coffee className="h-5 w-5" />,
    });
  };
  
  const handleShowCharacterPreview = () => {
    setShowPreview(true);
  };
  
  const handleStartAdventure = () => {
    // Always navigate directly to personality test
    navigate('/personality');
  };
  
  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center px-4 py-20">
      <StarryBackground />
      <CosmicParticles />
      
      {/* Main content */}
      <div className="max-w-5xl w-full mx-auto text-center z-10 space-y-12">
        <div className="space-y-6 animate-float">
          <div className="inline-block mb-2">
            {/* <Sparkles className="inline-block h-8 w-8 text-cosmic-cyan" /> */}
            <img src="/restaurant_nobackground.webp" alt="Logo" className="h-[300px] w-auto" />
          </div>
          
          <NeonTitle variant="magenta" size="xl" className="mb-3">
            {t('landing.title')}
          </NeonTitle>
          
          <h2 className="text-xl md:text-2xl font-space font-medium text-cosmic-cyan">
            🛸 {t('landing.subtitle')}
          </h2>
          
          {/* {showQuote && (
            <div className="opacity-0 animate-[fade-in_1s_ease_forwards] mt-4 h-20">
              <TypewriterText
                text={AdventureQuotes[quoteIndex]}
                speed={40}
                className="text-lg md:text-xl italic text-cosmic-green font-space"
                onComplete={() => setTypingComplete(true)}
              />
            </div>
          )} */}
          
          {/* <div className="max-w-2xl mx-auto opacity-0 animate-[fade-in_1.5s_ease_forwards] delay-500">
            <p className="text-white/80 px-4">
              Crea tu personaje galáctico, vive historias aleatorias generadas por IA y 
              embárcate en una travesía por los rincones más extraños del multiverso.
              ¿Estás listo para la aventura más ridículamente entretenida de tu vida?
            </p>
          </div> */}
        </div>
        
        <div className="flex flex-col items-center space-y-8 pb-10">

          <div className="flex gap-4 items-center">
          <ButtonGlow color="cyan">
            <CosmicButton 
              variant="primary" 
              size="lg"
              onClick={handleStartAdventure}
            >
              <span className="text-xl">{t('landing.getStarted')}</span>
            </CosmicButton>
          </ButtonGlow>
          
          <ButtonGlow color="cyan">
            <CosmicButton 
              variant="secondary" 
              size="lg"
              onClick={handleCheckGalaxy}
            >
              <span className="text-xl">{t('landing.exploreGalaxy')}</span>
            </CosmicButton>
          </ButtonGlow>
          </div>

        </div>

                {/* Adventure Steps */}
        <AdventureSteps />

        
        {/* Character Progress Card */}
        <div className="mt-12 animate-fade-in">
          <CharactersProgressCard />
        </div>

        
        {/* Latest Characters Slider - NEW SECTION */}
        <div className="mt-8 animate-fade-in">
          <LatestCharacterSlider />
        </div>
        
        {/* Testimonials Section
        <div className="mt-12 max-w-4xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 px-4">
            <GalaxyCard hasGlow glowColor="cyan" className="transform hover:scale-105 transition-transform">
              <div className="text-center p-4">
                <p className="italic text-white/80">
                  "Mi personaje 'Marvin, el Optimista Depresivo' me llevó a través de 
                  una aventura con puertas existenciales. ¡5/5 estrellas! Le daría 6 
                  si hubiera tenido mejor servicio."
                </p>
                <p className="mt-3 text-cosmic-cyan">— Viajero Galáctico #42</p>
              </div>
            </GalaxyCard>
            
            <GalaxyCard hasGlow glowColor="magenta" className="transform hover:scale-105 transition-transform">
              <div className="text-center p-4">
                <p className="italic text-white/80">
                  "¡No hay nada más divertido que escapar de la policía intergaláctica 
                  mientras tu personaje intenta razonar con un sándwich parlante! 
                  Altamente improbable y totalmente recomendado."
                </p>
                <p className="mt-3 text-cosmic-magenta">— Ex-presidente de la Galaxia</p>
              </div>
            </GalaxyCard>
          </div>
        </div> */}
        

        
        {/* Feature cards */}
        <FeatureCards />
      </div>
      
      <footer className="absolute bottom-4 text-center w-full text-xs text-white/50">
        {t('footer.inspirationText')} © {new Date().getFullYear()}
      </footer>

      {/* Character Preview Dialog */}
      <Dialog open={showPreview} onOpenChange={setShowPreview}>
        <DialogContent className="max-w-md bg-cosmic-dark border-cosmic-cyan/30">
          <div className="py-4">
            <h3 className="text-xl font-space text-cosmic-cyan text-center mb-4">Personaje de Ejemplo</h3>
            <CharacterCard character={sampleCharacter} />
            <p className="text-center mt-6 text-sm text-white/70">
              Crea tu propio personaje y únete a la aventura más ridícula de la galaxia
            </p>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Landing;
