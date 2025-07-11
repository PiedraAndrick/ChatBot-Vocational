# Utiliza la imagen base oficial de Python 3.12 en Bullseye
FROM python:3.12-bullseye

# Desactiva el almacenamiento en búfer de salida de Python (opcional)
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /code

# Copia el archivo de requerimientos al contenedor
COPY ./requirements.txt /code/requirements.txt

# Actualiza pip a la última versión
RUN pip install --upgrade pip

# Instala las dependencias sin usar la caché para reducir el tamaño de la imagen
RUN pip install --no-cache-dir -r /code/requirements.txt

# Remueve el archivo de requerimientos para mantener la imagen limpia (opcional)
RUN rm /code/requirements.txt

# Copia el código de la aplicación al contenedor
COPY ./app /code/app

#Copia los certificados SSL al contenedor
COPY ./certificados/selfsigned.crt /code/certs/selfsigned.crt
COPY ./certificados/selfsigned.key /code/private/selfsigned.key

# Expon el puerto en el que correrá la aplicación
EXPOSE 8000
EXPOSE 443

# Crea un usuario sin privilegios para ejecutar la aplicación (opcional)
RUN useradd -m myuser

RUN chown -R myuser:myuser /code/certs/selfsigned.crt
RUN chown -R myuser:myuser /code/private/selfsigned.key

USER myuser


# Comando por defecto para ejecutar la aplicación
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile=/code/private/selfsigned.key", "--ssl-certfile=/code/certs/selfsigned.crt"]