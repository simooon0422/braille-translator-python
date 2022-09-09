from machine import Pin, UART, I2C
from time import sleep
from pca import PCA9685
from servo import Servos
from braille_dictionary import braille_dictionary as b_dict

uart = UART(0,9600) #Initialize UART

i2c_sda = Pin(2) #SDA pin
i2c_scl = Pin(3) #SCL pin
i2c_id = 1 #I2C id

button_increase_pin = 15
button_decrease_pin = 14
current_letter = 0
last_time_increase = 0
last_time_decrease = 0

i2c = I2C(id=i2c_id, sda=i2c_sda, scl=i2c_scl) #Initialize I2C
pca = PCA9685(i2c=i2c) #Create PCA9685 object
servos = Servos(i2c=i2c) #Create Servos object


braille_dots = [0, 0, 0, 0, 0, 0]
serv_0_position = [90, 90, 90, 90, 90, 90]
serv_1_position = [150, 150, 150, 30, 30, 30]
serv_current_position = [90, 90, 90, 90, 90, 90]
serv_position = [90, 90, 90, 90, 90, 90]


def letter_to_braille(letter):
    braille_data = b_dict.get(letter, [0, 0, 0, 0, 0, 0])
    return braille_data

def physical_representation(letter_data):
    for i in letter_data:
        if letter_data[i] == 1:
            serv_position[i] = serv_1_position[i]
        else:
            serv_position[i] = serv_0_position[i]

def update_servos():
    for i in range(6):
        if serv_current_position[i] < serv_position[i]:
            for j in range(serv_current_position[i], serv_position[i], 1):
                servos.position(index=i, degrees=j)
                serv_current_position[i] = j
                sleep(0.01)
        else:
            for j in range(serv_current_position[i], serv_position[i], -1):
                servos.position(index=i, degrees=j)
                serv_current_position[i] = j
                sleep(0.01)
                
def reset_servos():
    for i in range(6):
        for i in range(6):
            servos.position(index=i, degrees=serv_0_position[i])
            
def handle_interrupt_increase(Pin):
    global current_letter, last_time_increase
    new_time = ticks_ms()
    if (new_time - last_time_increase) > 200:
        counter = counter + 1
        print(counter)
        last_time_increase = new_time
        
def handle_interrupt_decrease(Pin):
    global current_letter, last_time_decrease
    new_time = ticks_ms()
    if (new_time - last_time_decrease) > 200 and counter > 0:
        counter = counter - 1
        print(counter)
        last_time_decrease = new_time
        
button_increase = Pin(button_increase_pin, Pin.IN, Pin.PULL_UP)
button_decrease = Pin(button_decrease_pin, Pin.IN, Pin.PULL_UP)

button_increase.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt_increase)
button_decrease.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt_decrease)


reset_servos()
while True:
    if uart.any():
        command = uart.read()
        message = str(command.rstrip(), 'utf8')#str(command)#command.decode('utf-8')#str(command.rstrip(), 'utf8')
        print(message) #test
        braille_dots = letter_to_braille(message)     
#         print(letter_to_braille(message))
        print(braille_dots) #test
        physical_representation(braille_dots)
        update_servos()
        
#         if message == "180":
#             servos.position(index=0, degrees=180)
#         elif message == "90":
#             servos.position(index=0, degrees=90)
#         else:
#             servos.position(index=0, degrees=0)

# def update_servos():
#     for i in range(6):
#         servos.position(index=i, degrees=serv_position[i])        

