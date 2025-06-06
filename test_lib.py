# Import des librairies pour les signaux PWM
import smbus2
import cobra_pca9685_v10_COBRAQUAGE as pca9685 #nom du fichier global

myi2cbus = smbus2.SMBus(1) # Initialisation du bus I2C
myPCA9685 = pca9685.PCA9685(myi2cbus) # Initialisation du générateur de PWM

# Import des librairies pour les signaux logiques/numériques
import RPi.GPIO as GPIO
import time

#numeros_moteurs = {"brushless": [1, 2, 3, 4, 5], "MCC": [6, 7]}

brushless = {}
mcc={}
# Instanciation des brushless et initialisation à vitesse nulle
brushless["d"] = pca9685.brushless(myPCA9685,1)
brushless["g"] = pca9685.brushless(myPCA9685,2)
brushless["c"] = pca9685.brushless(myPCA9685,3)
brushless["av"] = pca9685.brushless(myPCA9685,4)
brushless["ar"] = pca9685.brushless(myPCA9685,5)

# Instanciation des mcc et initialisation à vitesse nulle
#mcc['t']= pca9685.MCC(myPCA9685,6,24,23)
#mcc['p']= pca9685.MCC(myPCA9685,7,8,7)

#sens_mot11=GPIO24 - BROCHE 24
#sens_mot12=GPIO23 - BROCHE 26
#sens_mot21=GPIO8 - BROCHE 16
#sens_mot21=GPIO7 - BROCHE 18

print("Prêt - Initialisation réalisée")

# Boucle_continue/principale
while True :
   #TEST pour commande en VITESSE:
   choix=input("Brushless (b) ou mcc (m) ?")
   if choix=='b':
      nom_brushless=input("Donner nom brushless:")
      commande_vitesse_pourcentage_b=int(input("Donner la commande de vitesse du moteur en pourcentage (entre -100 et 100):"))
      brushless[nom_brushless].cmd_vit_pourcent(commande_vitesse_pourcentage_b)
   if choix=='m':
      nom_mcc=input("Donner nom mcc")
      commande_vitesse_pourcentage_m=int(input("Donner la commande de vitesse du moteur en pourcentage (entre -100 et 100):"))
      mcc[nom_mcc].cmd_vit_pourcent(commande_vitesse_pourcentage_m)
      
   #TEST pour commande en LARGEUR D'IMPULSION:
    #commande_vitesse_us=int(input("Donner la commande de temps haut du moteur en us (entre 0 et 5000):"))
    #myPCA9685.commande_moteur_vitesse_us(commandeb_vitesse_us,1)