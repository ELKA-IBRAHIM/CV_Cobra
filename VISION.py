intro = """
  ____      _                 ___ _               _     _           
 / ___|___ | |__  _ __ __ _  |_ _| |__  _ __ __ _| |__ (_)_ __ ___  
| |   / _ \| '_ \| '__/ _` |  | || '_ \| '__/ _` | '_ \| | '_ ` _ \ 
| |__| (_) | |_) | | | (_| |  | || |_) | | | (_| | | | | | | | | | |
 \____\___/|_.__/|_|  \__,_| |___|_.__/|_|  \__,_|_| |_|_|_| |_| |_|


"""
print(intro)


text_calibration = """ 

  ____      _ _ _               _   _              
 / ___|__ _| (_) |__  _ __ __ _| |_(_) ___  _ __   
| |   / _` | | | '_ \| '__/ _` | __| |/ _ \| '_ \  
| |__| (_| | | | |_) | | | (_| | |_| | (_) | | | | 
 \____\__,_|_|_|_.__/|_|  \__,_|\__|_|\___/|_| |_| 

"""
text_Echequier = """
 _____     _                      _           
| ____|___| |__   ___  __ _ _   _(_) ___ _ __ 
|  _| / __| '_ \ / _ \/ _` | | | | |/ _ \ '__|
| |__| (__| | | |  __/ (_| | |_| | |  __/ |   
|_____\___|_| |_|\___|\__, |\__,_|_|\___|_|   
                         |_|                  


"""
text_temps_f_resolution = """
 _____                           __        __            _       _   _              __  
|_   _|__ _ __ ___  _ __  ___   / /  _ __ /_/  ___  ___ | |_   _| |_(_) ___  _ __   \ \ 
  | |/ _ \ '_ ` _ \| '_ \/ __| | |  | '__/ _ \/ __|/ _ \| | | | | __| |/ _ \| '_ \   | |
  | |  __/ | | | | | |_) \__ \ | |  | | |  __/\__ \ (_) | | |_| | |_| | (_) | | | |  | |
  |_|\___|_| |_| |_| .__/|___/ | |  |_|  \___||___/\___/|_|\__,_|\__|_|\___/|_| |_|  | |
                   |_|          \_\                                                 /_/ 

"""
text = f"Choisir: \
    \n \n 1 : Prendre des images d'un échequier pour calibraer la caméra \
    \n \n 2 : Calibration à partir d'un répertoire d'images \
    \n \n 3 : Calcul du temps de traitement en fonction de la résolution  \
    \n \n Votre choix : "

choix = input(text)

while not (choix in ['1', ' 1','2', ' 2' ,'3', ' 3']):
    print("\n" +" Votre choix n'est pas valide !!")
    choix = input(text)

if choix in ['1', ' 1']:
    print(text_Echequier)
    from EchequierPhotos import echequier_photos
    echequier_photos()
elif choix in [' 2', '2']:
    print(text_calibration)
    from Calibration import calibration
    calibration()
else :
    print(text_temps_f_resolution)
    from temps_resolution import temps_f_resolution
    temps_f_resolution()
