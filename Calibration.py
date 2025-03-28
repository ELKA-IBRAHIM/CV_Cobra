def calibration():
    #source: Revue3EI_LocalisationApriltags
    #Adaptation pour deux caméras 
    import os
    import numpy as np
    import cv2 as cv
    import glob
    import modele_cam
    import time
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 22, 0.001)
    taille = 0.022


    # Arrays to store 3D points and 2D image points
    obj_points = []
    img_points = []

    # Prepare expected object 3D object points (0,0,0), (1,0,0) ...
    objp = np.zeros((7*10,3), np.float32)
    objp[:,:2] = np.mgrid[0:10, 0:7].T.reshape(-1,2)

    
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    PhotosEchequier = input("nom du repertoire contant les images de l'échequier :")

    chemin = f"/home/CobraVision2/Localisation/CV_Cobra/{PhotosEchequier}"
    modele = modele_cam.modele()
    images = glob.glob(f"{chemin}/*.png")  
    print(len(images))
    for fname in images:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (7,10), None)
        print(ret)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (10,11), (-1,-1), criteria)
            imgpoints.append(corners2)

    #gray = cv.imread(images[0], cv.IMREAD_GRAYSCALE).shape
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    fichier_calibrationn =  f"/home/CobraVision2/Localisation/CV_Cobra/{modele}_Calibration.txt"
        
    current_time = time.localtime()
    date_actuelle = time.strftime("%Y-%m-%d", current_time)
    print(mtx, dist)
    with open(fichier_calibrationn, "a") as f:
        f.write(f"--------Calibration--{date_actuelle}-----camera {modele}----\n")
        f.write(f"mtx = {mtx}\n")
        f.write(f"dist = {dist}\n")        
calibration()