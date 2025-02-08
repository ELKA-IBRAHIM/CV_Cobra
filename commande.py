# -*- coding: utf-8 -*-
"""
Code de SALMA BAIRAT

"""
#La bibliothèque que nous avons écrite se base sur la bibliothèque adafruit_servokit

import smbus  
import time
import numpy as np
#from adafruit_servokit import ServoKit #pour utiliser composant PCA9685
#kit = ServoKit(channels=16)
import warnings

bus = smbus.SMBus(1)

class PCA9685: #pour commander les sorties pwm
    def __init__(self, address_PCA9685=0x40):
        
        self.address_PCA9685 = address_PCA9685
        self.bus=bus
       
       # INITIALISATION / DÉFINITION des registres
        self.MODE1 = 0x00  # self.REGISTRE = adresse_registre
        self.MODE2 = 0x01

        self.LED0_ON_L = 0x06
        self.LED0_ON_H = 0x07
        self.LED0_OFF_L = 0x08
        self.LED0_OFF_H = 0x09

        self.LED1_ON_L = 0x0A
        self.LED1_ON_H = 0x0B
        self.LED1_OFF_L = 0x0C
        self.LED1_OFF_H = 0x0D

        self.LED2_ON_L = 0x0E
        self.LED2_ON_H = 0x0F
        self.LED2_OFF_L = 0x10
        self.LED2_OFF_H = 0x11

        self.LED3_ON_L = 0x12
        self.LED3_ON_H = 0x13
        self.LED3_OFF_L = 0x14
        self.LED3_OFF_H = 0x15

        self.PRE_SCALE = 0xFE


        # CONFIGURATION des registres du PCA9685
        # write_byte_data prend trois arguments: l'adresse de l'appareil i2C, le nom de registre où on veut écrire, les données à écrire (byte/octet en hexadécimal)
        bus.write_byte_data(self.address_PCA9685,self.MODE1,0x10)
        bus.write_byte_data(self.address_PCA9685,self.PRE_SCALE,98)
        bus.write_byte_data(self.address_PCA9685,self.MODE1,0x00)


        bus.write_byte_data(self.address_PCA9685,self.MODE2,0x04) 

        # Les quatre registres suivants permettent de définir précisément les intervalles d’allumage et d’extinction (largeur d'impulsion) pour chaque LED, ce qui permet de contrôler la position d’un moteur.
        # LED N°0
        bus.write_byte_data(self.address_PCA9685,self.LED0_ON_L,0x0)  
        bus.write_byte_data(self.address_PCA9685,self.LED0_ON_H,0x0)
        bus.write_byte_data(self.address_PCA9685,self.LED0_OFF_L,0)
        bus.write_byte_data(self.address_PCA9685,self.LED0_OFF_H,0)

        # LED N°1       
        bus.write_byte_data(self.address_PCA9685,self.LED1_ON_L,37) # 0x25 est la valeur hexadécimale de 37 : valeur médiane de 12 et 62 
        bus.write_byte_data(self.address_PCA9685,self.LED1_ON_H,0x0)
        bus.write_byte_data(self.address_PCA9685,self.LED1_OFF_L,0x77)
        bus.write_byte_data(self.address_PCA9685,self.LED1_OFF_H,0x3)

        # LED N°2
        bus.write_byte_data(self.address_PCA9685,self.LED2_ON_L,0)
        bus.write_byte_data(self.address_PCA9685,self.LED2_ON_H,0x0)
        bus.write_byte_data(self.address_PCA9685,self.LED2_OFF_L,0)
        bus.write_byte_data(self.address_PCA9685,self.LED2_OFF_H,0)

        # LED N°3
        bus.write_byte_data(self.address_PCA9685,self.LED3_ON_L,0)
        bus.write_byte_data(self.address_PCA9685,self.LED3_ON_H,0x0)
        bus.write_byte_data(self.address_PCA9685,self.LED3_OFF_L,300)
        bus.write_byte_data(self.address_PCA9685,self.LED3_OFF_H,1)

        # PRE_SCALE (pour configurer la fréquence de la PWM (modulation de largeur d’impulsion) sur tous les canaux)
    def ecrire_temps_off_us(self,temp_off_us,num_sortie) :
        temps_H = temp_off_us//256
        temps_L = temp_off_us%256
        print("fonction ecrire_temps_off_us appel")
        if num_sortie == 0 :
            bus.write_byte_data(self.address_PCA9685,self.LED0_OFF_L,temps_L)
            bus.write_byte_data(self.address_PCA9685,self.LED0_OFF_H,temps_H)
        if num_sortie == 1 :
            bus.write_byte_data(self.address_PCA9685,self.LED1_OFF_L,temps_L)
            bus.write_byte_data(self.address_PCA9685,self.LED1_OFF_H,temps_H)
        if num_sortie == 2 :
            bus.write_byte_data(self.address_PCA9685,self.LED2_OFF_L,temps_L)
            bus.write_byte_data(self.address_PCA9685,self.LED2_OFF_H,temps_H)
        if num_sortie == 3 :
            bus.write_byte_data(self.address_PCA9685,self.LED3_OFF_L,temps_L)
            bus.write_byte_data(self.address_PCA9685,self.LED3_OFF_H,temps_H)
        if num_sortie == 4 :
            bus.write_byte_data(self.address_PCA9685,self.LED4_OFF_L,temps_L)
            bus.write_byte_data(self.address_PCA9685,self.LED4_OFF_H,temps_H)
        
