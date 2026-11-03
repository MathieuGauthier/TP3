import sys
import os

#__file__ = le fichier courant
absolute_file_path = os.path.abspath(__file__)
absolute_folder_path = os.path.dirname(absolute_file_path)
print(absolute_folder_path) # DEBUG

# Pour eviter de l'ajouter a chaque lancement.
if absolute_folder_path not in sys.path:
    sys.path.append(absolute_folder_path) # Ajoute le chemin du dossier courant au sys.path

import importlib
import animator
import ui

# Recharge les modules pour prendre en compte les modifications
importlib.reload(animator)
importlib.reload(ui)


def main():
    global tool_window
    try:
        tool_window.close()
    except Exception:
        pass
    tool_window = ui.UiAnimator()
    tool_window.show()

main()