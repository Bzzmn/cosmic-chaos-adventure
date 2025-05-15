import React from "react";
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./hooks/useAuth";
import ProtectedRoute from "./components/ProtectedRoute";
import Header from "./components/Header";
import Landing from "./pages/Landing";
import AuthPage from "./pages/AuthPage";
import PersonalityTest from "./pages/PersonalityTest";
import CharacterCreation from "./pages/CharacterCreation";
import CharacterDetail from "./pages/CharacterDetail";
import Adventure from "./pages/Adventure";
import NotFound from "./pages/NotFound";

// Creamos el QueryClient fuera del componente para evitar recreaciones en cada render
const queryClient = new QueryClient();

// Definimos el componente App como una función explícitamente
const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <AuthProvider>
            <Header />
            <div className="pt-8"> {/* Add padding to account for fixed header */}
              <Routes>
                <Route path="/" element={<Landing />} />
                <Route path="/auth" element={<AuthPage />} />
                <Route path="/personality" element={<PersonalityTest />} /> {/* No longer protected */}
                <Route path="/character-creation" element={
                  <ProtectedRoute>
                    <CharacterCreation />
                  </ProtectedRoute>
                } />
                <Route path="/character/:address" element={
                  <ProtectedRoute>
                    <CharacterDetail />
                  </ProtectedRoute>
                } />
                <Route path="/adventure" element={
                  <ProtectedRoute>
                    <Adventure />
                  </ProtectedRoute>
                } />
                {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
                <Route path="*" element={<NotFound />} />
              </Routes>
            </div>
          </AuthProvider>
        </BrowserRouter>
      </TooltipProvider>
    </QueryClientProvider>
  );
};

export default App;
