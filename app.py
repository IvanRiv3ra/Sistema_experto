from flask import Flask, request, render_template, redirect, url_for, session
from typing import Dict, List, Tuple
import json

# Clase KnowledgeBase - Representa la base de conocimientos del sistema experto
class KnowledgeBase:
    def __init__(self):
       # Diccionario con toda la información de cada carrera
        # Cada carrera tiene: descripción, áreas, habilidades requeridas, campo laboral, reglas y umbral mínimo
        self.carreras = {
            "Ingeniería en Sistemas Computacionales": {
                "descripcion": "Carrera enfocada en el desarrollo de software, sistemas informáticos y soluciones tecnológicas.",
                "areas": ["Programación", "Desarrollo web", "Inteligencia artificial", "Bases de datos"],
                "habilidades_requeridas": ["Lógica matemática", "Resolución de problemas", "Pensamiento analítico"],
                "campo_laboral": ["Empresas de tecnología", "Desarrollo de software", "Consultoría IT"],
                # Las reglas definen el peso o importancia de cada pregunta para esta carrera específica
                # Están organizadas por categoría (intereses, habilidades, conocimientos)
                "reglas": {
                    "intereses": {
                        "logica": 0.8,
                        "tecnologia": 0.9,
                        "programacion": 1.0,
                        "tecnicos": 0.7
                    },
                    "habilidades": {
                        "matematicas": 0.9,
                        "tecnicos": 0.8,
                        "investigacion": 0.6
                    },
                    "conocimientos": {
                        "programacion": 0.7,
                        "circuitos": 0.3
                    }
                },
                 # Umbral mínimo: porcentaje mínimo de compatibilidad requerido para recomendar esta carrera
                "umbral_minimo": 0.6
            },
            "Ingeniería Industrial": {
                "descripcion": "Carrera que optimiza procesos, sistemas y organizaciones para mejorar la eficiencia y productividad.",
                "areas": ["Logística", "Control de calidad", "Optimización de procesos", "Gestión de proyectos"],
                "habilidades_requeridas": ["Análisis de datos", "Liderazgo", "Organización"],
                "campo_laboral": ["Manufactura", "Logística", "Consultoría"],
                "reglas": {
                    "intereses": {
                        "procesos": 0.9,
                        "administrar": 0.8,
                        "logica": 0.6
                    },
                    "habilidades": {
                        "matematicas": 0.7,
                        "liderazgo": 0.8,
                        "administracion": 0.9,
                        "investigacion": 0.6
                    },
                    "conocimientos": {
                        "finanzas": 0.5
                    }
                },
                "umbral_minimo": 0.5
            },
            "Gastronomía": {
                "descripcion": "Carrera dedicada al arte culinario, la creación de platillos y la gestión de establecimientos de alimentos.",
                "areas": ["Cocina internacional", "Repostería", "Gestión de restaurantes", "Innovación culinaria"],
                "habilidades_requeridas": ["Creatividad", "Atención al detalle", "Trabajo bajo presión"],
                "campo_laboral": ["Restaurantes", "Hoteles", "Emprendimiento culinario"],
                "reglas": {
                    "intereses": {
                        "cocina": 1.0,
                        "creatividad": 0.8,
                        "manuales": 0.7
                    },
                    "habilidades": {
                        "creatividad": 0.9,
                        "manuales": 0.8,
                        "comunicacion": 0.6
                    },
                    "conocimientos": {
                        "culinarias": 0.8
                    }
                },
                "umbral_minimo": 0.5
            },
            "Ingeniería Mecatrónica": {
                "descripcion": "Carrera que combina mecánica, electrónica y programación para crear sistemas automatizados.",
                "areas": ["Robótica", "Automatización", "IoT", "Sistemas de control"],
                "habilidades_requeridas": ["Pensamiento lógico", "Programación", "Diseño mecánico"],
                "campo_laboral": ["Industria automotriz", "Automatización industrial", "Desarrollo de producto"],
                "reglas": {
                    "intereses": {
                        "robotica": 1.0,
                        "tecnologia": 0.8,
                        "logica": 0.7,
                        "tecnicos": 0.8
                    },
                    "habilidades": {
                        "matematicas": 0.8,
                        "tecnicos": 0.9,
                        "investigacion": 0.6
                    },
                    "conocimientos": {
                        "circuitos": 0.8,
                        "programacion": 0.7
                    }
                },
                "umbral_minimo": 0.6
            },
            "Administración de Empresas": {
                "descripcion": "Carrera enfocada en la gestión eficiente de organizaciones y recursos empresariales.",
                "areas": ["Finanzas", "Marketing", "Recursos humanos", "Emprendimiento"],
                "habilidades_requeridas": ["Liderazgo", "Comunicación", "Análisis financiero"],
                "campo_laboral": ["Empresas privadas", "Consultoría", "Emprendimiento"],
                "reglas": {
                    "intereses": {
                        "administrar": 1.0,
                        "procesos": 0.7,
                        "finanzas": 0.8
                    },
                    "habilidades": {
                        "liderazgo": 0.9,
                        "administracion": 0.9,
                        "comunicacion": 0.8
                    },
                    "conocimientos": {
                        "finanzas": 0.7
                    }
                },
                "umbral_minimo": 0.5
            },
            "Ingeniería Agrónoma": {
                "descripcion": "Carrera dedicada a mejorar la producción agrícola con técnicas sostenibles e innovadoras.",
                "areas": ["Agricultura de precisión", "Biotecnología", "Sistemas de riego", "Cultivos"],
                "habilidades_requeridas": ["Análisis de datos", "Investigación", "Trabajo de campo"],
                "campo_laboral": ["Empresas agrícolas", "Desarrollo rural", "Investigación"],
                "reglas": {
                    "intereses": {
                        "agricola": 1.0,
                        "medioambiente": 0.8,
                        "investigacion": 0.7
                    },
                    "habilidades": {
                        "investigacion": 0.9,
                        "manuales": 0.7,
                        "tecnicos": 0.6
                    },
                    "conocimientos": {
                        "agronomia": 0.8,
                        "medioambientesustentabilidad": 0.7
                    }
                },
                "umbral_minimo": 0.5
            },
            "Ingeniería Ambiental": {
                "descripcion": "Carrera enfocada en la protección del medio ambiente y el desarrollo de soluciones sostenibles.",
                "areas": ["Gestión de residuos", "Energías renovables", "Evaluación de impacto ambiental"],
                "habilidades_requeridas": ["Análisis científico", "Resolución de problemas", "Conciencia ecológica"],
                "campo_laboral": ["Consultorías ambientales", "Gobierno", "ONGs ambientales"],
                "reglas": {
                    "intereses": {
                        "medioambiente": 1.0,
                        "investigacion": 0.8,
                        "tecnicos": 0.6
                    },
                    "habilidades": {
                        "investigacion": 0.9,
                        "tecnicos": 0.7,
                        "matematicas": 0.6
                    },
                    "conocimientos": {
                        "medioambientesustentabilidad": 0.9
                    }
                },
                "umbral_minimo": 0.6
            },
            "Diseño Gráfico": {
                "descripcion": "Carrera dedicada a la comunicación visual y la creación de contenidos gráficos.",
                "areas": ["Diseño web", "Identidad corporativa", "Publicidad", "Animación"],
                "habilidades_requeridas": ["Creatividad", "Dominio técnico", "Comunicación visual"],
                "campo_laboral": ["Agencias de diseño", "Marketing", "Freelance"],
                "reglas": {
                    "intereses": {
                        "disenografico": 1.0,
                        "creatividad": 0.9,
                        "artistico": 0.8
                    },
                    "habilidades": {
                        "artistico": 0.9,
                        "creatividad": 0.9,
                        "comunicacion": 0.7
                    },
                    "conocimientos": {
                        "modelado3d": 0.7
                    }
                },
                "umbral_minimo": 0.5
            },
            "Arquitectura": {
                "descripcion": "Carrera enfocada en el diseño y planificación de espacios habitables y funcionales.",
                "areas": ["Diseño arquitectónico", "Urbanismo", "Restauración", "Arquitectura sostenible"],
                "habilidades_requeridas": ["Visión espacial", "Creatividad", "Pensamiento técnico"],
                "campo_laboral": ["Estudios de arquitectura", "Constructoras", "Consultoría"],
                "reglas": {
                    "intereses": {
                        "arquitectura": 1.0,
                        "disenografico": 0.7,
                        "artistico": 0.8
                    },
                    "habilidades": {
                        "artistico": 0.8,
                        "creatividad": 0.9,
                        "tecnicos": 0.7
                    },
                    "conocimientos": {
                        "arquitectonico": 0.9
                    }
                },
                "umbral_minimo": 0.6
            }
        }
        
        # Define pesos para cada categoría de preguntas
        # Estos valores indican la importancia relativa de cada tipo de pregunta en el cálculo final
        self.pesos_categorias = {
            "intereses": 0.4,
            "habilidades": 0.35,
            "conocimientos": 0.25
        }

