#startup
import version_info as v
print("Strider CLI PS4 Controller Client")
print("Version:", str(v.CLIENT_VERSION_MAJOR) + "." + str(v.CLIENT_VERSION_MINOR))

#connect to ssh
print()
import ssh_client as ssh
ssh_connection, ssh_channel = ssh.ssh_connect()

#if ssh_connection == None: #connection not sucessful
#    quit()


import pygame
import math
pygame.init()

controller = pygame.joystick.Joystick(0)
controller.init()

def handle_button_press(button):
    switch = {
        0: "-stop",
        1: "--stretch",
        2: "--idle",
        3: "--raise 100",

        11: "-fw",
        12: "-bw",
        13: "-left",
        14: "-rght",

        10: "--raise 10",
        9: "--raise -10"
    }

    command = switch.get(button, "unknown_command")

    if command != "unknown_command":
        print(f"Sending command: {command}")
        ssh.send_command(command, ssh_channel)
    else:
        print(f"Unknown Button Pressed: {button}")


joystick_threshold = 0.9 #deadzone
prev_angle = 0

def handle_left_joystick_event(axis_values):
    global prev_angle
    
    x, y = axis_values

    angle = math.degrees(math.atan2(y, x))
    magnitude = math.sqrt(x**2 + y**2)

    if magnitude > joystick_threshold:
        angle = round(angle)
        
        angle_difference = angle - prev_angle
        
        if abs(angle_difference) > 10:
            rotation_direction = "cw" if angle_difference > 0 else "ccw"

            command = f"-t{rotation_direction} 1"

            print(f"Sending command: {command}")
            
            ssh.send_command(command, ssh_channel)
            
            prev_angle = angle

last_command = ""
def handle_right_joystick_event(axis_values):
    global last_command
    
    x, y = axis_values

    magnitude = math.sqrt(x**2 + y**2)

    if magnitude > joystick_threshold:
        
        if y > joystick_threshold and abs(x) < 1:
            command = f"-bw"
        elif y < -joystick_threshold and abs(x) < 1:
            command = f"-fw"
        elif abs(y) < 1 and x > joystick_threshold:
            command = f"-rght"
        elif abs(y) < 1 and x < -joystick_threshold:
            command = f"-left"
        else:
            command = ""

        if command != "":
            if command != last_command:
                print(f"Sending command: {command}")
                ssh.send_command(command, ssh_channel)
                last_command = command

    elif abs(y) < 0.3 and abs(x) < 0.3:
        command = f"-stop"
        if command != last_command:
            print(f"Sending command: {command}")
            ssh.send_command(command, ssh_channel)
            last_command = command
            

try:
    print(controller.get_name())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 1 or event.axis == 0:
                    handle_left_joystick_event((controller.get_axis(0), controller.get_axis(1)))
                if event.axis == 2 or event.axis == 3:
                    handle_right_joystick_event((controller.get_axis(2), controller.get_axis(3)))
            elif event.type == pygame.JOYBUTTONDOWN:
                handle_button_press(event.button)
            elif event.type == pygame.JOYBUTTONUP:
                None
                # print("Button Released:", event.button)
            

except KeyboardInterrupt:
    ssh.ssh_close(ssh_connection)
    print("EXITING NOW")
    controller.quit()



