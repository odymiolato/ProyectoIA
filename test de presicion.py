import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model

# Datos de prueba ficticios (sustitúyelos por datos reales si los tienes)
edad = 35
peso = 70
genero = 1  # 1 para masculino, 0 para femenino
sintomas = [1, 0, 1, 0, 0, 1, 0, 0, 0]  # Por ejemplo, [dolor de cabeza, fatiga, nauseas, ...]
habitos = [0, "regular", "saludable", {"horas_diarias": 8, "calidad": "buena"}, 1, 2000, "medio", True, "mucho", 1]  # Por ejemplo, [tabaco, actividad_fisica, dieta, sueno, consumo_alcohol, consumo_agua_diario, estres, ejercicio_mental, tiempo_aire_libre, consumo_cafeina]

# Preprocesamiento de datos
edad_peso_genero = [edad, peso, genero]
sintomas_habitos = sintomas + [1 if isinstance(habito, str) else 0 for habito in habitos[:4]] + [0 if isinstance(habito, str) else habito for habito in habitos[4:]]
X_prueba = np.array(edad_peso_genero + sintomas_habitos).reshape(1, -1)

# Normalización de características numéricas
scaler = StandardScaler()
X_prueba_scaled = scaler.fit_transform(X_prueba)

# Cargar el modelo entrenado
modelo_entrenado = load_model('modelo_entrenado_tf.h5')

# Ajustar la arquitectura del modelo para que coincida con las dimensiones de entrada
modelo_entrenado.layers[0].input_shape = (None, 22)

# Realizar la predicción
prediccion = modelo_entrenado.predict(X_prueba_scaled)

# Obtener el índice de la clase con mayor probabilidad (tratamiento preventivo)
indice_prediccion = np.argmax(prediccion)

# Definir la lista de tratamientos preventivos
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

# Imprimir el tratamiento preventivo predicho
print("Tratamiento preventivo recomendado:", tratamientos_preventivos[indice_prediccion])
