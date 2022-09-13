from machine import Pin, UART, I2C
from time import sleep, ticks_ms
from pca import PCA9685
from servo import Servos
from braille_dictionary import braille_dictionary as b_dict

uart = UART(0,9600) #Initialize UART

i2c_sda = Pin(2) #SDA pin
i2c_scl = Pin(3) #SCL pin
i2c_id = 1 #I2C id

#buttons pins
button_increase_pin = 15
button_decrease_pin = 14

#variables for changing displayed letter
current_letter = 0
last_letter = 0

#variables storing time for buttons debounce
last_time_increase = 0
last_time_decrease = 0

message_list = [] #list containing letters to display

i2c = I2C(id=i2c_id, sda=i2c_sda, scl=i2c_scl) #Initialize I2C
pca = PCA9685(i2c=i2c) #Create PCA9685 object
servos = Servos(i2c=i2c) #Create Servos object


braille_dots = [0, 0, 0, 0, 0, 0] #data of braille version of letter
serv_0_position = [90, 90, 90, 90, 90, 90] #servo position when pin is down
serv_1_position = [115, 115, 115, 65, 65, 65] #servo position when pin is up
serv_current_position = [90, 90, 90, 90, 90, 90] #current servo position
serv_desired_position = [90, 90, 90, 90, 90, 90] #desired servo position

#function to get bralle data of current letter
def letter_to_braille(letter):
    braille_data = b_dict.get(letter, [0, 0, 0, 0, 0, 0])
    return braille_data

#function to specify desired servos positions
def physical_representation(letter_data):
    for i in range(len(letter_data)):
        if letter_data[i] == 1:
            serv_desired_position[i] = serv_1_position[i]
        else:
            serv_desired_position[i] = serv_0_position[i]

#function to update servos positions
def update_servos():
    print("des:") #test
    print(serv_desired_position) #test
    for i in range(6):
        if serv_current_position[i] < serv_desired_position[i]:
            for j in range(serv_current_position[i], serv_desired_position[i], 1):
                servos.position(index=i, degrees=j)
                serv_current_position[i] = j
                sleep(0.01) #slow down servo movement
        else:
            for j in range(serv_current_position[i], serv_desired_position[i], -1):
                servos.position(index=i, degrees=j)
                serv_current_position[i] = j
                sleep(0.01) #slow down servo movement
                
#function to set all pins on down position              
def reset_servos():
    for i in range(6):
        servos.position(index=i, degrees=serv_0_position[i])
            
#functions to change displayed letter on interrupt
def handle_interrupt_increase(Pin):
    global current_letter, last_time_increase
    new_time = ticks_ms()
    if (new_time - last_time_increase) > 200 and (current_letter < len(message_list)-1):
        current_letter = current_letter + 1
        print(current_letter) #test
        print(len(message_list)) #test
        last_time_increase = new_time
        
def handle_interrupt_decrease(Pin):
    global current_letter, last_time_decrease
    new_time = ticks_ms()
    if (new_time - last_time_decrease) > 200 and current_letter > 0:
        current_letter = current_letter - 1
        print(current_letter) #test
        last_time_decrease = new_time
        
#create buttons objects
button_increase = Pin(button_increase_pin, Pin.IN, Pin.PULL_UP)
button_decrease = Pin(button_decrease_pin, Pin.IN, Pin.PULL_UP)

#create interrupts
button_increase.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt_increase)
button_decrease.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt_decrease)


reset_servos() #reset servos positions before starting main program
while True:
    if uart.any():
        command = uart.read() #read data sent through bluetooth
        message = str(command, 'utf8') #store it in a variable
        print(message) #test
        message_list = list(message) #convert variable to a list
        print(message_list) #test
        current_letter = 0 #set currently displayed letter to the first one
        braille_dots = letter_to_braille(message[current_letter]) #get braille version data of current letter
        print(message[current_letter]) #test
        print(braille_dots) #test
        physical_representation(braille_dots) #specify desired servos positions
        update_servos() #update servos positions
        
    if current_letter != last_letter:
        #display next letter if current letter changed by interrupt
        braille_dots = letter_to_braille(message[current_letter]) #get braille version data of current letter
        print(message[current_letter]) #test
        print(braille_dots) #test
        physical_representation(braille_dots) #specify desired servos positions
        update_servos() #update servos positions
        last_letter = current_letter
#         if message == "180":
#             servos.position(index=0, degrees=180)
#         elif message == "90":
#             servos.position(index=0, degrees=90)
#         else:
#             servos.position(index=0, degrees=0)

# def update_servos():
#     for i in range(6):
#         servos.position(index=i, degrees=serv_desired_position[i])        

