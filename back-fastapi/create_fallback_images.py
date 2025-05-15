import os
import requests
import json
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import shutil
from openai import OpenAI

# Configuración
FALLBACK_DIR = "static/images/fallback"
API_KEY = os.environ.get("OPENAI_API_KEY", "")

# Asegurarse de que el directorio existe
os.makedirs(FALLBACK_DIR, exist_ok=True)

# Categorías de imágenes de fallback
categories = {
    "wormhole": "Un vórtice azul brillante en un espacio oscuro, estilo ciencia ficción", 
    "alien": "Una silueta extraterrestre con grandes ojos, estilo ciencia ficción minimalista",
    "time_machine": "Una máquina del tiempo con engranajes y luces, estilo retro futurista",
    "space": "Una vista del espacio profundo con estrellas y nebulosas brillantes",
    "spaceship": "Una nave espacial futurista con propulsores encendidos",
    "planet": "Un planeta alienígena con anillos y lunas, superficie exótica",
    "cosmic_default": "Una imagen cósmica abstracta con colores brillantes, nebulosas y estrellas"
}

def create_placeholder_image(filename, text):
    """Crea una imagen placeholder con texto simple"""
    img = Image.new('RGB', (800, 600), color=(20, 20, 40))
    d = ImageDraw.Draw(img)
    
    # Intentar cargar una fuente, de lo contrario usar la fuente predeterminada
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
    
    # Dibujar texto
    d.text((50, 250), f"Cosmic Chaos: {text}", fill=(200, 200, 255), font=font)
    d.text((50, 300), "Imagen de fallback", fill=(150, 150, 200), font=font)
    
    # Guardar la imagen
    img.save(os.path.join(FALLBACK_DIR, filename))
    print(f"Creada imagen placeholder: {filename}")

def generate_image_with_openai(prompt, filename):
    """Genera una imagen usando OpenAI DALL-E API"""
    if not API_KEY:
        print(f"No se encontró API_KEY de OpenAI. Creando imagen placeholder para {filename}")
        create_placeholder_image(filename, prompt)
        return
        
    try:
        client = OpenAI(api_key=API_KEY)
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"Genera una imagen de ciencia ficción de alta calidad que muestre: {prompt}. No incluir texto visible.",
            n=1,
            size="1024x1024"
        )
        
        # Obtener URL de la imagen generada
        image_url = response.data[0].url
        
        # Descargar la imagen
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # Guardar la imagen
            with open(os.path.join(FALLBACK_DIR, filename), 'wb') as f:
                f.write(image_response.content)
            print(f"Imagen generada con OpenAI guardada como: {filename}")
        else:
            print(f"Error descargando imagen generada: {image_response.status_code}")
            create_placeholder_image(filename, prompt)
    except Exception as e:
        print(f"Error generando imagen con OpenAI: {str(e)}")
        create_placeholder_image(filename, prompt)

def main():
    """Función principal para generar todas las imágenes de fallback"""
    print("Generando imágenes de fallback para Cosmic Chaos Adventure...")
    
    # Generar cada imagen
    for category, prompt in categories.items():
        filename = f"{category}.jpg"
        print(f"Generando imagen para: {category}")
        
        # Si la API_KEY está disponible, intentar generar con OpenAI
        if API_KEY:
            generate_image_with_openai(prompt, filename)
        else:
            create_placeholder_image(filename, prompt)
    
    print("Finalizado el proceso de generación de imágenes de fallback")

if __name__ == "__main__":
    main() 