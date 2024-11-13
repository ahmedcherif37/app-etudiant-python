# Dockerfile

# Utiliser une image de base pour Python
FROM python:3.9

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier de l'application et les fichiers de configuration
COPY app.py /app
COPY requirements.txt /app

# Copier le dossier templates pour inclure les fichiers HTML
COPY templates /app/templates

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port de l'application Flask
EXPOSE 5000

# Démarrer l'application Flask
CMD ["python", "app.py"]
