"""
Utilidades para el módulo de generación con LangGraph.
"""
import asyncio
from typing import Dict, Any, Callable, Awaitable

def run_async(coro):
    """Ejecuta una coroutine en el evento loop actual o crea uno nuevo."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)

def sync_to_async(func: Callable) -> Callable[..., Awaitable[Any]]:
    """Convierte una función síncrona a asíncrona."""
    async def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def async_to_sync(func: Callable[..., Awaitable[Any]]) -> Callable:
    """Convierte una función asíncrona a síncrona."""
    def wrapper(*args, **kwargs):
        return run_async(func(*args, **kwargs))
    return wrapper
