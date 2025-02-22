from picamera2 import Picamera2
def modele(n:int=0):     
        modeles = {
            "imx219": "V2",
            "imx708": "V3",
            "imx708_wide": "V3W"}
        print(n)
        picam2 = Picamera2(camera_num=n)
        modele = modeles[picam2.global_camera_info()[0]['Model']]
        picam2.stop()
        picam2.close()
        return modele
