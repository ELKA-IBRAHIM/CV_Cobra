from gpiozero import LED
import time
pin_sens_AV = 23
pin_sens_AR = 24

sens_AV = LED(pin_sens_AV)
sens_AR = LED(pin_sens_AR)

sens_AR.on()
time.sleep(50)
sens_AR.off()

