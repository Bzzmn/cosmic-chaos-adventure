"""
Generador simple de preguntas de personalidad que no depende de langgraph o langchain.
Usado como alternativa cuando hay problemas de compatibilidad.
"""
from typing import Dict, Any, List
import asyncio
import random
import os
import uuid
from datetime import datetime

class SimplePersonalityGenerator:
    """
    Generador de preguntas de personalidad que usa datos predefinidos.
    Soporta preguntas en inglés y español.
    """
    def __init__(self):
        # Base URL para imágenes estáticas
        self.base_url = "http://localhost:8000"
        
        # Preguntas predefinidas por tema en español
        self.questions_es = {
            "viaje espacial": [
                {
                    "question": "Tu nave espacial ha detectado una anomalía gravitacional no registrada. ¿Qué haces?",
                    "scenario_description": "Estás pilotando una nave de exploración en un sector desconocido cuando los sensores detectan una distorsión espacio-temporal. Ninguna base de datos tiene registro de este fenómeno y parece ser completamente nuevo para la ciencia.",
                    "context_image": f"{self.base_url}/static/images/fallback/wormhole.webp",
                    "options": [
                        {"text": "Lanzar una sonda automatizada para investigar", "emoji": "🛰️", "value": 3, "effect": {"absurdity_resistance": 8, "quantum_charisma": 5}, "feedback": "Prudente pero curioso. La ciencia agradece tu contribución."},
                        {"text": "Pilotear directamente hacia la anomalía", "emoji": "🚀", "value": 4, "effect": {"time_warping": 12, "cosmic_luck": 8}, "feedback": "La audacia puede cambiar universos enteros."},
                        {"text": "Analizar desde distancia segura", "emoji": "🔭", "value": 2, "effect": {"absurdity_resistance": 10, "sarcasm_level": 6}, "feedback": "Sabio observador de las rarezas cósmicas."},
                        {"text": "Informar y alejarse inmediatamente", "emoji": "📡", "value": 1, "effect": {"absurdity_resistance": 12, "quantum_charisma": 2}, "feedback": "Vivir para contarlo. Prudencia interestelar."}
                    ]
                },
                {
                    "question": "Durante tu viaje interestelar, descubres un planeta con una civilización primitiva. ¿Qué decides?",
                    "scenario_description": "Tu nave realiza una parada en un planeta oceánico donde detectas una especie inteligente subacuática en sus primeras etapas tecnológicas. Tienen una cultura rica pero desconocen la existencia de vida extraterrestre.",
                    "context_image": f"{self.base_url}/static/images/fallback/planet.webp",
                    "options": [
                        {"text": "Establecer primer contacto oficial", "emoji": "🤝", "value": 4, "effect": {"quantum_charisma": 14, "time_warping": 4}, "feedback": "¡Embajador cósmico por excelencia!"},
                        {"text": "Estudiarlos en secreto", "emoji": "🔍", "value": 2, "effect": {"absurdity_resistance": 7, "sarcasm_level": 8}, "feedback": "Antropólogo espacial certificado."},
                        {"text": "Dejarles sutilmente tecnología", "emoji": "🎁", "value": 3, "effect": {"cosmic_luck": 9, "time_warping": 7}, "feedback": "Una semilla plantada en el cosmos."},
                        {"text": "Evitar interferencia y seguir tu viaje", "emoji": "🚫", "value": 1, "effect": {"absurdity_resistance": 10, "sarcasm_level": 5}, "feedback": "El observador silencioso. La galaxia lo agradece."}
                    ]
                }
            ],
            "encuentro alienígena": [
                {
                    "question": "Una delegación alienígena ofrece tecnología avanzada a cambio de arte humano. ¿Cómo respondes?",
                    "scenario_description": "Los Zephyritas, una especie alienígena altamente desarrollada, han establecido contacto y ofrecen compartir tecnología de viaje interestelar. Solo piden llevar consigo una colección representativa de arte humano, ya que son incapaces de crear arte propio.",
                    "context_image": f"{self.base_url}/static/images/fallback/alien.webp",
                    "options": [
                        {"text": "Ofrecer obras maestras históricas", "emoji": "🖼️", "value": 3, "effect": {"quantum_charisma": 8, "time_warping": 6}, "feedback": "Embajador cultural del patrimonio humano."},
                        {"text": "Crear nueva colección específica para ellos", "emoji": "🎨", "value": 4, "effect": {"quantum_charisma": 12, "absurdity_resistance": 9}, "feedback": "¡Inspirado innovador interdimensional!"},
                        {"text": "Solicitar más detalles sobre su tecnología", "emoji": "🔬", "value": 2, "effect": {"sarcasm_level": 9, "absurdity_resistance": 7}, "feedback": "Cauteloso y metódico. El universo es complejo."},
                        {"text": "Rechazar el intercambio", "emoji": "🚫", "value": 1, "effect": {"time_warping": 3, "absurdity_resistance": 12}, "feedback": "Conservador cultural. Valor en lo propio."}
                    ]
                },
                {
                    "question": "Descubres que un alienígena se oculta entre la población humana. ¿Qué haces?",
                    "scenario_description": "Has encontrado pruebas de que un ser de otro mundo vive bajo una identidad humana falsa. Parece inofensivo e incluso contribuye positivamente a la sociedad, pero su presencia viola los protocolos espaciales establecidos.",
                    "context_image": f"{self.base_url}/static/images/fallback/alien.webp",
                    "options": [
                        {"text": "Confrontarlo en privado", "emoji": "🤫", "value": 3, "effect": {"quantum_charisma": 9, "sarcasm_level": 6}, "feedback": "Diplomático espacial discreto."},
                        {"text": "Reportarlo a las autoridades", "emoji": "👮", "value": 1, "effect": {"absurdity_resistance": 10, "cosmic_luck": 3}, "feedback": "Seguir las reglas en un universo caótico."},
                        {"text": "Ofrecerle ayuda y protección", "emoji": "🛡️", "value": 4, "effect": {"quantum_charisma": 12, "cosmic_luck": 8}, "feedback": "Amigo cósmico universal."},
                        {"text": "Vigilarlo sin intervenir", "emoji": "👁️", "value": 2, "effect": {"sarcasm_level": 8, "time_warping": 7}, "feedback": "Observador cauteloso del ballet cósmico."}
                    ]
                }
            ],
            "paradoja temporal": [
                {
                    "question": "Encuentras un dispositivo que te permite ver 24 horas en el futuro. ¿Cómo lo usas?",
                    "scenario_description": "Un científico excéntrico te ha dejado un dispositivo cuántico que muestra exactamente lo que sucederá mañana. Funciona una vez al día y no puedes compartir lo que ves sin desencadenar una paradoja.",
                    "context_image": f"{self.base_url}/static/images/fallback/time_machine.webp",
                    "options": [
                        {"text": "Usarlo para prevenir accidentes", "emoji": "🚨", "value": 3, "effect": {"cosmic_luck": 10, "time_warping": 8}, "feedback": "Salvador temporal. El universo nota tus acciones."},
                        {"text": "Aprovecharlo para beneficio personal", "emoji": "💰", "value": 4, "effect": {"quantum_charisma": 6, "time_warping": 12}, "feedback": "Empresario cuántico. Tiempo es dinero."},
                        {"text": "Observar sin intervenir", "emoji": "👁️", "value": 2, "effect": {"absurdity_resistance": 9, "sarcasm_level": 7}, "feedback": "Testigo del tejido temporal."},
                        {"text": "Destruir el dispositivo", "emoji": "🔨", "value": 1, "effect": {"absurdity_resistance": 12, "quantum_charisma": 3}, "feedback": "Guardián natural del flujo temporal."}
                    ]
                },
                {
                    "question": "Te encuentras atrapado en un bucle temporal. ¿Cómo reaccionas?",
                    "scenario_description": "Estás viviendo el mismo día una y otra vez. Nadie más parece ser consciente del fenómeno, y todas tus acciones se reinician al final del día. Ya has repetido este día 42 veces.",
                    "context_image": f"{self.base_url}/static/images/fallback/time_machine.webp",
                    "options": [
                        {"text": "Aprender una habilidad nueva cada día", "emoji": "🧠", "value": 3, "effect": {"quantum_charisma": 8, "absurdity_resistance": 10}, "feedback": "Maestro del tiempo infinito."},
                        {"text": "Buscar patrones que rompan el bucle", "emoji": "🔍", "value": 4, "effect": {"time_warping": 14, "sarcasm_level": 6}, "feedback": "Detective cuántico extraordinario."},
                        {"text": "Experimentar sin preocuparte por consecuencias", "emoji": "🎭", "value": 2, "effect": {"sarcasm_level": 9, "cosmic_luck": 7}, "feedback": "Caos controlado. Experimenta y adapta."},
                        {"text": "Mantener una rutina estricta", "emoji": "📋", "value": 1, "effect": {"absurdity_resistance": 12, "time_warping": 4}, "feedback": "Orden en el caos temporal."}
                    ]
                }
            ],
            "colonización espacial": [
                {
                    "question": "Lideras una misión de colonización y descubres que el planeta ya tiene vida microscópica. ¿Qué decisión tomas?",
                    "scenario_description": "Tu colonia está lista para establecerse en un planeta aparentemente habitable, pero los análisis revelan microorganismos nativos. Reubicar la colonia costaría vidas y recursos, pero continuar podría afectar el ecosistema extraterrestre.",
                    "context_image": f"{self.base_url}/static/images/fallback/spaceship.webp",
                    "options": [
                        {"text": "Establecer zonas de coexistencia controlada", "emoji": "🔄", "value": 3, "effect": {"quantum_charisma": 9, "absurdity_resistance": 8}, "feedback": "Diplomático microbiano interplanetario."},
                        {"text": "Reubicar la colonia a otro planeta", "emoji": "🚀", "value": 1, "effect": {"absurdity_resistance": 12, "cosmic_luck": 5}, "feedback": "Protector primordial. La vida es sagrada."},
                        {"text": "Modificar genéticamente a los colonos para adaptarse", "emoji": "🧬", "value": 4, "effect": {"time_warping": 10, "quantum_charisma": 8}, "feedback": "Revolucionario evolucionario cósmico."},
                        {"text": "Establecer la colonia en órbita", "emoji": "🛰️", "value": 2, "effect": {"sarcasm_level": 7, "time_warping": 6}, "feedback": "Compromiso astuto entre mundos."}
                    ]
                },
                {
                    "question": "La colonia espacial que lideras enfrenta recursos limitados. ¿Cómo los administras?",
                    "scenario_description": "Tu asentamiento en el borde exterior tiene suministros para seis meses. La nave de reabastecimiento se ha retrasado y no hay garantía de cuándo llegará. Las tensiones aumentan entre los 500 colonos.",
                    "context_image": f"{self.base_url}/static/images/fallback/space.webp",
                    "options": [
                        {"text": "Implementar racionamiento estricto", "emoji": "📊", "value": 2, "effect": {"absurdity_resistance": 9, "sarcasm_level": 5}, "feedback": "Administrador espacial pragmático."},
                        {"text": "Enviar misión para encontrar recursos", "emoji": "🔍", "value": 3, "effect": {"cosmic_luck": 8, "quantum_charisma": 7}, "feedback": "Explorador adaptable. El espacio provee."},
                        {"text": "Desarrollar tecnología de autosuficiencia", "emoji": "🌱", "value": 4, "effect": {"time_warping": 9, "quantum_charisma": 10}, "feedback": "Innovador estelar visionario."},
                        {"text": "Hibernar a parte de la población", "emoji": "❄️", "value": 1, "effect": {"absurdity_resistance": 10, "cosmic_luck": 3}, "feedback": "Pragmático glacial. Las decisiones difíciles definen líderes."}
                    ]
                }
            ]
        }
        
        # Preguntas predefinidas por tema en inglés
        self.questions_en = {
            "space travel": [
                {
                    "question": "Your spaceship has detected an unregistered gravitational anomaly. What do you do?",
                    "scenario_description": "You're piloting an exploration vessel in an unknown sector when sensors detect a space-time distortion. No database has any record of this phenomenon and it appears to be completely new to science.",
                    "context_image": f"{self.base_url}/static/images/fallback/wormhole.webp",
                    "options": [
                        {"text": "Launch an automated probe to investigate", "emoji": "🛰️", "value": 3, "effect": {"absurdity_resistance": 8, "quantum_charisma": 5}, "feedback": "Cautious yet curious. Science appreciates your contribution."},
                        {"text": "Pilot directly toward the anomaly", "emoji": "🚀", "value": 4, "effect": {"time_warping": 12, "cosmic_luck": 8}, "feedback": "Boldness can change entire universes."},
                        {"text": "Analyze from a safe distance", "emoji": "🔭", "value": 2, "effect": {"absurdity_resistance": 10, "sarcasm_level": 6}, "feedback": "Wise observer of cosmic oddities."},
                        {"text": "Report and immediately move away", "emoji": "📡", "value": 1, "effect": {"absurdity_resistance": 12, "quantum_charisma": 2}, "feedback": "Live to tell the tale. Interstellar prudence."}
                    ]
                },
                {
                    "question": "During your interstellar journey, you discover a planet with a primitive civilization. What do you decide?",
                    "scenario_description": "Your ship makes a stop at an oceanic planet where you detect an intelligent underwater species in its early technological stages. They have a rich culture but are unaware of the existence of extraterrestrial life.",
                    "context_image": f"{self.base_url}/static/images/fallback/planet.webp",
                    "options": [
                        {"text": "Establish official first contact", "emoji": "🤝", "value": 4, "effect": {"quantum_charisma": 14, "time_warping": 4}, "feedback": "Cosmic ambassador par excellence!"},
                        {"text": "Study them in secret", "emoji": "🔍", "value": 2, "effect": {"absurdity_resistance": 7, "sarcasm_level": 8}, "feedback": "Certified space anthropologist."},
                        {"text": "Subtly leave them technology", "emoji": "🎁", "value": 3, "effect": {"cosmic_luck": 9, "time_warping": 7}, "feedback": "A seed planted in the cosmos."},
                        {"text": "Avoid interference and continue your journey", "emoji": "🚫", "value": 1, "effect": {"absurdity_resistance": 10, "sarcasm_level": 5}, "feedback": "The silent observer. The galaxy thanks you."}
                    ]
                }
            ],
            "alien encounter": [
                {
                    "question": "An alien delegation offers advanced technology in exchange for human art. How do you respond?",
                    "scenario_description": "The Zephyrites, a highly developed alien species, have established contact and offer to share interstellar travel technology. They only ask to take with them a representative collection of human art, as they are unable to create art themselves.",
                    "context_image": f"{self.base_url}/static/images/fallback/alien.webp",
                    "options": [
                        {"text": "Offer historical masterpieces", "emoji": "🖼️", "value": 3, "effect": {"quantum_charisma": 8, "time_warping": 6}, "feedback": "Cultural ambassador of human heritage."},
                        {"text": "Create a new collection specifically for them", "emoji": "🎨", "value": 4, "effect": {"quantum_charisma": 12, "absurdity_resistance": 9}, "feedback": "Inspired interdimensional innovator!"},
                        {"text": "Request more details about their technology", "emoji": "🔬", "value": 2, "effect": {"sarcasm_level": 9, "absurdity_resistance": 7}, "feedback": "Cautious and methodical. The universe is complex."},
                        {"text": "Reject the exchange", "emoji": "🚫", "value": 1, "effect": {"time_warping": 3, "absurdity_resistance": 12}, "feedback": "Cultural conservative. Value in what's yours."}
                    ]
                },
                {
                    "question": "You discover an alien hiding among the human population. What do you do?",
                    "scenario_description": "You've found evidence that a being from another world is living under a false human identity. They seem harmless and even contribute positively to society, but their presence violates established space protocols.",
                    "context_image": f"{self.base_url}/static/images/fallback/alien.webp",
                    "options": [
                        {"text": "Confront them in private", "emoji": "🤫", "value": 3, "effect": {"quantum_charisma": 9, "sarcasm_level": 6}, "feedback": "Discreet space diplomat."},
                        {"text": "Report them to the authorities", "emoji": "👮", "value": 1, "effect": {"absurdity_resistance": 10, "cosmic_luck": 3}, "feedback": "Following rules in a chaotic universe."},
                        {"text": "Offer them help and protection", "emoji": "🛡️", "value": 4, "effect": {"quantum_charisma": 12, "cosmic_luck": 8}, "feedback": "Universal cosmic friend."},
                        {"text": "Watch them without intervening", "emoji": "👁️", "value": 2, "effect": {"sarcasm_level": 8, "time_warping": 7}, "feedback": "Cautious observer of the cosmic ballet."}
                    ]
                }
            ],
            "time paradox": [
                {
                    "question": "You find a device that allows you to see 24 hours into the future. How do you use it?",
                    "scenario_description": "An eccentric scientist has left you a quantum device that shows exactly what will happen tomorrow. It works once a day and you cannot share what you see without triggering a paradox.",
                    "context_image": f"{self.base_url}/static/images/fallback/time_machine.webp",
                    "options": [
                        {"text": "Use it to prevent accidents", "emoji": "🚨", "value": 3, "effect": {"cosmic_luck": 10, "time_warping": 8}, "feedback": "Temporal savior. The universe notices your actions."},
                        {"text": "Use it for personal gain", "emoji": "💰", "value": 4, "effect": {"quantum_charisma": 6, "time_warping": 12}, "feedback": "Quantum entrepreneur. Time is money."},
                        {"text": "Observe without intervening", "emoji": "👁️", "value": 2, "effect": {"absurdity_resistance": 9, "sarcasm_level": 7}, "feedback": "Witness to the temporal fabric."},
                        {"text": "Destroy the device", "emoji": "🔨", "value": 1, "effect": {"absurdity_resistance": 12, "quantum_charisma": 3}, "feedback": "Natural guardian of temporal flow."}
                    ]
                },
                {
                    "question": "You find yourself trapped in a time loop. How do you react?",
                    "scenario_description": "You're living the same day over and over again. No one else seems to be aware of the phenomenon, and all your actions reset at the end of the day. You've already repeated this day 42 times.",
                    "context_image": f"{self.base_url}/static/images/fallback/time_machine.webp",
                    "options": [
                        {"text": "Learn a new skill every day", "emoji": "🧠", "value": 3, "effect": {"quantum_charisma": 8, "absurdity_resistance": 10}, "feedback": "Master of infinite time."},
                        {"text": "Look for patterns that break the loop", "emoji": "🔍", "value": 4, "effect": {"time_warping": 14, "sarcasm_level": 6}, "feedback": "Extraordinary quantum detective."},
                        {"text": "Experiment without worrying about consequences", "emoji": "🎭", "value": 2, "effect": {"sarcasm_level": 9, "cosmic_luck": 7}, "feedback": "Controlled chaos. Experiment and adapt."},
                        {"text": "Maintain a strict routine", "emoji": "📋", "value": 1, "effect": {"absurdity_resistance": 12, "time_warping": 4}, "feedback": "Order in temporal chaos."}
                    ]
                }
            ],
            "space colonization": [
                {
                    "question": "You lead a colonization mission and discover the planet already has microscopic life. What decision do you make?",
                    "scenario_description": "Your colony is ready to settle on a seemingly habitable planet, but analyses reveal native microorganisms. Relocating the colony would cost lives and resources, but continuing could affect the extraterrestrial ecosystem.",
                    "context_image": f"{self.base_url}/static/images/fallback/spaceship.webp",
                    "options": [
                        {"text": "Establish controlled coexistence zones", "emoji": "🔄", "value": 3, "effect": {"quantum_charisma": 9, "absurdity_resistance": 8}, "feedback": "Interplanetary microbial diplomat."},
                        {"text": "Relocate the colony to another planet", "emoji": "🚀", "value": 1, "effect": {"absurdity_resistance": 12, "cosmic_luck": 5}, "feedback": "Primordial protector. Life is sacred."},
                        {"text": "Genetically modify the colonists to adapt", "emoji": "🧬", "value": 4, "effect": {"time_warping": 10, "quantum_charisma": 8}, "feedback": "Cosmic evolutionary revolutionary."},
                        {"text": "Establish the colony in orbit", "emoji": "🛰️", "value": 2, "effect": {"sarcasm_level": 7, "time_warping": 6}, "feedback": "Clever compromise between worlds."}
                    ]
                },
                {
                    "question": "The space colony you lead faces limited resources. How do you manage them?",
                    "scenario_description": "Your settlement on the outer rim has supplies for six months. The resupply ship is delayed and there's no guarantee when it will arrive. Tensions are rising among the 500 colonists.",
                    "context_image": f"{self.base_url}/static/images/fallback/space.webp",
                    "options": [
                        {"text": "Implement strict rationing", "emoji": "📊", "value": 2, "effect": {"absurdity_resistance": 9, "sarcasm_level": 5}, "feedback": "Pragmatic space administrator."},
                        {"text": "Send a mission to find resources", "emoji": "🔍", "value": 3, "effect": {"cosmic_luck": 8, "quantum_charisma": 7}, "feedback": "Adaptable explorer. Space provides."},
                        {"text": "Develop self-sufficiency technology", "emoji": "🌱", "value": 4, "effect": {"time_warping": 9, "quantum_charisma": 10}, "feedback": "Visionary stellar innovator."},
                        {"text": "Hibernate part of the population", "emoji": "❄️", "value": 1, "effect": {"absurdity_resistance": 10, "cosmic_luck": 3}, "feedback": "Glacial pragmatist. Difficult decisions define leaders."}
                    ]
                }
            ]
        }
        
        # Mapeo de temas de español a inglés
        self.theme_mapping = {
            "viaje espacial": "space travel",
            "encuentro alienígena": "alien encounter",
            "paradoja temporal": "time paradox",
            "colonización espacial": "space colonization"
        }
    
    async def generate_personality_question(self, theme: str, lang: str = "en") -> Dict[str, Any]:
        """
        Genera una pregunta de personalidad basada en un tema y el idioma solicitado
        
        Args:
            theme: Tema para la pregunta
            lang: Idioma ('en' para inglés, 'es' para español)
            
        Returns:
            Diccionario con la estructura de la pregunta
        """
        # Simular pequeño retraso para que parezca que está generando
        await asyncio.sleep(0.5)
        
        # Determinar qué conjunto de preguntas usar según el idioma
        if lang.lower() == "es":
            questions = self.questions_es
            theme_to_use = theme
        else:
            questions = self.questions_en
            # Si el tema está en español, traducirlo a inglés
            theme_to_use = self.theme_mapping.get(theme, theme)
        
        # Si el tema existe, seleccionar una pregunta aleatoria
        if theme_to_use in questions and questions[theme_to_use]:
            return random.choice(questions[theme_to_use])
        
        # Si el tema no existe o no hay preguntas, usar fallback
        return self.generate_fallback_question(theme, lang)
    
    def generate_fallback_question(self, theme: str, lang: str = "en") -> Dict[str, Any]:
        """
        Genera una pregunta de fallback cuando el tema no existe
        
        Args:
            theme: Tema para la pregunta
            lang: Idioma ('en' para inglés, 'es' para español)
            
        Returns:
            Diccionario con estructura de pregunta
        """
        if lang.lower() == "es":
            return {
                "question": f"Pregunta fallback sobre {theme}",
                "context_image": f"{self.base_url}/static/images/fallback/cosmic_default.webp",
                "scenario_description": f"Descripción fallback de escenario sobre {theme}.",
                "options": [
                    {"text": f"Opción fallback 1 para {theme}", "emoji": "🚀", "value": 4, "effect": {"quantum_charisma": 10}, "feedback": f"Feedback fallback 1 para {theme}"},
                    {"text": f"Opción fallback 2 para {theme}", "emoji": "🔭", "value": 3, "effect": {"absurdity_resistance": 8}, "feedback": f"Feedback fallback 2 para {theme}"},
                    {"text": f"Opción fallback 3 para {theme}", "emoji": "🌌", "value": 2, "effect": {"time_warping": 12}, "feedback": f"Feedback fallback 3 para {theme}"},
                    {"text": f"Opción fallback 4 para {theme}", "emoji": "🛰️", "value": 1, "effect": {"cosmic_luck": 5}, "feedback": f"Feedback fallback 4 para {theme}"}
                ]
            }
        else:
            return {
                "question": f"Fallback question about {theme}",
                "context_image": f"{self.base_url}/static/images/fallback/cosmic_default.webp",
                "scenario_description": f"Fallback scenario description about {theme}.",
                "options": [
                    {"text": f"Fallback option 1 for {theme}", "emoji": "🚀", "value": 4, "effect": {"quantum_charisma": 10}, "feedback": f"Fallback feedback 1 for {theme}"},
                    {"text": f"Fallback option 2 for {theme}", "emoji": "🔭", "value": 3, "effect": {"absurdity_resistance": 8}, "feedback": f"Fallback feedback 2 for {theme}"},
                    {"text": f"Fallback option 3 for {theme}", "emoji": "🌌", "value": 2, "effect": {"time_warping": 12}, "feedback": f"Fallback feedback 3 for {theme}"},
                    {"text": f"Fallback option 4 for {theme}", "emoji": "🛰️", "value": 1, "effect": {"cosmic_luck": 5}, "feedback": f"Fallback feedback 4 for {theme}"}
                ]
            }

# Instancia global del generador
generator = SimplePersonalityGenerator()

# Función para generar una pregunta (API pública del módulo)
async def generate_personality_question(theme: str, lang: str = "en") -> Dict[str, Any]:
    """
    Genera una pregunta de personalidad basada en un tema y el idioma solicitado
    
    Args:
        theme: Tema para la pregunta
        lang: Idioma ('en' para inglés, 'es' para español)
        
    Returns:
        Diccionario con la estructura de la pregunta
    """
    return await generator.generate_personality_question(theme, lang)
    
# Función para generar una pregunta de fallback (API pública del módulo)
def generate_fallback_question(theme: str, lang: str = "en") -> Dict[str, Any]:
    """
    Genera una pregunta de fallback
    
    Args:
        theme: Tema para la pregunta
        lang: Idioma ('en' para inglés, 'es' para español)
        
    Returns:
        Diccionario con estructura de pregunta
    """
    return generator.generate_fallback_question(theme, lang) 