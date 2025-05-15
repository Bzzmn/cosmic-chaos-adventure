import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { useTranslation } from 'react-i18next';
import StarryBackground from '@/components/StarryBackground';
import CosmicParticles from '@/components/CosmicParticles';
import CosmicButton from '@/components/CosmicButton';
import NeonTitle from '@/components/NeonTitle';
import GalaxyCard from '@/components/GalaxyCard';
import TypewriterText from '@/components/TypewriterText';
import CharacterCard, { CharacterType, Artifact } from '@/components/CharacterCard';
import { ArrowLeft, ArrowRight, Star, Sparkles, User, ChevronLeft, ChevronRight } from 'lucide-react';
import { cn } from '@/lib/utils';

interface StoryOption {
  text: string;
  outcome: string;
  nextStep: number;
  icon: React.ReactNode;
  artifact?: Artifact;
}

interface StoryStep {
  narrative: string;
  options: StoryOption[];
}

// Sample artifact definitions
const possibleArtifacts: Artifact[] = [
  {
    id: "art-1",
    name: "Paradoxical Calculator",
    description: "Adds by subtracting and multiplies by dividing, but somehow always gets the correct result.",
    effect: {
      stat: "absurdityResistance",
      bonus: 20,
      duration: 3,
    },
    isActive: false
  },
  {
    id: "art-2",
    name: "Infinite Coffee Mug",
    description: "A cup that never empties, although each sip tastes like a different beverage.",
    effect: {
      stat: "quantumCharisma",
      bonus: 15,
      duration: 2,
    },
    isActive: false
  },
  {
    id: "art-3",
    name: "Voice Glasses",
    description: "They allow you to see what others say as floating text, including thoughts they don't want to share.",
    effect: {
      stat: "sarcasmLevel",
      bonus: 25,
      duration: 1,
    },
    isActive: false
  },
  {
    id: "art-4",
    name: "Whimsical Pocket Watch",
    description: "Sometimes it runs fast, sometimes it runs slow, but it always gets you to where you need to be on time.",
    effect: {
      stat: "timeWarping",
      bonus: 20,
      duration: 2,
    },
    isActive: false
  },
  {
    id: "art-5",
    name: "Probabilistic Umbrella",
    description: "Subtly alters reality so that improbable events occur in your favor.",
    effect: {
      stat: "cosmicLuck",
      bonus: 30,
      duration: 1,
    },
    isActive: false
  }
];

