import google as genai
from PIL import Image
from io import BytesIO
import uuid
from datetime import datetime
import os
from typing import Dict, Any, List, TypedDict
from dotenv import load_dotenv

load_dotenv()


# Suponiendo que tienes un objeto settings o cargas la API key de otra forma
# from app.core.config import settings # Comentado para ejemplo autocontenido


class ImageGenerationError(Exception):
    """Error personalizado para problemas en generación de imágenes"""
    pass

class GeminiImageGeneratorWithFlash:
    def __init__(self,
                 storage_path: str = "static/images/generated_flash",
                 model_name: str = "gemini-2.0-flash-preview-image-generation"):
        self.storage_path = storage_path
        self.model_name = model_name
        os.makedirs(self.storage_path, exist_ok=True)
        print(f"Usando modelo Gemini: {self.model_name}")

    def _format_prompt(self, scenario_description: str) -> str:
        return f"""
        Crea una imagen digital detallada y vibrante para el siguiente escenario de ciencia ficción:

        {scenario_description}

        Estilo: ilustración sci-fi de alta calidad, estética futurista, colores vibrantes, detalles de ciencia ficción, ambiente cósmico.
        Formato: Impactante visualmente, legible como imagen de contexto, sin texto superpuesto en la imagen.
        """

    def _save_image(self, image_data: bytes, scenario_description: str) -> str:
        try:
            # Intenta abrir con Pillow para validar que son datos de imagen válidos
            img = Image.open(BytesIO(image_data))
            img_format = img.format if img.format else "JPEG" # Default a JPEG si no se detecta
            extension = img_format.lower()

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            # Usar una parte del scenario para el nombre puede ser útil pero necesita sanitización
            safe_scenario_part = "".join(c if c.isalnum() else "_" for c in scenario_description[:20])
            filename = f"flash_scenario_{safe_scenario_part}_{timestamp}_{uuid.uuid4().hex[:6]}.{extension}"
            file_path = os.path.join(self.storage_path, filename)

            with open(file_path, "wb") as f:
                f.write(image_data)

            relative_url = f"/{self.storage_path}/{filename}" # Asumiendo que storage_path es relativo a la raíz web de static
            print(f"Imagen guardada en: {file_path}, URL relativa: {relative_url}")
            return relative_url
        except Exception as e:
            print(f"Error al guardar o validar la imagen: {e}")
            raise ImageGenerationError(f"Fallo al procesar/guardar datos de imagen: {e}")


    async def generate_image(self, scenario_description: str) -> Dict[str, Any]:
        # Suponiendo que tienes una variable global o un setting para habilitar/deshabilitar
        # IMAGE_GENERATION_ENABLED = True # O settings.IMAGE_GENERATION_ENABLED
        # if not IMAGE_GENERATION_ENABLED:
        #     print("Generación de imágenes deshabilitada.")
        #     return self._get_fallback_image(scenario_description, "Image generation disabled")

        prompt_text = self._format_prompt(scenario_description)
        if not prompt_text:
            print("Prompt vacío, usando fallback.")
            return self._get_fallback_image(scenario_description, "Prompt is empty")

        print(f"Generando imagen para: '{scenario_description[:50]}...'")

        try:
            from google.genai import types  # Importación local para evitar error si no está instalado
            
            # Configurar el modelo para generación de imágenes
            client = genai.Client()
            
            # Según la documentación, debemos especificar las modalidades de respuesta
            # como TEXT e IMAGE para la generación de imágenes
            generation_config = types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"]
            )
            
            # Enviar la solicitud según formato de la documentación oficial
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt_text,
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"]
                )
            )

            
            # Procesar la respuesta multimodal
            print("Procesando respuesta del API...")
            
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text') and part.text is not None:
                    print(f"Texto recibido: {part.text[:100]}...")
                elif hasattr(part, 'inline_data') and part.inline_data is not None:
                    # Extraer los datos de la imagen
                    image_data = part.inline_data.data
                    mime_type = part.inline_data.mime_type
                    print(f"Imagen recibida. Tipo MIME: {mime_type}")
                    
                    # Guardar la imagen
                    image_url = self._save_image(image_data, scenario_description)
                    return {
                        "generated_image_url": image_url,
                        "generated_description": "Imagen generada con éxito por Gemini",
                    }
            
            # Si llegamos aquí, no se encontró ninguna imagen en la respuesta
            print("No se encontró imagen en la respuesta")
            return self._get_fallback_image(scenario_description, "No se encontró imagen en la respuesta")

        except Exception as e:
            import traceback
            print(f"Excepción durante la llamada a la API de Gemini o procesamiento: {e}")
            traceback.print_exc()
            return self._get_fallback_image(scenario_description, f"Error en API: {str(e)}")

    def _get_fallback_image(self, scenario_description: str, error_msg: str) -> Dict[str, str]:
        print(f"FALLBACK: Usando imagen de respaldo para '{scenario_description[:30]}...'. Error: {error_msg}")
        # Lógica de fallback (puedes mejorarla como en tu código original)
        # Por simplicidad, devolvemos una URL genérica o un mensaje
        return {
            "generated_image_url": "/static/images/fallback/cosmic_default.jpg", 
            "generated_description": f"Descripción de respaldo para: {scenario_description[:50]}...",
            "error_message": error_msg
        }


# --- Definición del Estado y Nodo para LangGraph ---

class ImageGenerationState(TypedDict):
    scenario_description: str
    generated_image_url: str
    generated_description: str  # Para la descripción generada
    error_message: str  # Para capturar errores si la generación falla

# Instancia global del generador (o podrías pasarla/crearla dentro del nodo si prefieres)




