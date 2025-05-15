import React, { useState, useEffect } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { toast } from 'sonner';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import StarryBackground from '@/components/StarryBackground';
import CosmicParticles from '@/components/CosmicParticles';
import GalaxyCard from '@/components/GalaxyCard';
import NeonTitle from '@/components/NeonTitle';
import CosmicButton from '@/components/CosmicButton';
import { Github, Mail, LogIn, UserPlus, User, ArrowRight } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { usePersonalityStore } from '@/lib/store';

// Login form schema
const loginSchema = z.object({
  email: z.string().email("Ingresa un correo electrónico válido"),
  password: z.string().min(6, "La contraseña debe tener al menos 6 caracteres"),
});

// Registration form schema
const registerSchema = z.object({
  name: z.string().min(2, "El nombre debe tener al menos 2 caracteres"),
  email: z.string().email("Ingresa un correo electrónico válido"),
  password: z.string().min(6, "La contraseña debe tener al menos 6 caracteres"),
});

interface LocationState {
  from?: Location;
  answers?: number[];
  questions?: any[];
  fromTest?: boolean;
}

const AuthPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"login" | "register">("login");
  const navigate = useNavigate();
  const location = useLocation();
  const { login, register: registerUser } = useAuth();
  
  // Usar el Zustand store
  const { answers, questions, isTestCompleted } = usePersonalityStore();
  
  const state = location.state as LocationState;
  const fromTest = state?.fromTest || isTestCompleted;
  
  // Set active tab to register if coming from test
  useEffect(() => {
    if (fromTest) {
      setActiveTab("register");
    }
  }, [fromTest]);

  // Login form
  const loginForm = useForm<z.infer<typeof loginSchema>>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: ""
    },
  });

  // Registration form
  const registerForm = useForm<z.infer<typeof registerSchema>>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      name: "",
      email: "",
      password: ""
    },
  });

  // Handle login submission
  const onLoginSubmit = (values: z.infer<typeof loginSchema>) => {
    login(values.email, values.password)
      .then(() => {
        toast.success("¡Inicio de sesión exitoso!");
        if (fromTest && answers.length > 0) {
          // Si viene del test con respuestas guardadas, ir a creación de personaje
          navigate("/character-creation");
        } else {
          navigate("/personality");
        }
      })
      .catch((error) => {
        toast.error("Error al iniciar sesión", {
          description: error.message || "Verifica tus credenciales e intenta de nuevo"
        });
      });
  };

  // Handle registration submission
  const onRegisterSubmit = (values: z.infer<typeof registerSchema>) => {
    registerUser(values.name, values.email, values.password)
      .then(() => {
        toast.success("¡Registro exitoso!");
        if (fromTest && answers.length > 0) {
          // Si viene del test con respuestas guardadas, ir a creación de personaje
          navigate("/character-creation");
        } else {
          navigate("/personality");
        }
      })
      .catch((error) => {
        toast.error("Error al registrarse", {
          description: error.message || "Intenta con otro correo electrónico"
        });
      });
  };

  // Handle social login
  const handleSocialLogin = (provider: string) => {
    // Mock social login
    toast.loading(`Iniciando sesión con ${provider}...`);
    setTimeout(() => {
      login("user@example.com", "password123", provider)
        .then(() => {
          toast.success(`¡Inicio de sesión con ${provider} exitoso!`);
          if (fromTest && answers.length > 0) {
            // Si viene del test con respuestas guardadas, ir a creación de personaje
            navigate("/character-creation");
          } else {
            navigate("/personality");
          }
        })
        .catch(() => {
          toast.error(`Error al iniciar sesión con ${provider}`);
        });
    }, 1500);
  };

  return (
    <div className="relative min-h-screen w-full flex items-center justify-center py-12 px-4">
      <StarryBackground />
      <CosmicParticles />
      
      <div className="w-full max-w-md z-10">
        <div className="text-center mb-8">
          <Link to="/" className="inline-block">
            <NeonTitle size="lg" variant="magenta" className="mb-2">
              El Restaurante del Fin del Universo
            </NeonTitle>
          </Link>
          {fromTest ? (
            <p className="text-cosmic-green font-space">¡Genial! Regístrate para guardar tu personaje</p>
          ) : (
            <p className="text-cosmic-cyan font-space">¡Prepárate para tu aventura cósmica!</p>
          )}
        </div>
        
        <GalaxyCard className="w-full" hasGlow glowColor="cyan">
          <Tabs
            defaultValue={activeTab}
            value={activeTab}
            onValueChange={(v) => setActiveTab(v as "login" | "register")}
            className="w-full"
          >
            <TabsList className="grid grid-cols-2 mb-6">
              <TabsTrigger value="login" className="font-space">Iniciar Sesión</TabsTrigger>
              <TabsTrigger value="register" className="font-space">Registrarse</TabsTrigger>
            </TabsList>
            
            <TabsContent value="login" className="space-y-6">
              <div className="space-y-2 text-center">
                <h2 className="text-2xl font-space font-bold text-cosmic-cyan">Bienvenido de nuevo</h2>
                <p className="text-sm text-white/70">Ingresa tus credenciales para continuar</p>
              </div>
              
              <Form {...loginForm}>
                <form onSubmit={loginForm.handleSubmit(onLoginSubmit)} className="space-y-4">
                  <FormField
                    control={loginForm.control}
                    name="email"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-white">Correo electrónico</FormLabel>
                        <FormControl>
                          <div className="relative">
                            <Mail className="absolute left-3 top-3 h-4 w-4 text-cosmic-cyan/70" />
                            <Input placeholder="tu@email.com" className="pl-10" {...field} />
                          </div>
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  
                  <FormField
                    control={loginForm.control}
                    name="password"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-white">Contraseña</FormLabel>
                        <FormControl>
                          <Input type="password" placeholder="••••••••" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  
                  <Button 
                    type="submit" 
                    className="w-full bg-cosmic-magenta hover:bg-cosmic-magenta/90"
                  >
                    <LogIn className="mr-2 h-4 w-4" /> Iniciar Sesión
                  </Button>
                </form>
              </Form>
              
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t border-white/10" />
                </div>
                <div className="relative flex justify-center text-xs">
                  <span className="bg-cosmic-dark px-2 text-white/50">O continúa con</span>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-3">
                <Button 
                  variant="outline" 
                  className="border-white/20 hover:bg-white/5"
                  onClick={() => handleSocialLogin("GitHub")}
                >
                  <Github className="mr-2 h-4 w-4" /> GitHub
                </Button>
                <Button 
                  variant="outline" 
                  className="border-white/20 hover:bg-white/5"
                  onClick={() => handleSocialLogin("Google")}
                >
                  <svg className="mr-2 h-4 w-4" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="google" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 488 512">
                    <path fill="currentColor" d="M488 261.8C488 403.3 391.1 504 248 504 110.8 504 0 393.2 0 256S110.8 8 248 8c66.8 0 123 24.5 166.3 64.9l-67.5 64.9C258.5 52.6 94.3 116.6 94.3 256c0 86.5 69.1 156.6 153.7 156.6 98.2 0 135-70.4 140.8-106.9H248v-85.3h236.1c2.3 12.7 3.9 24.9 3.9 41.4z"></path>
                  </svg>
                  Google
                </Button>
              </div>
            </TabsContent>
            
            <TabsContent value="register" className="space-y-6">
              <div className="space-y-2 text-center">
                <h2 className="text-2xl font-space font-bold text-cosmic-green">Crea tu cuenta</h2>
                <p className="text-sm text-white/70">Ingresa tus datos para registrarte</p>
              </div>
              
              <Form {...registerForm}>
                <form onSubmit={registerForm.handleSubmit(onRegisterSubmit)} className="space-y-4">
                  <FormField
                    control={registerForm.control}
                    name="name"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-white">Nombre</FormLabel>
                        <FormControl>
                          <div className="relative">
                            <User className="absolute left-3 top-3 h-4 w-4 text-cosmic-green/70" />
                            <Input placeholder="Tu nombre" className="pl-10" {...field} />
                          </div>
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  
                  <FormField
                    control={registerForm.control}
                    name="email"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-white">Correo electrónico</FormLabel>
                        <FormControl>
                          <div className="relative">
                            <Mail className="absolute left-3 top-3 h-4 w-4 text-cosmic-green/70" />
                            <Input placeholder="tu@email.com" className="pl-10" {...field} />
                          </div>
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  
                  <FormField
                    control={registerForm.control}
                    name="password"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel className="text-white">Contraseña</FormLabel>
                        <FormControl>
                          <Input type="password" placeholder="••••••••" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  
                  <Button 
                    type="submit" 
                    className="w-full bg-cosmic-green hover:bg-cosmic-green/90"
                  >
                    <UserPlus className="mr-2 h-4 w-4" /> Registrarse
                  </Button>
                </form>
              </Form>
              
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t border-white/10" />
                </div>
                <div className="relative flex justify-center text-xs">
                  <span className="bg-cosmic-dark px-2 text-white/50">O regístrate con</span>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-3">
                <Button 
                  variant="outline" 
                  className="border-white/20 hover:bg-white/5"
                  onClick={() => handleSocialLogin("GitHub")}
                >
                  <Github className="mr-2 h-4 w-4" /> GitHub
                </Button>
                <Button 
                  variant="outline" 
                  className="border-white/20 hover:bg-white/5"
                  onClick={() => handleSocialLogin("Google")}
                >
                  <svg className="mr-2 h-4 w-4" aria-hidden="true" focusable="false" data-prefix="fab" data-icon="google" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 488 512">
                    <path fill="currentColor" d="M488 261.8C488 403.3 391.1 504 248 504 110.8 504 0 393.2 0 256S110.8 8 248 8c66.8 0 123 24.5 166.3 64.9l-67.5 64.9C258.5 52.6 94.3 116.6 94.3 256c0 86.5 69.1 156.6 153.7 156.6 98.2 0 135-70.4 140.8-106.9H248v-85.3h236.1c2.3 12.7 3.9 24.9 3.9 41.4z"></path>
                  </svg>
                  Google
                </Button>
              </div>
            </TabsContent>
          </Tabs>
        </GalaxyCard>
        
        <div className="mt-6 text-center">
          <Link to="/" className="text-cosmic-cyan hover:text-cosmic-magenta transition-colors underline underline-offset-4 font-space text-sm">
            Volver al inicio
          </Link>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