# Clase InferenceEngine - Motor de inferencia que aplica las reglas para determinar compatibilidad
class InferenceEngine:
    def __init__(self, knowledge_base: KnowledgeBase):
        # Recibe y almacena una instancia de la base de conocimientos
        self.kb = knowledge_base

    # Método que evalúa una respuesta individual
    def evaluar_respuesta(self, respuesta: str, peso: float) -> float:
        # Si la respuesta es "si", retorna el peso completo; si es "no", retorna 0
       return peso if respuesta == "si" else 0
    
    # Método principal que aplica las reglas para calcular la compatibilidad con una carrera
    def aplicar_reglas(self, respuestas: Dict[str, str], carrera: str, datos_carrera: Dict) -> Tuple[float, List[str]]:
        puntuacion_total = 0
        reglas = datos_carrera["reglas"]

        # Itera sobre cada categoría (intereses, habilidades, conocimientos)
        for categoria, peso_categoria in self.kb.pesos_categorias.items():
            if categoria in reglas:
                suma_categoria = 0
                matches = 0
                # Para cada campo en esta categoría, evalúa la respuesta del usuario
                for campo, peso in reglas[categoria].items():
                    if campo in respuestas:
                        valor = self.evaluar_respuesta(respuestas[campo], peso)
                        suma_categoria += valor
                        if valor > 0:
                            matches += 1

                # Si hay al menos una coincidencia, calcula la puntuación para esta categoría
                if matches > 0:
                    # La puntuación se calcula como promedio de valores * peso de la categoría
                    puntuacion_categoria = (suma_categoria / len(reglas[categoria])) * peso_categoria
                    puntuacion_total += puntuacion_categoria

        # Calcula el porcentaje de compatibilidad final
        compatibilidad = (puntuacion_total / sum(self.kb.pesos_categorias.values())) * 100
        return compatibilidad

    # Método que evalúa todas las carreras y retorna las más compatibles
    def inferir_carreras(self, respuestas: Dict[str, str]) -> Dict[str, Dict]:
        resultados = {}

        # Itera sobre cada carrera en la base de conocimientos
        for carrera, datos in self.kb.carreras.items():
            # Calcula la compatibilidad para esta carrera
            compatibilidad = self.aplicar_reglas(respuestas, carrera, datos)
            
            # Si la compatibilidad supera el umbral mínimo, incluye la carrera en los resultados
            if compatibilidad >= datos["umbral_minimo"] * 100:
                resultados[carrera] = {
                    "compatibilidad": round(compatibilidad, 1), # Redondea a 1 decimal
                    "descripcion": datos["descripcion"],
                    "areas": datos["areas"],
                    "habilidades_requeridas": datos["habilidades_requeridas"],
                    "campo_laboral": datos["campo_laboral"]
                }

        # Ordena las carreras de mayor a menor compatibilidad
        return dict(sorted(
            resultados.items(),
            key=lambda item: item[1]["compatibilidad"],
            reverse=True
        ))

