import React, { createContext, useState, useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { authService } from '@/lib/api/services';
import { User, UserWithToken, LoginCredentials, SocialLoginData, UserUpdate } from '@/lib/api/types';
import { getAuthUser } from '@/lib/api';

// Tipo para errores de API
interface ApiErrorResponse {
  status: number;
  message: string;
  detail?: unknown;
}

// Define tipos
interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string, provider?: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  socialLogin: (provider: string, token: string, email?: string, name?: string) => Promise<void>;
  updateProfile: (data: UserUpdate) => Promise<void>;
  logout: () => void;
}

// Crear contexto de autenticación
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Proveedor de autenticación
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // Estado local para el usuario actual
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  
  // Hooks de React Query
  const queryClient = useQueryClient();
  const navigate = useNavigate();

  // Cargar usuario desde localStorage al inicio
  useEffect(() => {
    const storedUser = getAuthUser<UserWithToken>();
    if (storedUser) {
      setUser(storedUser);
    }
    setIsLoading(false);
  }, []);

  // Mutación para login
  const loginMutation = useMutation({
    mutationFn: async ({ email, password }: { email: string; password: string }) => {
      const credentials: LoginCredentials = {
        username: email, // La API espera 'username' aunque sea un email
        password
      };
      return await authService.login(credentials);
    },
    onSuccess: (data) => {
      setUser(data);
      // Invalidar cualquier consulta relacionada con el usuario
      queryClient.invalidateQueries({ queryKey: ['user'] });
    },
    onError: (error: Error | ApiErrorResponse) => {
      console.error('Error de login:', error);
      throw error;
    }
  });

  // Mutación para registro
  const registerMutation = useMutation({
    mutationFn: async ({ name, email, password }: { name: string; email: string; password: string }) => {
      return await authService.register({ name, email, password });
    },
    onSuccess: (data) => {
      setUser(data);
      // Invalidar cualquier consulta relacionada con el usuario
      queryClient.invalidateQueries({ queryKey: ['user'] });
    },
    onError: (error: Error | ApiErrorResponse) => {
      console.error('Error de registro:', error);
      throw error;
    }
  });
  
  // Mutación para login social
  const socialLoginMutation = useMutation({
    mutationFn: async ({ provider, token, email, name }: SocialLoginData) => {
      return await authService.socialLogin({ provider, token, email, name });
    },
    onSuccess: (data) => {
      setUser(data);
      // Invalidar cualquier consulta relacionada con el usuario
      queryClient.invalidateQueries({ queryKey: ['user'] });
    },
    onError: (error: Error | ApiErrorResponse) => {
      console.error('Error de login social:', error);
      throw error;
    }
  });
  
  // Mutación para actualizar perfil
  const updateProfileMutation = useMutation({
    mutationFn: async (data: UserUpdate) => {
      return await authService.updateProfile(data);
    },
    onSuccess: (data) => {
      setUser({
        ...data,
        token: (user as UserWithToken)?.token // Mantener el token existente
      } as UserWithToken);
      // Invalidar cualquier consulta relacionada con el usuario
      queryClient.invalidateQueries({ queryKey: ['user'] });
      toast.success('Perfil actualizado con éxito');
    },
    onError: (error: Error | ApiErrorResponse) => {
      console.error('Error al actualizar perfil:', error);
      toast.error('Error al actualizar perfil');
      throw error;
    }
  });

  // Función para iniciar sesión
  const login = async (email: string, password: string, provider?: string) => {
    try {
      setIsLoading(true);
      
      if (provider) {
        // Este es un mock para simular login social - en una implementación real, 
        // deberías usar SocialLoginData con token real de OAuth
        await socialLoginMutation.mutateAsync({
          provider,
          token: 'mock-token',
          email,
          name: email.split('@')[0]
        });
      } else {
        await loginMutation.mutateAsync({ email, password });
      }
      
      setIsLoading(false);
    } catch (error: unknown) {
      setIsLoading(false);
      const message = error instanceof Error ? error.message : 'Credenciales inválidas';
      toast.error(`Error al iniciar sesión: ${message}`);
      throw error;
    }
  };

  // Función para registrar un nuevo usuario
  const register = async (name: string, email: string, password: string) => {
    try {
      setIsLoading(true);
      await registerMutation.mutateAsync({ name, email, password });
      setIsLoading(false);
    } catch (error: unknown) {
      setIsLoading(false);
      const message = error instanceof Error ? error.message : 'Error al registrarse';
      toast.error(`Error al registrarse: ${message}`);
      throw error;
    }
  };
  
  // Función para login social
  const socialLogin = async (provider: string, token: string, email?: string, name?: string) => {
    try {
      setIsLoading(true);
      await socialLoginMutation.mutateAsync({ provider, token, email, name });
      setIsLoading(false);
    } catch (error: unknown) {
      setIsLoading(false);
      const message = error instanceof Error ? error.message : `Error al iniciar sesión con ${provider}`;
      toast.error(message);
      throw error;
    }
  };
  
  // Función para actualizar perfil
  const updateProfile = async (data: UserUpdate) => {
    await updateProfileMutation.mutateAsync(data);
  };
  
  // Función para cerrar sesión
  const logout = () => {
    authService.logout();
    setUser(null);
    // Limpiar todas las consultas en caché
    queryClient.clear();
    toast.success('Has cerrado sesión correctamente');
    navigate('/');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        socialLogin,
        updateProfile,
        logout
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// Hook personalizado para acceder al contexto
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth debe ser usado dentro de un AuthProvider');
  }
  return context;
};

export default useAuth;
