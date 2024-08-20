import os
import subprocess
import sys

# Chemin de l'environnement virtuel
venv_path = 'venv'

# Vérifier si l'environnement virtuel existe
if not os.path.exists(venv_path):
    # Créer l'environnement virtuel s'il n'existe pas
    print(f"Création de l'environnement virtuel dans le dossier '{venv_path}'...")
    subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
else:
    print(f"L'environnement virtuel '{venv_path}' existe déjà.")

# Chemin vers l'interpréteur Python dans l'environnement virtuel
venv_python = os.path.join(venv_path, 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join(venv_path, 'bin', 'python')

# Installation des packages avec l'environnement virtuel
subprocess.check_call([venv_python, '-m', 'pip', 'install', '-r', 'requirements.txt'])

# Exécution du jeu en utilisant l'environnement virtuel
subprocess.check_call([venv_python, '-m', 'src.Game'])
