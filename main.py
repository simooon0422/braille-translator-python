from machine import Pin, UART, I2C
from pca import PCA9685
from servo import Servos

uart = UART(0,9600) #Initialize UART

i2c_sda = Pin(2) #SDA pin
i2c_scl = Pin(3) #SCL pin
i2c_id = 1 #I2C id

i2c = I2C(id=i2c_id, sda=i2c_sda, scl=i2c_scl) #Initialize I2C
pca = PCA9685(i2c=i2c) #Create PCA9685 object
servos = Servos(i2c=i2c) #Create Servos object


braille_dots = [0, 0, 0, 0, 0, 0]


def letter_to_braille(letter):
    return braille_dict.get(letter, "nothing")

while True:
    if uart.any():
        command = uart.read()
        message = str(command.rstrip(), 'utf8')#str(command)#command.decode('utf-8')#str(command.rstrip(), 'utf8')
        print(message)
        
        print(letter_to_braille(message))
        
#         if message == "180":
#             servos.position(index=0, degrees=180)
#         elif message == "90":
#             servos.position(index=0, degrees=90)
#         else:
#             servos.position(index=0, degrees=0)

        

