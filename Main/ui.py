from PySide6.QtWidgets import (QGroupBox,QLabel,QSpinBox,QWidget,
                                QPushButton,QVBoxLayout,QGridLayout,QDoubleSpinBox)
import maya.cmds as cmds


class UiAnimator(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Animation")
        self.setMinimumWidth(400)
        self.build_ui()

    
    
    def build_ui(self):
        
        self.interface = QVBoxLayout(self)
        self.interface.setSpacing(10)


# -------------------------------------- Section du timing ----------------------------------------------

        # 1: Le groupe (Le contenant)
        groupe_temps = QGroupBox("Animation Timing")
        layout_temps = QGridLayout(groupe_temps)

        # 2 : La ligne pour la duree en frame + un spinbox pour choisir la valeur(intialise a 48)
        label_duration = QLabel("Duration (Frames) : ")
        self.spin_duration = QSpinBox()
        self.spin_duration.setRange(1, 10000)
        self.spin_duration.setValue(1)

        # 2.1 : A quelle frequence on ajoute une cle sur la ligne de temps
        label_step = QLabel("Steps (Frames) : ")
        self.spin_step = QSpinBox()
        self.spin_step.setRange(1, 10000)
        self.spin_step.setValue(1)

        # 3 : On place le tout dans une Grille
        layout_temps.addWidget(label_duration, 0, 0)
        layout_temps.addWidget(self.spin_duration, 0, 1)
        layout_temps.addWidget(label_step, 0, 2)
        layout_temps.addWidget(self.spin_step, 0, 3)




# --------------------------------------- Section des transform ----------------------------------------------
# J'utilise ma fonction d'optimisation pour ne pas répéter la formule du timing, je réduis le nombre de lignes de code.
# Ici je peux initialiser mes valeurs min et max de chaque groupe transform.


        group_translate, self.t_min, self.t_max = self.create_transform_group("Translate Parameters", -1, 1)
        group_rotate, self.r_min, self.r_max = self.create_transform_group("Rotate Parameters", -1, 1)
        group_scale, self.scale_min, self.scale_max = self.create_transform_group("Scale Parameters", 0.5, 1)


# ------------------------------------------ Section du bouton ------------------------------------------------

        generate_button = QPushButton("Generate animation")
        #generate_button.clicked.connect() # ici, le bouton va detenir la fonction qui detient le code de l'outil.

# ------------------------------------------- Le layout de l'interface -----------------------------------------
        # Fin : On ajoute ensuite a l'interface
        self.interface.addWidget(groupe_temps)
        self.interface.addWidget(group_translate)
        self.interface.addWidget(group_rotate)
        self.interface.addWidget(group_scale)
        self.interface.addWidget(generate_button)

 
# -------------------------------------------- Optimisation  ---------------------------------
# Comme le group translate, rotate et  scale son identique, je creer une fonction qui recoit ce qui change et retourne pour construire les groupes
# spins_min et spins_max sont deux listes vides. Chaque fois qu’on crée un spinbox, on le range dedans pour le retrouver plus tard.
#



    def create_transform_group(self, title, default_min, default_max):
        group = QGroupBox(title)
        layout = QGridLayout(group)
        layout.setContentsMargins(0,30,0,30)
        spins_min = []
        spins_max = []

        for column, axis in enumerate(["x", "y", "z"]): #column (X,Y,Z) = (O,1,2)
            
            # La ligne des minimums en premier. Elle comme a (0,0), alors meme si fois 2, toujours 0. Ensuite, 2 et apres 4.
            layout.addWidget(QLabel(f"min {axis} :"), 0, column * 2) # Axe X = occupe deux columns dans la grille, label = 1 et  spinbox = 2. A la ligne (row) 0.

            # Pour placer le spinbox juste à coté du QLabel (min), j'ajoute +1 au column*2 pour me tasser de 1.
            spin_min = QDoubleSpinBox() # Le spinmox du min est un Float.
            spin_min.setRange(-10000,10000)
            spin_min.setValue(default_min)
            spin_min.setFixedSize(100,25)
            layout.addWidget(spin_min, 0, column * 2 + 1)
            spins_min.append(spin_min)

            # La ligne des maximum en deuxieme, a le meme comportement, mais sur la row (1).
            layout.addWidget(QLabel(f"max {axis} :"), 1, column * 2) # Axe X = occupe de column dans la grille, label = 1 et  spinbox = 2. 
            spin_max = QDoubleSpinBox() # Le spinmox du max est un Float.
            spin_max.setRange(-10000,10000)
            spin_max.setValue(default_max)
            spin_max.setFixedSize(100,25)
            layout.addWidget(spin_max, 1, column * 2 + 1)
            spins_max.append(spin_max)

        return group, spins_min, spins_max # Je retourne ensuite le group et les 2 listes.




def main():
    global tool_window
    try:
        tool_window.close()
    except Exception:
        pass
    tool_window = UiAnimator()
    tool_window.show()

main()