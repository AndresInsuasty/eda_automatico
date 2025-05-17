# Dockerfile
# Base imágen ligera de Python
FROM python:3.11-slim

# Establece directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos (si lo usas) y el código
# Si no tienes requirements.txt, puedes eliminar esa línea e instalar con pip directamente
COPY requirements.txt ./
COPY app.py ./

# Instala dependencias sin cache para mantener la imagen ligera
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto por defecto de Streamlit
EXPOSE 8501

# Comando para ejecutar la app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]