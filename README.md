# CV_COBRA 
EL KASSIMI IBRAHIM :)


# Fichiers
## EchequierPhotos(.py)
  - **Entrée**
  - Le nombre d'images qu'on souhaite capturer (au moins 10).
 - Le nombre de caméras (1 ou 2) : Possibilité de capturer l'échequier par deux caméras en même temps.
- **Sortie**:
- Création d'un (ou deux) repértoire(s) contenant les images de l'échequier.


## Calibration(.py)
  - **Entrée:**
  - Le nom du répertoire contenant les images de l'échequier.
- **Sortie:**:
- Création d'un fichier txt contenant la matrice intrinsèque de la caméra et les coefficients de distorsion.

## Photos_resolution(.py)

- **Entrée:**
- Rien (pour le moment)
- **Sortie:**
-  Création d'unrépertoire contenant des images avec différentes résolutions


## temps_resolution(.py)

- **Entrée:**
- N: Le nombre d'expériences pour moyenner la durée de traitement.
- **Sortie**
- Création (ou ecriture sur ) d'un fichier txt (ex : V2_temps_resolution.txt) contenant:
- - La date de la mesure.
- - la caméra utilisée
- - les résultats des mesures.

## modele_cam(.py)

- **Entrée:**
- n: le port de la caméra utilisé (0 par défaut)
- **Sortie:**
- V2, V3 ou V3W (V3W: V3 WIDE)


## PositionCam(.py)

