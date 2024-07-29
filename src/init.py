import os
import requests
import shutil    
from config.config import *


def init():
    # Wird vom Hauptprogramm aufgerufen um umgebung einzurichten
    create_dirs()
    download_proxy_list()

def create_dirs():
    # Erstellt benötigte Verzeichnisse
    for dir_name, dir_path in DIRS.items():
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)


def download_proxy_list():
    # Lädt die Proxyliste herunter
    url = proxy_list_download
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(proxy_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Proxyliste erfolgreich heruntergeladen und in {proxy_file} gespeichert.")
    else:
        print(f"Fehler beim Herunterladen der Proxyliste: {response.status_code}")
    