# Configuración de la aplicación Flask
app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = 'tu_clave_secreta'

# Inicializa la base de conocimientos y el motor de inferencia
knowledge_base = KnowledgeBase()
inference_engine = InferenceEngine(knowledge_base)

# Ruta principal - Muestra el formulario de evaluación
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Ruta para procesar el formulario enviado
@app.route('/analizar', methods=['POST'])
def analizar():
    if request.method == 'POST':
        # Obtiene las respuestas del formulario
        respuestas = dict(request.form)
        
        # Usa el motor de inferencia para determinar las carreras recomendadas
        resultados = inference_engine.inferir_carreras(respuestas)
        
        # Guarda los resultados en la sesión para mostrarlos en la página de resultados
        session['resultados'] = resultados
        
        # Redirige al usuario a la página de resultados
        return redirect(url_for('resultados'))
    
    return redirect(url_for('index'))

# Ruta para mostrar los resultados
@app.route('/resultados')
def resultados():
    # Verifica si hay resultados en la sesión
    if 'resultados' not in session:
        return redirect(url_for('index'))
    
    # Renderiza la plantilla de resultados con los datos guardados
    return render_template('resultados.html',
                         resultados=session['resultados'],
                         explicacion=session['explicacion'])

# Renderiza la plantilla de resultados con los datos guardados
if __name__ == '__main__':  
    app.run(debug=True) # Inicia el servidor en modo debug