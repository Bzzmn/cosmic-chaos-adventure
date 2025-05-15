#!/usr/bin/env python3
"""
Script de prueba para el generador de preguntas de personalidad.
Este script prueba diferentes partes del generador para aislar problemas.
"""
import asyncio
import sys
import os
import traceback
from pprint import pprint

# Configurar variables de entorno para habilitar o deshabilitar características
os.environ["GENERATE_QUESTIONS_ON_DEMAND"] = "true"

# Añadir el directorio principal al path para poder importar paquetes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def test_fallback_question():
    """
    Prueba la función generate_fallback_question
    """
    print("\n=== PRUEBA DE FALLBACK ===")
    try:
        from app.services.langchain_graph.personality_generator import generate_fallback_question
        
        theme = "viaje espacial"
        result = generate_fallback_question(theme)
        
        print(f"Pregunta fallback para '{theme}':")
        pprint(result)
        print("✅ Función de fallback funciona correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en fallback: {str(e)}")
        traceback.print_exc()
        return False

async def test_build_graph():
    """
    Prueba la construcción del grafo
    """
    print("\n=== PRUEBA DE CONSTRUCCIÓN DEL GRAFO ===")
    try:
        from app.services.langchain_graph.personality_generator import build_personality_question_graph
        
        graph = build_personality_question_graph()
        if graph is None:
            print("⚠️ El grafo es None - probablemente langgraph no está disponible")
            return False
        
        print(f"✅ Grafo construido correctamente: {graph}")
        return True
    except Exception as e:
        print(f"❌ Error construyendo el grafo: {str(e)}")
        traceback.print_exc()
        return False

async def test_grafo_ejecucion():
    """
    Prueba la ejecución del grafo con un tema
    """
    print("\n=== PRUEBA DE EJECUCIÓN DEL GRAFO ===")
    try:
        # Solo ejecutar si el grafo se puede construir
        if not await test_build_graph():
            return False
        
        from app.services.langchain_graph.personality_generator import generate_personality_question
        
        theme = "viaje espacial"
        print(f"Generando pregunta para tema '{theme}'...")
        
        result = await generate_personality_question(theme)
        
        print("Resultado:")
        pprint(result)
        print("✅ Generación de pregunta completada")
        return True
    except Exception as e:
        print(f"❌ Error en ejecución del grafo: {str(e)}")
        traceback.print_exc()
        return False

async def test_async_wrapper():
    """
    Prueba específicamente el wrapper asincrónico
    """
    print("\n=== PRUEBA DE ASYNC WRAPPER ===")
    try:
        from app.services.langchain_graph.async_wrapper import AsyncGraph, to_async
        
        # Crear una función síncrona simple
        def dummy_func(x):
            return x * 2
        
        # Convertirla a async
        async_func = to_async(dummy_func)
        
        # Probar
        result = await async_func(5)
        print(f"Resultado de función asíncrona: {result}")
        
        print("✅ AsyncWrapper funciona correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en AsyncWrapper: {str(e)}")
        traceback.print_exc()
        return False

async def test_importacion_langgraph():
    """
    Prueba la importación de langgraph
    """
    print("\n=== PRUEBA DE IMPORTACIÓN DE LANGGRAPH ===")
    try:
        print("Intentando importar langgraph...")
        
        try:
            import langgraph
            print(f"Versión de langgraph: {langgraph.__version__}")
            
            # Probar importación específica de Graph
            from langgraph.graph import Graph
            print("✅ Graph importado correctamente")
            
            # Probar importaciones problemáticas
            print("Intentando importar from langgraph.checkpoint")
            from langgraph.checkpoint import BaseCheckpointSaver
            print("✅ BaseCheckpointSaver importado correctamente")
            
            try:
                from langgraph.checkpoint.base import CheckpointAt
                print("✅ CheckpointAt importado correctamente")
            except ImportError:
                print("❌ No se pudo importar CheckpointAt (error esperado en versiones antiguas)")
            
            return True
        except ImportError as e:
            print(f"❌ Error importando langgraph: {str(e)}")
            traceback.print_exc()
            return False
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        traceback.print_exc()
        return False

async def main():
    """
    Función principal para ejecutar todas las pruebas
    """
    print("🧪 INICIO DE PRUEBAS DE PERSONALITY GENERATOR 🧪")
    
    # 1. Probar importación de langgraph
    await test_importacion_langgraph()
    
    # 2. Probar fallback
    await test_fallback_question()
    
    # 3. Probar async wrapper
    await test_async_wrapper()
    
    # 4. Probar construcción y ejecución del grafo
    await test_grafo_ejecucion()
    
    print("\n✨ PRUEBAS COMPLETADAS ✨")

if __name__ == "__main__":
    asyncio.run(main()) 