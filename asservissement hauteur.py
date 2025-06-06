   
class PID:
    def __init__(self, Kp, Ki, Kd, consigne=0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.consigne = consigne

        self.previous_error = 0
        self.integral = 0
    
    
    def compute(self, measured_value):
        
        """Calcule la sortie PID en fonction de la valeur mesurée"""
        error = self.consigne - measured_value

        # Terme proportionnel
        P = self.Kp * error

        # Terme intégral
        self.integral += error
        I = self.Ki * self.integral

        # Terme dérivé
        D = self.Kd * (error - self.previous_error)
        self.previous_error = error

        R=P+I+D

        # Sortie PID (limitée entre 0 et 100 pour la vitesse du moteur)
        output = max(min(R, 50), 10)
        return output
    
g=PID(0.5,1,1,100)




class PID:
    def __init__(self, Kp, Ki, Kd, consigne):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.consigne = consigne

        self.previous_error = 0
        self.integral = 0

    def compute(self, measured_value):
        
        
        """Calcule la sortie PID en fonction de la valeur mesurée"""
        error = self.consigne - measured_value

        # Terme proportionnel
        P = self.Kp * error

        # Terme intégral
        self.integral += error
        I = self.Ki * self.integral

        # Terme dérivé
        D = self.Kd * (error - self.previous_error)
        self.previous_error = error

        R=P+I+D

        # Sortie PID (limitée entre 0 et 100 pour la vitesse du moteur)
        output = max(min(R, 50), 10)
        return output

# Asservissement en hauteur :
    
consigneh = int(input("donner consigne hauteur:"))

pid = PID(0.5,0.1,0.05,consigneh)

while True : 
    distance = lidar.read_distance()
    # print(f"La distance mesurée par le télémètre infrarouge est: {distance}cm")
    
    vitesse=pid.compute(distance)
    
    mot_brushless.commande(vitesse,0)
    
    if distance<5 : 
        mot_brushless.commande(0,0)
        break