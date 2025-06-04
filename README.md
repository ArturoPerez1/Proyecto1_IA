# Proyecto: Predictor de Calidad de Vino 🍷

Este proyecto implementa un predictor de calidad de vino utilizando Machine Learning, con una interfaz gráfica de usuario (GUI) para la interacción. El desarrollo se divide en dos fases principales: el entrenamiento del modelo en Google Colab y la aplicación GUI en un entorno local (VS Code).

## Guía de Ejecución del Proyecto

Sigue los pasos a continuación para poner en marcha y ejecutar el proyecto.

### 1. Fase de Entrenamiento del Modelo (Google Colab)

Esta fase cubre la exploración de datos, preprocesamiento y entrenamiento del modelo de Machine Learning, aprovechando los recursos de Google Colab.

1.  **Abrir Google Colab:**
    * Navega a [colab.research.google.com](https://colab.research.google.com/).
    * Crea un nuevo Notebook (`File` > `New notebook`).

2.  **Cargar el Dataset:**
    * Necesitas el archivo `winequality-red.csv` (o `winequality-white.csv` si estás utilizando ese).
    * **Opción A (Recomendada - Persistente): Subir a Google Drive:**
        * Sube el archivo `winequality-red.csv` a tu Google Drive (ej. dentro de una carpeta `proyectos_ml`).
    * **Opción B (Temporal - Para la sesión actual de Colab):**
        * En el panel lateral izquierdo de Colab, haz clic en el icono de la carpeta (`Files`).
        * Haz clic en el icono de "Upload to session storage" (la flecha hacia arriba).
        * Selecciona tu archivo `winequality-red.csv`. Ten en cuenta que este archivo se borrará cuando la sesión de Colab finalice.

3.  **Copiar y Ejecutar el Código de Colab:**
    * Copia todo el código Python proporcionado para las Fases 1 y 2 (exploración, preprocesamiento con `KNNImputer` y `StandardScaler`, y entrenamiento del `RandomForestRegressor`). Este código incluye la lógica para guardar los preprocesadores y el modelo.
    * Pégalo en una celda de tu Notebook de Colab.
    * **¡MUY IMPORTANTE!:** En la línea `file_path_drive = '/content/drive/MyDrive/winequality-red.csv'`, **actualiza la ruta** para que apunte a la ubicación real de tu archivo CSV en Google Drive. Si lo subiste directamente a la sesión (Opción B), la ruta sería simplemente `winequality-red.csv`.
    * Ejecuta la celda (presiona `Shift + Enter` o haz clic en el botón de "Play").

4.  **Verificar la Ejecución en Colab:**
    * Observa la salida en el Notebook para asegurarte de que el dataset se cargue correctamente y el modelo se entrene sin errores.
    * Al final de la ejecución, deberías ver mensajes confirmando que los archivos `.joblib` (el modelo, el `imputer` y el `scaler`) han sido guardados exitosamente.

### 2. Descargar los Archivos `.joblib`

Estos archivos son el corazón de tu aplicación local, ya que contienen el modelo entrenado y los objetos de preprocesamiento.

1.  **Acceder a Google Drive:**
    * Abre tu Google Drive en el navegador web (la misma cuenta que usaste con Colab).
    * Navega a la carpeta donde Colab guardó los archivos (`wine_quality_imputer.joblib`, `wine_quality_scaler.joblib`, `wine_quality_model.joblib`). Por defecto, si usaste `/content/drive/MyDrive/`, estarán en la raíz de "Mi unidad" o en la subcarpeta que hayas especificado.

2.  **Descargar los Archivos:**
    * Selecciona los tres archivos `.joblib`.
    * Haz clic derecho sobre ellos y selecciona `Descargar`.
    * Guárdalos en una carpeta en tu computadora. Se recomienda crear una carpeta específica para este proyecto (ej. `C:\proyectos\wine_predictor_app` en Windows o `~/proyectos/wine_predictor_app` en macOS/Linux).

### 3. Crear Entorno Virtual en Python (Local)

Crear un entorno virtual es una buena práctica para aislar las dependencias de tu proyecto.

1.  **Abrir VS Code:**
    * Abre Visual Studio Code.
    * Ve a `File` > `Open Folder...` y selecciona la carpeta donde descargaste los archivos `.joblib` en el paso anterior.

2.  **Abrir la Terminal Integrada de VS Code:**
    * Ve a `Terminal` > `New Terminal` o usa el atajo de teclado (`Ctrl + Shift + Ñ` en Windows o ``Ctrl + Shift + ` `` en macOS/Linux). Asegúrate de que la terminal se inicie en la ruta raíz de la carpeta de tu proyecto.

3.  **Crear el Entorno Virtual:**
    * En la terminal, ejecuta el siguiente comando:
        ```bash
        python -m venv myenv
        ```
        (Puedes elegir un nombre diferente a `myenv` si lo deseas, por ejemplo, `venv`). Esto creará una subcarpeta llamada `myenv` dentro de tu directorio de proyecto.

4.  **Activar el Entorno Virtual:**
    * **En Windows (PowerShell):**
        ```bash
        .\myenv\Scripts\Activate.ps1
        ```
    * **En Windows (CMD):**
        ```bash
        .\myenv\Scripts\activate.bat
        ```
    * **En macOS/Linux:**
        ```bash
        source myenv/bin/activate
        ```
    * Deberías ver `(myenv)` (o el nombre que hayas elegido) al inicio de la línea de comandos de tu terminal, indicando que el entorno está activo.

5.  **Seleccionar el Intérprete de Python en VS Code:**
    * Haz clic en la versión de Python que se muestra en la **barra de estado azul inferior** de VS Code (normalmente en el lado izquierdo).
    * En la paleta de comandos que se abrirá en la parte superior, busca y selecciona el intérprete que corresponde a tu entorno virtual (ej. `Python 3.x.x ('myenv': venv)`). Esto configurará VS Code para usar el Python de tu entorno virtual en este proyecto.

### 4. Instalar las Librerías Necesarias (Local)

Con el entorno virtual activo en la terminal de VS Code:

1.  **Instala las librerías del proyecto:**
    ```bash
    pip install pandas scikit-learn matplotlib seaborn joblib
    ```
    * `tkinter` ya viene incluido con la instalación estándar de Python, por lo que no es necesario instalarlo por separado.

### 5. Correr el Proyecto (Aplicación GUI)

Finalmente, ejecutarás la aplicación de escritorio.

1.  **Crear el Archivo de la GUI:**
    * En VS Code, crea un nuevo archivo en la raíz de tu proyecto llamado `app_predictor_vino.py`.
    * Copia y pega el código completo de la aplicación GUI (el que incluye la interfaz Tkinter y la lógica de predicción) en este archivo.

2.  **Verificar Rutas de Archivos en la GUI:**
    * Abre `app_predictor_vino.py` y asegúrate de que las rutas a los archivos `.joblib` sean correctas. Si los guardaste en la misma carpeta que `app_predictor_vino.py`, las rutas por defecto ya deberían ser correctas:
        ```python
        MODEL_PATH = 'wine_quality_model.joblib'
        IMPUTER_PATH = 'wine_quality_imputer.joblib'
        SCALER_PATH = 'wine_quality_scaler.joblib'
        ```

3.  **Ejecutar la Aplicación:**
    * Asegúrate de que tu entorno virtual `(myenv)` esté activo en la terminal de VS Code.
    * Ejecuta el script de la aplicación:
        ```bash
        python app_predictor_vino.py
        ```
    * Deberías ver aparecer la ventana de tu aplicación "Wine Quality Predictor".

¡Ahora puedes interactuar con la aplicación, ingresar los parámetros del vino y obtener predicciones de calidad!
