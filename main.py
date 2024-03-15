import pygame
import socket
import struct
import time
 
pygame.init()
 
# Initialize the joystick
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
 
# Server address and port
server_address = '192.168.50.151'  # Replace with the IP address of your ESP32
server_port = 10000

def encode_motor_values(motor1, motor2, motor3):
    encode_value = (motor1<<22)|(motor2<<11)|motor3
    return encode_value
 
# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def apply_deadzone(value, deadzone=0.1, maximum=0.9):
    if -deadzone < value < deadzone:
        return 0
    if -maximum < value < maximum
        return 0.995
    else:
        return value
try:
    # Connect to the server
    client_socket.connect((server_address, server_port))
 
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
        # Read the left Y-axis, right y-axis, and trigger values
        left_y = apply_deadzone(joystick.get_axis(1))
        right_y = apply_deadzone(joystick.get_axis(3))
        l2_trigger = apply_deadzone(joystick.get_axis(4))
        r2_trigger = apply_deadzone(joystick.get_axis(5))
 
        # Read button states
        #r1_button = joystick.get_button(5)
        #l1_button = joystick.get_button(4)
        
        
        #adjusts joystick values to [-199, 199]
        throttle_value = right_y * 200
        motor3_value = left_y * 200
        
        #percent modification adjusted to output [0-1]
        left_mod = ((l2_trigger + 1) * 0.5)
        right_mod = ((r2_trigger + 1) * 0.5)
        
        #reduces speed of motors based on mod percent in order to turn 
        motor1_value = throttle_value * left_mod 
        motor2_value = throttle_value * right_mod
        
        motor1_value = int(motor1_value)
        motor2_value = int(motor2_value)
        motor3_value = int(motor3_value)
        
        #print(motor1_value)
        #print(motor2_value)
        #print(motor3_value)
        
        encoded_value = encode_motor_values(motor1_value, motor2_value, motor3_value)
        
        print(encoded_value)
        
        data = struct.pack('i', encoded_value)
        
        client_socket.sendall(data) #sends data to Esp32
        

        
        # # Add a short delay to control the sending rate
        time.sleep(0.1)  # Adjust the delay as needed
 
finally:
    # Close the socket and the joystick (usually not reached in an infinite loop)
    client_socket.close()
    joystick.quit()
