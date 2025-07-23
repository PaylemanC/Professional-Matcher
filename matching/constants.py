"""
Constantes y patterns de términos comunes en ofertas laborales IT:
- Verbos de accion. 
- Soft skills.
- Frases relevantes.
"""

COMMON_ACTION_VERBS = [
    # Desarrollo y programacion
    'desarrollar', 'programar', 'codificar', 'implementar', 'crear',
    'diseñar', 'construir', 'estructurar', 'arquitectar', 'modelar',
    'integrar', 'conectar', 'migrar', 'actualizar', 'optimizar',
    'refactorizar', 'depurar', 'testear', 'probar', 'validar',
    'verificar', 'revisar', 'analizar', 'documentar', 'especificar',    
    # Gestion y liderazgo
    'gestionar', 'administrar', 'coordinar', 'supervisar', 'dirigir',
    'liderar', 'organizar', 'planificar', 'ejecutar', 'controlar',
    'monitorear', 'evaluar', 'supervisar', 'guiar', 'mentorizar',
    'capacitar', 'formar', 'entrenar', 'enseñar', 'facilitar',    
    # Comunicacion y colaboracion
    'comunicar', 'presentar', 'explicar', 'demostrar', 'colaborar',
    'participar', 'contribuir', 'apoyar', 'asistir', 'ayudar',
    'interactuar', 'negociar', 'persuadir', 'influir', 'convencer',    
    # Resolucion de problemas
    'resolver', 'solucionar', 'identificar', 'diagnosticar', 'investigar',
    'encontrar', 'descubrir', 'determinar', 'establecer', 'definir',
    'proponer', 'sugerir', 'recomendar', 'aconsejar', 'mejorar',
    'innovar', 'transformar', 'cambiar', 'adaptar', 'ajustar',    
    # Operaciones y mantenimiento
    'operar', 'mantener', 'configurar', 'instalar', 'desplegar',
    'implementar', 'automatizar', 'monitorizar', 'supervisar', 'controlar',
    'backup', 'respaldar', 'recuperar', 'restaurar', 'sincronizar',
    'actualizar', 'parchar', 'reparar', 'corregir', 'solucionar',    
    # Analisis y reporting
    'analizar', 'estudiar', 'examinar', 'investigar', 'evaluar',
    'medir', 'calcular', 'estimar', 'proyectar', 'predecir',
    'reportar', 'informar', 'documentar', 'registrar', 'rastrear',
    'monitorear', 'observar', 'revisar', 'auditar', 'verificar'
]

COMMON_SOFT_SKILLS = [
    # Comunicacion
    'comunicacion efectiva', 'comunicacion clara', 'comunicacion asertiva',
    'habilidades de comunicacion', 'comunicacion interpersonal',
    'comunicacion tecnica', 'documentacion tecnica',    
    # Liderazgo y gestion
    'liderazgo', 'liderazgo de equipos', 'gestion de equipos',
    'coordinacion de equipos', 'mentoring', 'coaching',
    'supervision', 'delegacion', 'toma de decisiones',
    'gestion de proyectos', 'planificacion estrategica',    
    # Pensamiento critico y resolucion de problemas
    'pensamiento critico', 'pensamiento analitico', 'resolucion de problemas',
    'analisis critico', 'analisis detallado', 'solucion de problemas',
    'creatividad', 'innovacion', 'pensamiento lateral',
    'razonamiento logico', 'capacidad de sintesis',    
    # Organizacion y gestion del tiempo
    'gestion del tiempo', 'organizacion personal', 'organizacion laboral',
    'planificacion', 'planificacion operativa', 'priorizacion',
    'multitarea', 'multi-tarea', 'eficiencia', 'productividad',
    'gestion de tareas', 'administracion del tiempo',    
    # Trabajo en equipo y colaboracion
    'trabajo en equipo', 'colaboracion', 'colaboracion efectiva',
    'espiritu de equipo', 'cooperacion', 'sinergia',
    'empatia', 'empatia profesional', 'inteligencia emocional',
    'relaciones interpersonales', 'networking',    
    # Adaptabilidad y flexibilidad
    'adaptabilidad', 'flexibilidad', 'versatilidad',
    'capacidad de adaptacion', 'apertura al cambio',
    'resiliencia', 'tolerancia a la frustracion',
    'manejo del estres', 'gestion del cambio',    
    # Orientacion a resultados y proactividad
    'orientacion a resultados', 'orientacion al logro',
    'proactividad', 'iniciativa', 'autonomia',
    'autonomia profesional', 'autodisciplina',
    'responsabilidad', 'compromiso', 'dedicacion',
    'perseverancia', 'determinacion',    
    # Aprendizaje y desarrollo
    'aprendizaje continuo', 'curiosidad intelectual',
    'capacidad de aprendizaje', 'autoformacion',
    'actualizacion profesional', 'desarrollo profesional',
    'mejora continua', 'crecimiento personal',    
    # Habilidades tecnicas blandas
    'atencion al detalle', 'precision', 'calidad',
    'orientacion a la calidad', 'metodologia',
    'pensamiento sistemico', 'vision estrategica',
    'orientacion al cliente', 'orientacion al usuario',
    'negociacion', 'persuasion', 'influencia'
]

