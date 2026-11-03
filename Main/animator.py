import random
import maya.cmds as cmds


attributes = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]  # Liste des attribute.

# ------------------------------------------- LA fonction qui va generer l'animation -----------------------------------------
def generate_animation(duration, step, t_min, t_max, r_min, r_max, scale_min, scale_max):

        
    # Etape 1 : Je regarde s'il y a une selection de fait avant tout. Si non, je renvoie un warning. ---------------------------
    selection = cmds.ls(selection=True, type="transform") # Je recupere la selection de l'utilisateur, mais je ne veux que les transforms.
    if not selection:
        cmds.warning("Sélectionne au moins un objet.")
        return
        


    # Etape 2 : J'etablie la longeur de mon animation.------------------------------------------------------------------------
    start = 0
    end = duration

    frames = list(range(start, end, step)) # Je cree une liste de INT. Le range va de start a end, avec un pas de step. 
    frames.append(end)  # Ajoute la dernière frame
    print(frames) # J'imprimme la liste des frames pour verifier que tout est ok. DEBUG

    cmds.playbackOptions(minTime=start, maxTime=end) # configurer la durée de l'animation


    # Etape 3: Je place les keyframes sur chaque objet selectionne ----------------------------------------------------------
    cmds.undoInfo(openChunk=True)
    try:
        
    # A chaque frame, pour l'objet selectionne, je place une keyframe random sur chaque axe (x,y,z) entre les valeurs min et max.
        for obj in selection:
            cmds.cutKey(obj, attribute=attributes,clear=True) # Supprime uniquement les keyframes sur les attributs de translation, rotation et scale pour l'objet sélectionné.
            
            for frame in frames:
                for i, axis in enumerate("xyz"):
                    cmds.setKeyframe(obj, attribute=f"t{axis}", value=random.uniform(t_min[i], t_max[i]), time=frame)
                    cmds.setKeyframe(obj, attribute=f"r{axis}", value=random.uniform(r_min[i], r_max[i]), time=frame)
                    cmds.setKeyframe(obj, attribute=f"s{axis}", value=random.uniform(scale_min[i], scale_max[i]), time=frame)

             # Je cherche la valeur au debut, et je la place a la fin pour que l'objet revienne a sa position initiale.
            for attr in attributes:
                first_value = cmds.getAttr(f"{obj}.{attr}", time=start) # Je recupere la valeur de l'attribut a la frame de debut.
                cmds.setKeyframe(obj, attribute=attr, value=first_value, time=end) # Je place la valeur de debut a la fin pour que l'objet revienne a sa position initiale.     


    finally:
        cmds.undoInfo(closeChunk=True)

# ------------------------------------------------------------------------------------------------------------------------------