const Adventure: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [showOutcome, setShowOutcome] = useState<string | null>(null);
  const [storyComplete, setStoryComplete] = useState<boolean>(false);
  const [character, setCharacter] = useState<CharacterType | null>(location.state?.character || null);
  const [artifactMessage, setArtifactMessage] = useState<string | null>(null);
  const [isFirstAdventure, setIsFirstAdventure] = useState<boolean>(false);
  const [characterPanelOpen, setCharacterPanelOpen] = useState<boolean>(false);
  
  // Set character panel to be closed by default on all screens
  useEffect(() => {
    setCharacterPanelOpen(false);
  }, []);
  
  // Check if we have a character
  useEffect(() => {
    if (!character) {
      navigate('/personality');
      return;
    }
    
    // Check if this is the first adventure (coming from character creation)
    if (location.state?.fromCharacterCreation) {
      setIsFirstAdventure(true);
      
      // Welcome toast for first adventure
      toast.success(t('adventure.firstAdventureWelcome'), {
        description: t('adventure.firstAdventureDescription', { name: character.name }),
        icon: <Star className="h-5 w-5" />,
        duration: 5000,
      });
    }
  }, [character, navigate, location.state, t]);

  // Enhance story steps with artifact rewards
  const storySteps: StoryStep[] = [
    {
      narrative: `You wake up on a spaceship bound for the Restaurant at the End of the Universe. The captain announces that we'll have to make a small detour through a wormhole. Suddenly, the lights flicker and an alarm sounds. "Passengers, please remain calm," says a robotic voice, "We are experiencing technical difficulties..."`,
      options: [
        {
          text: "Offer help to the captain",
          outcome: `You head to the bridge. The captain, a penguin in a spacesuit, looks at you in surprise: "Oh, ${character?.name}, just in time! We urgently need a ${character?.class}." He hands you a quantum screwdriver and points to a console full of flashing buttons.`,
          nextStep: 1,
          icon: <Star className="h-5 w-5" />,
          artifact: possibleArtifacts[0]
        },
        {
          text: "Stay in your seat and order another drink",
          outcome: `You order another Pan Galactic Gargle Blaster. The robot waiter brings you one and says: "The last drink before the... temporary end of the journey". As you drink, the ship takes an unexpected turn and you end up floating down the center aisle to the amusement of the other passengers.`,
          nextStep: 2,
          icon: <Sparkles className="h-5 w-5" />
        }
      ]
    },
    {
      narrative: `You're holding the quantum screwdriver while the penguin-captain watches nervously. "We need to reconnect the improbability drive before we get trapped in the dimension of eternal Thursdays," he explains. The console has two loose cables: one bright blue and one fluorescent pink.`,
      options: [
        {
          text: "Connect the blue cable to the main port",
          outcome: `You connect the blue cable. The ship vibrates, the lights change to a purple hue, and for a moment everyone on board transforms into singing salamanders before returning to normal. The captain claps with his flippers: "Brilliant! We've taken an interdimensional shortcut."`,
          nextStep: 3,
          icon: <Star className="h-5 w-5" />
        },
        {
          text: "Connect the pink cable and cross your fingers",
          outcome: `When you connect the pink cable, the ship's gravity momentarily reverses. Everything and everyone falls towards the ceiling. The penguin-captain slides a badge towards you: "Congratulations, you are now the new gravitational orientation officer. We didn't have one until now."`,
          nextStep: 3,
          icon: <Sparkles className="h-5 w-5" />,
          artifact: possibleArtifacts[1]
        }
      ]
    },
    {
      narrative: `As the drink takes effect, you find you can understand the conversations of the ship's ornamental plants. One of them, a cactus wearing a tie, complains about the lack of humidity. Suddenly, the ship shakes and the captain announces: "Would all passengers with intergalactic negotiation skills please report to hatch 7."`,
      options: [
        {
          text: "Ignore the announcement and keep listening to the plants",
          outcome: `The plants reveal to you the secret of emotional photosynthesis and give you a small seed that, according to them, will grow in any environment and protect you from sad thoughts. You put it in your pocket just as the ship stabilizes.`,
          nextStep: 3,
          icon: <Sparkles className="h-5 w-5" />,
          artifact: possibleArtifacts[2]
        },
        {
          text: "Go to hatch 7, pretending to know about negotiation",
          outcome: `At the hatch you find the captain negotiating with an intelligent gas cloud that has confused the ship with its distant cousin. Your absurd interpretation of an expert in gaseous relations convinces the cloud to release them, impressing the entire crew.`,
          nextStep: 3,
          icon: <Star className="h-5 w-5" />
        }
      ]
    },
    {
      narrative: `Finally, the ship stabilizes and you arrive at your destination: The Restaurant at the End of the Universe. The maître d', a being with five eyes and an elegant tuxedo, recognizes you: "Ah, ${character?.name}, the famous ${character?.class}. Your table is ready by the window with views of tonight's cosmic apocalypse. Would you like to see the menu or would you prefer the chef's surprise specialty?"`,
      options: [
        {
          text: "Look at the menu in detail",
          outcome: `The menu is written in 17 languages simultaneously and changes every time you blink. You finally order "something that won't try to eat me first". They serve you a dish that sings opera every time you poke it. It's delicious and makes you feel temporarily omniscient.`,
          nextStep: 4,
          icon: <Sparkles className="h-5 w-5" />,
          artifact: possibleArtifacts[3]
        },
        {
          text: "Try the surprise specialty",
          outcome: `The chef, a luminous octopus with a chef's hat, personally brings a covered dish. When uncovered, it reveals a dessert that suspiciously resembles you, made of something like jelly. "It's an honor-reflection," explains the chef. "It tastes like your favorite memory." And curiously, it does.`,
          nextStep: 4,
          icon: <Star className="h-5 w-5" />
        }
      ]
    },
    {
      narrative: `As you enjoy your meal, the universe begins its final show outside the window. Galaxies compress, stars explode in slow motion, and everything reduces to a point of bright light before restarting for the next session. An android approaches your table with a small box: "To commemorate your visit, we offer the opportunity to take with you an eternal souvenir in the form of an NFT. Would you be interested in preserving your cosmic identity on the universal blockchain?"`,
      options: [
        {
          text: "Accept the cosmic NFT",
          outcome: `The android smiles and takes a capture of your essence. "Your identity has been immortalized on the universal blockchain. Even after this cycle of the universe, ${character?.name} the ${character?.class} will remain in the cosmic registry." He hands you a holographic card with a multidimensional QR code.`,
          nextStep: -1, // End of story
          icon: <Sparkles className="h-5 w-5" />
        },
        {
          text: "Politely decline, preferring to maintain your mystery",
          outcome: `"Wise decision," says the android with a wink. "Some prefer to remain as unregistered legends." He gives you a small golden key anyway. "For the next time you visit. The back door will always be open for ${character?.name}, the enigmatic ${character?.class}."`,
          nextStep: -1, // End of story
          icon: <Star className="h-5 w-5" />,
          artifact: possibleArtifacts[4]
        }
      ]
    }
  ];
  
  const handleChooseOption = (option: StoryOption) => {
    // Check if this option gives an artifact
    if (option.artifact && character) {
      // Find first empty slot
      const emptySlotIndex = character.artifacts.findIndex(slot => slot === null);
      
      if (emptySlotIndex !== -1) {
        // Clone character to avoid direct state mutation
        const updatedCharacter = {...character};
        // Clone artifacts array
        updatedCharacter.artifacts = [...updatedCharacter.artifacts];
        // Add artifact to empty slot
        updatedCharacter.artifacts[emptySlotIndex] = {...option.artifact};
        
        setCharacter(updatedCharacter);
        setArtifactMessage(t('adventure.artifactObtained', { name: option.artifact.name }));
        
        // Show toast
        toast.success(t('adventure.newArtifact'), {
          description: option.artifact.name,
          icon: <Sparkles className="h-5 w-5" />,
        });
      }
    }
    
    // Show outcome
    setShowOutcome(option.outcome);
    
    // After delay, go to next step or finish
    setTimeout(() => {
      setArtifactMessage(null);
      if (option.nextStep >= 0) {
        setCurrentStep(option.nextStep);
        setShowOutcome(null);
      } else {
        // Story complete
        setStoryComplete(true);
      }
    }, 6000);
  };
  
  const handleActivateArtifact = (artifactIndex: number) => {
    if (!character || !character.artifacts[artifactIndex]) return;
    
    // Clone character and artifacts to avoid direct state mutation
    const updatedCharacter = {...character};
    updatedCharacter.artifacts = [...updatedCharacter.artifacts];
    
    const artifact = updatedCharacter.artifacts[artifactIndex];
    
    // Toggle artifact activation
    if (artifact) {
      const updatedArtifact = {...artifact};
      updatedArtifact.isActive = !updatedArtifact.isActive;
      
      if (updatedArtifact.isActive) {
        toast.success(t('adventure.artifactActivated'), {
          description: t('adventure.artifactEffect', { 
            name: artifact.name, 
            stat: t(`personalityTest.traits.${artifact.effect.stat}`), 
            bonus: artifact.effect.bonus, 
            duration: artifact.effect.duration 
          }),
          icon: <Sparkles className="h-5 w-5" />,
        });
      } else {
        toast.info(t('adventure.artifactDeactivated'), {
          description: artifact.name,
          icon: <Star className="h-5 w-5" />,
        });
      }
      
      updatedCharacter.artifacts[artifactIndex] = updatedArtifact;
      setCharacter(updatedCharacter);
    }
  };
  
  const handleMintNFT = () => {
    toast.success(t('adventure.mintNFTTitle'), {
      description: t('adventure.mintNFTDescription'),
      icon: <Star className="h-5 w-5" />,
      action: {
        label: t('adventure.connectWallet'),
        onClick: () => {
          toast.info(t('adventure.mintInDevelopment'), {
            description: t('adventure.nextUpdateFeature'),
          });
        },
      },
    });
  };
  
  const handleBackToStart = () => {
    navigate('/');
  };
  
  const toggleCharacterPanel = () => {
    setCharacterPanelOpen(!characterPanelOpen);
  };
  
  const currentStoryStep = storySteps[currentStep];
  
  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center px-4 py-20">
      <StarryBackground />
      <CosmicParticles />
      
      {isFirstAdventure && (
        <div className="absolute top-4 left-0 right-0 z-20 flex justify-center">
          <div className="bg-cosmic-green/20 text-cosmic-green px-4 py-2 rounded-lg backdrop-blur-md border border-cosmic-green/30 max-w-md text-center">
            <h3 className="font-semibold mb-1">{t('adventure.welcomeTitle')}</h3>
            <p className="text-sm">{t('adventure.welcomeMessage', { name: character?.name })}</p>
          </div>
        </div>
      )}
      
      {/* Character panel toggle button - Fixed position */}
      <button 
        onClick={toggleCharacterPanel}
        className="fixed left-0 top-1/2 transform -translate-y-1/2 z-40 bg-cosmic-dark/80 hover:bg-cosmic-dark/90 border border-cosmic-cyan/30 rounded-r-lg p-2 text-cosmic-cyan transition-all"
        aria-label={characterPanelOpen ? t('adventure.hideCharacter') : t('adventure.showCharacter')}
      >
        {characterPanelOpen ? <ChevronLeft /> : <ChevronRight />}
        <User className="h-5 w-5 mt-1" />
      </button>
      
      {/* Character sidebar - Overlay */}
      <div 
        className={cn(
          "fixed top-0 left-0 h-full z-30 transform transition-transform duration-300 ease-in-out",
          characterPanelOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        <div className="relative h-full">
          {/* Semi-transparent overlay backdrop */}
          {characterPanelOpen && (
            <div 
              className="fixed inset-0 bg-black/50 backdrop-blur-sm z-30"
              onClick={toggleCharacterPanel}
            />
          )}
          
          {/* Character panel */}
          <div className="relative z-40 h-full bg-black/90 border-r border-cosmic-cyan/20 overflow-y-auto pb-20 pt-20 w-full sm:w-80 lg:w-96">
            {character && (
              <div className="px-4">
                <CharacterCard 
                  character={character} 
                  onActivateArtifact={handleActivateArtifact}
                />
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Main story content - Always centered */}
      <div className="max-w-3xl w-full mx-auto z-10">
        <div className="mb-8 text-center">
          <NeonTitle variant="magenta" size="lg">{t('adventure.title')}</NeonTitle>
        </div>
        
        {/* Progress bar */}
        <div className="h-1 w-full bg-white/10 rounded-full mb-8">
          <div 
            className="h-full bg-cosmic-magenta rounded-full" 
            style={{ width: `${(currentStep / (storySteps.length - 1)) * 100}%` }}
          />
        </div>
        
        {storyComplete ? (
          <div className="text-center space-y-6">
            <GalaxyCard hasGlow glowColor="green" className="min-h-[14rem] flex flex-col justify-center">
              <div className="p-4">
                <h3 className="text-2xl font-space font-bold text-cosmic-green mb-4">
                  {t('adventure.completed')}
                </h3>
                <p className="mb-4">
                  {t('adventure.completedMessage', { name: character?.name, class: character?.class })}
                </p>
                <p className="text-white/70">
                  {t('adventure.mintQuestion')}
                </p>
              </div>
            </GalaxyCard>
            
            <div className="flex flex-col space-y-4 sm:flex-row sm:space-y-0 sm:space-x-4 justify-center">
              <CosmicButton variant="primary" onClick={handleMintNFT}>
                <Star className="mr-2 h-4 w-4" />
                {t('adventure.takeToMultiverse')}
              </CosmicButton>
              
              <CosmicButton variant="secondary" onClick={handleBackToStart}>
                <ArrowLeft className="mr-2 h-4 w-4" />
                {t('adventure.backToHome')}
              </CosmicButton>
            </div>
          </div>
        ) : showOutcome || artifactMessage ? (
          <GalaxyCard hasGlow glowColor="magenta" className="min-h-[14rem] flex flex-col justify-center">
            <div className="p-4">
              {artifactMessage && (
                <div className="bg-cosmic-green/20 text-cosmic-green p-3 rounded-md mb-4">
                  <TypewriterText 
                    text={artifactMessage} 
                    className="text-sm"
                    speed={30}
                  />
                </div>
              )}
              {showOutcome && (
                <TypewriterText 
                  text={showOutcome} 
                  className="text-lg"
                  speed={30}
                />
              )}
            </div>
          </GalaxyCard>
        ) : (
          <div className="space-y-6">
            <GalaxyCard hasGlow glowColor="cyan" className="min-h-[14rem] flex flex-col justify-center">
              <div className="p-4">
                <TypewriterText 
                  text={currentStoryStep.narrative} 
                  className="text-lg"
                  speed={20}
                />
              </div>
            </GalaxyCard>
            
            <div className="grid grid-cols-1 gap-4">
              {currentStoryStep.options.map((option, index) => (
                <button 
                  key={index} 
                  onClick={() => handleChooseOption(option)}
                  className="bg-black/40 backdrop-blur-sm border border-white/10 rounded-lg p-4 text-left hover:bg-white/5 transition-colors flex items-center"
                >
                  <div className="h-10 w-10 rounded-full flex items-center justify-center bg-cosmic-magenta/20 mr-4">
                    {option.icon}
                  </div>
                  <div className="flex-1">
                    <span>{option.text}</span>
                    {option.artifact && (
                      <div className="mt-1 text-xs text-cosmic-cyan flex items-center">
                        <Star className="h-3 w-3 mr-1" />
                        <span>{t('adventure.reward')}: {option.artifact.name}</span>
                      </div>
                    )}
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Adventure;
