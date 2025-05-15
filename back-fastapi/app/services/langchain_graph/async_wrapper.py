"""
Wrapper para ejecutar funciones síncronas en un entorno asincrónico.
"""
import asyncio
from functools import wraps
from typing import Any, Callable, Coroutine, Dict
import concurrent.futures

def to_async(func: Callable) -> Callable[..., Coroutine[Any, Any, Any]]:
    """
    Convierte una función síncrona en asíncrona.
    
    Args:
        func: Función síncrona a convertir
        
    Returns:
        Versión asíncrona de la función
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Usar ThreadPoolExecutor para ejecutar funciones síncronas en un thread
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return await asyncio.get_event_loop().run_in_executor(
                pool, lambda: func(*args, **kwargs)
            )
    return wrapper

class AsyncGraph:
    """Wrapper asincrónico para LangGraph."""
    def __init__(self, graph):
        self.graph = graph
    
    async def arun(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta el grafo de manera asíncrona.
        
        Args:
            inputs: Entradas para el grafo
            
        Returns:
            Resultados del grafo
        """
        try:
            # Utilizar to_async para ejecutar el grafo en un thread separado
            run_func = to_async(self.graph.invoke)
            return await run_func(inputs)
        except Exception as e:
            # Fallback a una simulación básica si hay error
            print(f"Error ejecutando el grafo: {str(e)}")
            return self._fallback_simulation(inputs)

    def _fallback_simulation(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Proporciona una respuesta simulada en caso de error.
        
        Args:
            inputs: Entradas originales
            
        Returns:
            Resultados simulados
        """
        theme = inputs.get("theme", "espacio")
        
        # Respuesta simulada
        return {
            "generate_question": {
                "question": f"Pregunta simulada sobre {theme}",
                "scenario_description": f"Descripción de escenario simulado sobre {theme}."
            },
            "generate_image": {
                "context_image": "/static/images/fallback/cosmic_default.jpg"
            },
            "generate_options": {
                "options": [
                    {"text": "Opción simulada 1", "emoji": "🚀", "value": 4, "effect": {"quantum_charisma": 10}},
                    {"text": "Opción simulada 2", "emoji": "🔭", "value": 3, "effect": {"absurdity_resistance": 8}},
                    {"text": "Opción simulada 3", "emoji": "🌌", "value": 2, "effect": {"time_warping": 12}},
                    {"text": "Opción simulada 4", "emoji": "🛰️", "value": 1, "effect": {"cosmic_luck": 5}}
                ]
            },
            "generate_feedback": {
                "options_with_feedback": [
                    {"text": "Opción simulada 1", "emoji": "🚀", "value": 4, "effect": {"quantum_charisma": 10}, "feedback": "Feedback para opción 1"},
                    {"text": "Opción simulada 2", "emoji": "🔭", "value": 3, "effect": {"absurdity_resistance": 8}, "feedback": "Feedback para opción 2"},
                    {"text": "Opción simulada 3", "emoji": "🌌", "value": 2, "effect": {"time_warping": 12}, "feedback": "Feedback para opción 3"},
                    {"text": "Opción simulada 4", "emoji": "🛰️", "value": 1, "effect": {"cosmic_luck": 5}, "feedback": "Feedback para opción 4"}
                ]
            }
        }