class capteurs():

    def __init__(self, addresse_SRF10 = 0x70, addresse_BNO055 = 0x28):
        #self.address_SRF10 = addresse_SRF10   # télémètre ultrasons : plus utilisé => à remplacer par Lidar (télémètre infrarouge)
        self.address_BNO055 = addresse_BNO055 # centrale inertielle
        data = bus.read_i2c_block_data(self.address_BNO055,0x3F,1)
        data[0] = 0x20
        bus.write_byte_data(self.address_BNO055,0x07,1)
        bus.write_byte_data(self.address_BNO055,0x08,0x08)
        bus.write_byte_data(self.address_BNO055,0x0A,0x23)
        bus.write_byte_data(self.address_BNO055,0x0B,0x00)
        bus.write_byte_data(self.address_BNO055,0x09,0x1B)
        bus.write_byte_data(self.address_BNO055,0x07,0)
        bus.write_byte_data(self.address_BNO055,0x40,0x01)
        bus.write_byte_data(self.address_BNO055,0x3B,0x01)
        bus.write_byte_data(self.address_BNO055,0x3E,0x00)
        bus.write_byte_data(self.address_BNO055,0x3D,0x0C)
        print("fin de l'initialisation")
        pass

class LidarTFLuna: # pour lire la distance mesurée par le LiDAR TF Luna en utilisant le protocole I2C
    def __init__(self, i2c_address=0x10, i2c_bus=1):
        # Initialiser le bus I2C
        self.address = i2c_address
        self.bus = smbus.SMBus(i2c_bus)
    
    def read_distance(self):
        # Le TF Luna envoie les données de distance en 2 octets
        try:
            # Lire les 2 bytes (octets) de données de distance
            distance_data = self.bus.read_i2c_block_data(self.address, 0x00, 2)  #arguments: adresse unique du périphérique, adresse du premier registre à lire,  nbre de bytes à lire
            # Combiner les 2 octets en une seule valeur de distance en cm
            distance = (distance_data[0] + (distance_data[1] << 8))
            return distance
        except Exception as e:
            print(f"Erreur de lecture du LiDAR TF Luna : {e}")
            return None
    
    def get(self):
        self.lancement_mesure_us()
        time.sleep(0.5)
        distance_us_cm = self.lecture_distance_us_cm()
        roll_brut = (bus.read_word_data(self.address_BNO055,0x1C))
        pitch_brut = (bus.read_word_data(self.address_BNO055,0x18))
        yaw_brut = (bus.read_word_data(self.address_BNO055,0x1A))
        roll = np.int16(roll_brut)/16
        pitch = np.int16(pitch_brut)/16
        yaw = np.int16(yaw_brut)/16
        return(distance_us_cm, roll, pitch, yaw)
    
    def lancement_mesure_us(self):
        bus.write_byte_data(self.address_SRF10, 0, 0x51)
        return -1

    def lecture_distance_us_cm(self):
        MSB = bus.read_byte_data(self.address_SRF10, 2)
        LSB = bus.read_byte_data(self.address_SRF10, 3)
        distance = (MSB << 8) + LSB
        return distance
    

#initialisation:

lidar = LidarTFLuna()
#capteur = capteurs()
alt_obj = 150
myPCA9685 = PCA9685()
print("pret")

#boucle_continue/principale
while True : 
    time.sleep(1)
    temps_off = int(input("donner temp off :"))
    numero_sortie = int(input("donner numero sortie:"))
    myPCA9685.ecrire_temps_off_us(temps_off,numero_sortie)
    distance = lidar.read_distance()  # pour obtenir la distance mesurée par lidar
    print(distance)
    #distance_us, roll, pitch, yaw = capteur.get()
    # alt_mes = distance_us*np.cos(roll)*np.cos(pitch)*np.cos(yaw)
    # eps = alt_obj - alt_mes