SOFT_SKILL_PATTERNS = [
    r'comunicacion\s*(efectiva|clara|asertiva|interpersonal|tecnica)?',
    r'presentacion\s*(oral|escrita|publica)?',
    r'habilidades\s*de\s*comunicacion',
    r'liderazgo\s*(de\s*equipos?)?',
    r'gestion\s*de\s*equipos?',
    r'coordinacion\s*de\s*equipos?',
    r'mentoring|coaching',
    r'pensamiento\s*(critico|analitico|lateral)',
    r'resolucion\s*de\s*problemas',
    r'analisis\s*(critico|detallado)',
    r'toma\s*de\s*decisiones',
    r'gestion\s*del?\s*tiempo',
    r'organizacion\s*(personal|laboral)?',
    r'planificacion\s*(estrategica|operativa)?',
    r'multitarea|multi-tarea',
    r'trabajo\s*en\s*equipo',
    r'colaboracion\s*(efectiva)?',
    r'empatia\s*(profesional)?',
    r'adaptabilidad|flexibilidad',
    r'gestion\s*de\s*proyectos?',
    r'orientacion\s*a\s*(resultados|logro|calidad|cliente|usuario)',
    r'proactividad|iniciativa',
    r'autonomia\s*(profesional)?',
    r'aprendizaje\s*continuo',
    r'atencion\s*al\s*detalle',
    r'mejora\s*continua',
    r'inteligencia\s*emocional',
    r'pensamiento\s*sistemico',
    r'vision\s*estrategica'
]

RELEVANT_PHRASE_PATTERNS = [
    r'metodologia|metodologias|framework|frameworks',
    r'certificacion|certificaciones|titulo|titulos',
    r'testing|pruebas|qa|quality',
    r'devops|ci/cd|continuous|deployment',
    r'agile|agil|scrum|kanban',
    r'cloud|nube',
    r'api|rest|graphql|microservicio|soap',
    r'container',
    r'master|postgrado|especializacion|diplomado',
    r'pmp|itil|prince2|cobit',
    r'iso\s*27001|iso\s*9001',
    r'lean|six\s*sigma',
    r'design\s*thinking|design\s*patterns',
    r'unit\s*testing|integration\s*testing',
    r'tdd|bdd|ddd',
    r'automatizacion|robotizacion|scripting',
    r'big\s*data|data\s*science|machine\s*learning',
    r'inteligencia\s*artificial|ai|ml',
    r'analisis\s*de\s*datos|data\s*analytics',
    r'visualizacion\s*de\s*datos|data\s*visualization',
    r'gestion\s*de\s*datos|data\s*management',
    r'base\s*de\s*datos|database|db',
    r'patron\s*de\s*diseno|design\s*pattern',
    r'arquitectura|arquitectura\s*de\s*software|software\s*architecture',
    r'ingenieria|engineering|software\s*engineering',
    r'ciberseguridad|cybersecurity|seguridad\s*informatica',
    r'singleton|factory|observer|strategy|command|adapter|proxy|decorator\s',
    r'frontend|backend|full\s*stack|fullstack|fullstack',
    r'qa|quality\s*assurance|quality\s*control',
    r'(edtech|fintech|healthtech|legaltech|agrotech|biotech|paytech|insuretech|adtech|gamingtech|iot|blockchain|crypto)'
]
