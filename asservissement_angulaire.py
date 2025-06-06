import cv2
from picamera2 import Picamera2
import time
from pyapriltags import Detector
import numpy as np


class Tag :
    def __init__(self):
        
        self.picam2 = Picamera2()
        
        self.WIDTH = 1536
        self.HEIGH = 864
        self.picam2.configure(self.picam2.create_preview_configuration({'size':(self.WIDTH,self.HEIGH)}))
        self.picam2.start()

        self.at_detector = Detector(families="tag36h11",nthreads=1,quad_sigma=0.0,refine_edges=1,\
decode_sharpening=0.25,debug=0)

        #coefficients de distorsion de la camera

        self.mtx = np.array([[ 977.08159964 	,  0.00000000e+00,  789.18761132],[ 0.00000000e+00,  977.14004212, 434.47165678],[ 0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])
        self.dist = np.array([[-0.02727091,  0.1312434,   0.00479796,  0.00269239, -1.30723302]])
        self.fx = self.mtx[0][0]
        self.cx = self.mtx[0][2]
        self.fy = self.mtx[1][1]
        self.cy = self.mtx[1][2]
        
        #Positions des tags dans l'environnement
        
        self.listePoints3D = {100: (0.085, 0.27, 0), 101: (0.085, 1.27, 0), 102: (0.085, 2.27, 0), 103: (0.085, 3.27, 0), 104: (0.085, 4.27, 0), 105: (0.085, 5.27, 0), 106: (0.085, 6.27, 0), 107: (0.085, 7.27, 0), 108: (0.085, 8.27, 0), 109: (0.085, 9.27, 0), 110: (1.085, 0.27, 0), 111: (1.085, 1.27, 0), 112: (1.085, 2.27, 0), 113: (1.085, 3.27, 0), 114: (1.085, 4.27, 0), 115: (1.085, 5.27, 0), 116: (1.085, 6.27, 0), 117: (1.085, 7.27, 0), 118: (1.085, 8.27, 0), 119: (1.085, 9.27, 0), 120: (2.085, 0.27, 0), 121: (2.085, 1.27, 0), 122: (2.085, 2.27, 0), 123: (2.085, 3.27, 0), 124: (2.085, 4.27, 0), 125: (2.085, 5.27, 0), 126: (2.085, 6.27, 0), 127: (2.085, 7.27, 0), 128: (2.085, 8.27, 0), 129: (2.085, 9.27, 0), 130: (3.085, 0.27, 0), 131: (3.085, 1.27, 0), 132: (3.085, 2.27, 0), 133: (3.085, 3.27, 0), 134: (3.085, 4.27, 0), 135: (3.085, 5.27, 0), 136: (3.085, 6.27, 0), 137: (3.085, 7.27, 0), 138: (3.085, 8.27, 0), 139: (3.085, 9.27, 0), 140: (4.085, 0.27, 0), 141: (4.085, 1.27, 0), 142: (4.085, 2.27, 0), 143: (4.085, 3.27, 0), 144: (4.085, 4.27, 0), 145: (4.085, 5.27, 0), 146: (4.085, 6.27, 0), 147: (4.085, 7.27, 0), 148: (4.085, 8.27, 0), 149: (4.085, 9.27, 0), 150: (5.085, 0.27, 0), 151: (5.085, 1.27, 0), 152: (5.085, 2.27, 0), 153: (5.085, 3.27, 0), 154: (5.085, 4.27, 0), 155: (5.085, 5.27, 0), 156: (5.085, 6.27, 0), 157: (5.085, 7.27, 0), 158: (5.085, 8.27, 0), 159: (5.085, 9.27, 0), 160: (6.085, 0.27, 0), 161: (6.085, 1.27, 0), 162: (6.085, 2.27, 0), 163: (6.085, 3.27, 0), 164: (6.085, 4.27, 0), 165: (6.085, 5.27, 0), 166: (6.085, 6.27, 0), 167: (6.085, 7.27, 0), 168: (6.085, 8.27, 0), 169: (6.085, 9.27, 0), 170: (7.085, 0.27, 0), 171: (7.085, 1.27, 0), 172: (7.085, 2.27, 0), 173: (7.085, 3.27, 0), 174: (7.085, 4.27, 0), 175: (7.085, 5.27, 0), 176: (7.085, 6.27, 0), 177: (7.085, 7.27, 0), 178: (7.085, 8.27, 0), 179: (7.085, 9.27, 0), 180: (8.085, 0.27, 0), 181: (8.085, 1.27, 0), 182: (8.085, 2.27, 0), 183: (8.085, 3.27, 0), 184: (8.085, 4.27, 0), 185: (8.085, 5.27, 0), 186: (8.085, 6.27, 0), 187: (8.085, 7.27, 0), 188: (8.085, 8.27, 0), 189: (8.085, 9.27, 0), 190: (9.085, 0.27, 0), 191: (9.085, 1.27, 0), 192: (9.085, 2.27, 0), 193: (9.085, 3.27, 0), 194: (9.085, 4.27, 0), 195: (9.085, 5.27, 0), 196: (9.085, 6.27, 0), 197: (9.085, 7.27, 0), 198: (9.085, 8.27, 0), 199: (9.085, 9.27, 0)}
        self.matrice=np.array([[-1,0,0],[0,1,0],[0,0,1]])

    def Detection_Tags(self):
        img=cv2.cvtColor(self.picam2.capture_array(),cv2.COLOR_BGR2GRAY) #prise d'une photo puis correction
        img_undistorded = cv2.undistort(img, self.mtx, self.dist, None, newCameraMatrix=self.mtx)
        #indication de la taille des tags, lancement de la detection
        tags=self.at_detector.detect(img_undistorded,estimate_tag_pose=True,camera_params=[self.fx,self.fy,self.cx,self.cy],tag_size=0.172) 
        return tags

    def calculAngles(self,R):
        sy = np.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
        singular = sy < 1e-6
        if not singular:
            x = np.arctan2(R[2, 1], R[2, 2])
            y = np.arctan2(-R[2, 0], sy)
            z = np.arctan2(R[1, 0], R[0, 0])
        else:
            x = np.arctan2(-R[1, 2], R[1, 1])
            y = np.arctan2(-R[2, 0], sy)
            z = 0
        return np.degrees(np.array([x, y, z]))



    def localisation(self):
        """Renvoie:
            (x, y, z, alpha)
            - La position de la caméra (x, y, z) dans le repère du sol
            - L'angle de lacet (c'est le seul qui nous interesse dans le cas d'un dirigeable
            """
    
        tags=self.Detection_Tags()
    
        positions=[]
        angles=[]
        
        positionMoyenne=np.array([0,0,0],dtype='float64')
        angleMoyen=np.array([0,0,0],dtype='float64')
    
        for tag in tags:
        
            angles.append(np.array(self.calculAngles(tag.pose_R)))
        
            pose=np.dot(np.transpose(tag.pose_R),tag.pose_t)
       
            try :
                positions.append(np.dot(self.matrice,np.transpose(pose)[0])+np.array(self.listePoints3D[tag.tag_id])) 
            except : 
                print("Tag inconnu")
         
            for position in positions:
                positionMoyenne += position
            for angle in angles:
                angleMoyen += angle
    
        n=len(positions)
        if n!=0:
            positionMoyenne=positionMoyenne/n
            angleMoyen=angleMoyen/n

            #            X                    Y                     Z              Lacet
            return(positionMoyenne[0], positionMoyenne[1], positionMoyenne[2], angleMoyen[2])   
    
# ASSERV

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
        self.integral = max(min(self.integral, 100), -100)
        I = self.Ki * self.integral

        # Terme dérivé
        D = self.Kd * (error - self.previous_error)
        self.previous_error = error

        R=P+I+D

        # Sortie PID (limitée entre 0 et 100 pour la vitesse du moteur)
        output = max(min(R, 50), 20)
        return output
    
    def compute2(self, measured_value):
        
        
        """Calcule la sortie PID en fonction de la valeur mesurée"""
        error = self.consigne - measured_value
        if error > 180:
            error -= 360
        elif error < -180:
            error += 360  

        # Terme proportionnel
        P = self.Kp * error

        # Terme intégral
        self.integral += error
        self.integral = max(min(self.integral, 100), -100)
        I = self.Ki * self.integral

        # Terme dérivé
        D = self.Kd * (error - self.previous_error)
        self.previous_error = error

        R=P+D
        #print (R)
        # Sortie PID (limitée entre -50,-20 et 20,50 pour la vitesse du moteur)
        if R<0 : 
            output = min(max(R, -50), -20)
        else :
            output = max(min(R, 50), 20)
        return output

    
 
consigne = int(input("donner angle consigne:"))
tolerance = 2

pid = PID(0.5,0.1,0.05,consigne)  

tag=Tag()

while True: 
    angle=tag.localisation()[3] 
    vitesse=pid.compute2(angle)
    print(tag.localisation()[0],tag.localisation()[1])    
    #mot_brushless.commande(vitesse,0)
    #mot_brushless.commande(vitesse,1)
    
    
