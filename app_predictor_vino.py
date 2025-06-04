# app_predictor_vino.py

# Importar librerías necesarias
import tkinter as tk
from tkinter import ttk, messagebox
import joblib
import pandas as pd
import numpy as np

# --- 1. Carga del Modelo y Preprocesadores ---
# Las rutas a tus archivos .joblib. Asegúrate de que estén en la misma carpeta que este script
# o proporciona la ruta completa y correcta.
MODEL_PATH = 'modelos\wine_quality_model.joblib'
IMPUTER_PATH = 'modelos\wine_quality_imputer.joblib'
SCALER_PATH = 'modelos\wine_quality_scaler.joblib'

try:
    model = joblib.load(MODEL_PATH)
    imputer = joblib.load(IMPUTER_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("Modelo, Imputer y Scaler cargados exitosamente.")
except FileNotFoundError:
    messagebox.showerror("Error de Carga",
                         "No se encontraron los archivos del modelo o preprocesadores.\n"
                         "Asegúrate de que 'wine_quality_model.joblib', 'wine_quality_imputer.joblib' y "
                         "'wine_quality_scaler.joblib' estén en la misma carpeta que este script.")
    # Si los archivos no se encuentran, la aplicación no podrá funcionar correctamente.
    # Podrías considerar salir o deshabilitar funcionalidades. Por ahora, solo imprime un mensaje y sale.
    exit() # Salir de la aplicación si los archivos esenciales no se encuentran
except Exception as e:
    messagebox.showerror("Error de Carga", f"Ocurrió un error al cargar los archivos: {e}")
    exit()

# Definición de las características del vino (ordenadas como en el dataset)
FEATURES = [
    'fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
    'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
    'pH', 'sulphates', 'alcohol'
]

# --- 2. Funciones de Lógica de la Aplicación ---

def predict_quality():
    """
    Función que se ejecuta al presionar el botón "Predecir Calidad".
    Recoge las entradas del usuario, las preprocesa y realiza la predicción.
    """
    input_data = {}
    # 2.1 Recolectar datos del usuario
    for feature in FEATURES:
        # Obtener el valor de la entrada. Usamos .get() en el widget de entrada.
        # Quitamos espacios en blanco con .strip()
        value_str = entry_widgets[feature].get().strip()

        if value_str == "":
            # Si el campo está vacío, lo marcamos como NaN para que el imputer lo maneje.
            input_data[feature] = np.nan
        else:
            try:
                # Intentar convertir el valor a flotante.
                input_data[feature] = float(value_str)
            except ValueError:
                # Si no es un número válido, mostrar un error y detener la predicción.
                messagebox.showerror("Error de Entrada",
                                     f"El valor para '{feature}' no es un número válido. Por favor, corrígelo.")
                return # Detener la función si hay un error de validación

    # Convertir los datos de entrada a un DataFrame de Pandas
    # Esto es crucial para que el imputer y scaler puedan procesarlos correctamente.
    # Se crea un DataFrame con una sola fila.
    df_input = pd.DataFrame([input_data])

    # Asegurarse de que las columnas del DataFrame de entrada estén en el mismo orden que las características
    # usadas para entrenar el imputer y scaler.
    df_input = df_input[FEATURES]

    # 2.2 Manejo de Datos Ausentes: Imputación
    # Aplicar el imputer entrenado a los datos de entrada.
    # El imputer se ajustó en el X_train original y ahora imputa los NaNs en df_input.
    imputed_input = imputer.transform(df_input)

    # Convertir el array imputado de nuevo a DataFrame para mantener los nombres de las columnas
    # (aunque no es estrictamente necesario para el scaler si se mantiene el orden)
    imputed_df = pd.DataFrame(imputed_input, columns=FEATURES)

    # 2.3 Escalado de Características
    # Aplicar el scaler entrenado a los datos imputados.
    # El scaler se ajustó en X_train_imputed y ahora escala los datos de entrada.
    scaled_input = scaler.transform(imputed_df)

    # 2.4 Realizar Predicción
    # El modelo espera un array 2D, incluso si es una sola muestra.
    # predict() retorna un array, tomamos el primer elemento [0].
    predicted_quality = model.predict(scaled_input)[0]

    # Redondear la predicción a un número entero o con un decimal para mostrarla más limpia
    predicted_quality = round(predicted_quality, 2)

    # 2.5 Categorización Cualitativa de la Calidad
    # Definir umbrales para las categorías de calidad. Estos pueden ajustarse.
    # Comúnmente, la calidad del vino varía de 3 a 8 en el dataset.
    if predicted_quality < 5:
        qualitative_quality = "Malo"
    elif predicted_quality < 7:
        qualitative_quality = "Regular"
    else:
        qualitative_quality = "Bueno"

    # 2.6 Mostrar Resultados en la GUI
    result_label_score.config(text=f"Calidad Predicha (Score): {predicted_quality}")
    result_label_category.config(text=f"Categoría de Calidad: {qualitative_quality}")

    for feature_name in FEATURES:
        entry_widgets[feature_name].delete(0, tk.END)

# --- 3. Diseño e Implementación de la Interfaz Gráfica (GUI) ---

# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Wine Quality Predictor")
root.geometry("500x700") # Establecer un tamaño inicial de la ventana
root.resizable(False, False) # Evita que la ventana se pueda redimensionar

# Crear un Frame principal para un mejor control del layout
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Título de la aplicación
title_label = ttk.Label(main_frame, text="Predictor de Calidad de Vino", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Frame para las entradas de los parámetros fisicoquímicos
input_frame = ttk.LabelFrame(main_frame, text="Parámetros Fisicoquímicos del Vino", padding="10")
input_frame.pack(pady=10, fill=tk.X)

# Diccionario para almacenar las referencias a los widgets de entrada (Entry)
entry_widgets = {}
# Crear etiquetas y campos de entrada para cada característica
for i, feature in enumerate(FEATURES):
    row = i // 2 # 2 columnas por fila
    col = i % 2

    frame = ttk.Frame(input_frame)
    frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

    label = ttk.Label(frame, text=f"{feature.replace('_', ' ').title()}:")
    label.pack(side=tk.LEFT, padx=(0, 5))

    entry = ttk.Entry(frame, width=15)
    entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
    entry_widgets[feature] = entry # Guardar la referencia al widget de entrada

# Ajustar las columnas del input_frame para que se expandan proporcionalmente
input_frame.grid_columnconfigure(0, weight=1)
input_frame.grid_columnconfigure(1, weight=1)

# Botón para activar la predicción
predict_button = ttk.Button(main_frame, text="Predecir Calidad", command=predict_quality)
predict_button.pack(pady=20)

# Frame para mostrar los resultados
result_frame = ttk.LabelFrame(main_frame, text="Resultados de la Predicción", padding="10")
result_frame.pack(pady=10, fill=tk.X)

# Etiquetas para mostrar el puntaje numérico y la categoría cualitativa
result_label_score = ttk.Label(result_frame, text="Calidad Predicha (Score): -", font=("Arial", 12))
result_label_score.pack(pady=5)

result_label_category = ttk.Label(result_frame, text="Categoría de Calidad: -", font=("Arial", 12, "bold"))
result_label_category.pack(pady=5)

# Iniciar el bucle principal de la aplicación
root.mainloop()