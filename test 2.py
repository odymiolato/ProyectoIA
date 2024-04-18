import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import pymongo
import tensorflow as tf

# Conexión a la base de datos MongoDB
client = pymongo.MongoClient('localhost', 27017)
db = client['IAtest']
modelos_de_analisis = db['modelos_de_analisis']

# Definición de tratamientos preventivos
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

# Obtener datos de la base de datos
modelo_de_analisis = list(modelos_de_analisis.find())

X = []
y = []

for datos in modelo_de_analisis:
    # Extraer características del paciente
    edad = datos['edad']
    peso = datos['peso']
    genero = 1 if datos['genero'] == "m" else 0

    # Codificar síntomas
    sintomas = datos["sintomas"]
    sintomas_codificados = [1 if sintoma else 0 for sintoma in sintomas.values()]

    # Concatenar características del paciente
    caracteristicas_paciente = [edad, peso, genero] + sintomas_codificados
    X.append(caracteristicas_paciente)

    # Obtener índice del tratamiento preventivo
    tratamiento_index = tratamientos_preventivos.index(datos['tratamientos_preventivos'])
    y.append(tratamiento_index)

X = np.array(X)
y = np.array(y)

# Dividir datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalizar características numéricas
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train[:, :3])  # Solo las características numéricas
X_test_scaled = scaler.transform(X_test[:, :3])  # Solo las características numéricas

# Crear modelo de redes neuronales con TensorFlow
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(3,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(len(tratamientos_preventivos), activation='softmax')
])

# Compilar modelo
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Entrenar modelo
model.fit(X_train_scaled, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Evaluar modelo en conjunto de prueba
test_loss, test_acc = model.evaluate(X_test_scaled, y_test)
print('Precisión del modelo en el conjunto de prueba:', test_acc)

# Guardar modelo entrenado
# Guardar modelo entrenado
model.save('modelo_entrenado_tf.h5')
print("Modelo entrenado guardado con éxito en 'modelo_entrenado_tf.h5'.")

