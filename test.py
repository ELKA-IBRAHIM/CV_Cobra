from picamera2 import Picamera2
import time

# Initialiser la caméra
picam2 = Picamera2(1)
print(picam2)

# Configurer en mode photo
picam2.configure(picam2.create_still_configuration())

# Démarrer la caméra et attendre qu'elle soit prête
picam2.start()
time.sleep(2)  # Attendre 2 secondes pour stabiliser la caméra

# Capturer l’image et l’enregistrer
nom_image = "image.jpg"
picam2.capture_file(nom_image)

print(f"Image enregistrée sous : {nom_image}")

# Arrêter la caméra
picam2.stop()
