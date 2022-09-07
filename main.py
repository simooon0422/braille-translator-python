from machine import Pin, UART, I2C
from pca import PCA9685
from servo import Servos

uart = UART(0,9600) #Initialize UART

sda = Pin(2) #SDA pin
scl = Pin(3) #SCL pin
i2c_id = 1 #I2C id

i2c = I2C(id=i2c_id, sda=sda, scl=scl) #Initialize I2C
pca = PCA9685(i2c=i2c) #Create PCA9685 object
servos = Servos(i2c=i2c) #Create Servos object

print(i2c.scan())

while True:
    if uart.any():
        command = uart.read()
        message = str(command.rstrip(), 'utf8')#str(command)#command.decode('utf-8')#str(command.rstrip(), 'utf8')
        print(message)

        
