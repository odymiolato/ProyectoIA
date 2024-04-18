import random
from pymongo import MongoClient
from tqdm import tqdm
from datetime import datetime
now = datetime.now()

client = MongoClient('localhost', 27017)
db = client['IAtest']

analisis_predictivos = db['modelos_de_analisis']


relaciones_sintomas_enfermedades = [
    "Migraña", "Gripe", "Hipertensión",
    "Anemia", "Hipotiroidismo", "Depresión",
    "Gripe", "Embarazo", "Intoxicación alimentaria",
    "Vértigo", "Hipotensión", "Ansiedad",
    "Gastritis", "Apendicitis", "Colon irritable",
    "Infección viral", "Gripe", "Infección bacteriana",
    "Asma", "Neumonía", "EPOC",
    "Infarto de miocardio", "Angina de pecho", "Espasmo muscular",
    "Úlcera gástrica", "Hemorroides", "Cáncer de colon"
    ]



tratamientos_preventivos = [
    "Vacuna contra la gripe",
    "Aspirina para la prevención de enfermedades cardíacas",
    "Ejercicio regular",
    "Dieta rica en fibra para prevenir el cáncer de colon",
    "Exámenes de detección regulares para enfermedades crónicas",
    "Consumo de ácidos grasos omega-3 para la salud cardíaca",
    "Vacuna contra el virus del papiloma humano (VPH)",
    "Exámenes de la vista regulares para detectar problemas de salud ocular",
    "Vacunación contra la hepatitis B",
    "Consumo moderado de alcohol para la salud cardiovascular",
    "Uso de protector solar para prevenir el cáncer de piel",
    "Terapia de reemplazo hormonal para prevenir la osteoporosis en mujeres posmenopáusicas",
    "Exámenes de detección de cáncer de mama",
    "Uso de condones para prevenir enfermedades de transmisión sexual"
]

def generar_analisis_predictivo(paciente_id):
    analisis = {
        "paciente_id": paciente_id,
        "edad": random.randint(20,60),
        "peso": random.randint(90,300),
        "genero": random.choice(["m", "f"]),
        "sintomas": {
            "dolor_de_cabeza": random.choice([True,False]),
            "fatiga": random.choice([True,False]),
            "nauseas": random.choice([True,False]),
            "mareos": random.choice([True,False]),
            "dolor_abdominal": random.choice([True,False]),
            "fiebre": random.choice([True,False]),
            "dificultad_respirar": random.choice([True,False]),
            "dolor_pecho": random.choice([True,False]),
            "sangrado": random.choice([True,False])
        },
        "habitos":{
            "tabaco": {
                "frecuencia": random.choice([1, 0]),  # 1 para "sí", 0 para "no"
                "cantidad_diaria": random.randint(0,10)
            },
            "actividad_fisica": random.randint(0, 2),  # 0 para "regular", 1 para "irregular", 2 para "ninguna"
            "dieta": random.randint(0, 1),  # 0 para "saludable", 1 para "no saludable"
            "sueno": {
                "horas_diarias": random.randint(3,12),
                "calidad": random.choice(["buena","mala"])
            },
            "consumo_alcohol": {
                "frecuencia": random.choice([1, 0]),  # 1 para "sí", 0 para "no"
                "cantidad_diaria": random.randint(0,300)
            },
            "consumo_agua_diario": random.randint(100,3000), 
            "estres": random.randint(0, 2),  # 0 para "alto", 1 para "medio", 2 para "bajo"
            "ejercicio_mental": random.choice([True,False]),
            "tiempo_aire_libre": random.randint(0, 2),  # 0 para "regular", 1 para "poco", 2 para "mucho"
            "consumo_cafeina": {
                "frecuencia": random.choice([1, 0]),  # 1 para "si", 0 para "no"
                "cantidad_diaria": random.randint(0,400)
            }
        },
        "enfermedad": relaciones_sintomas_enfermedades[random.randint(0,26)],
        "tratamientos_preventivos": tratamientos_preventivos[random.randint(0,13)],
        "fecha_registro": now
    }
    return analisis



total_analisis = 100000 
batch_size = 1000
for _ in tqdm(range(0, total_analisis, batch_size)):
    batch = [generar_analisis_predictivo(random.randint(1, 100000)) for _ in range(batch_size)]
    analisis_predictivos.insert_many(batch)
