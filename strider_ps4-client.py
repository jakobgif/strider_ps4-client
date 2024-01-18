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
        3: "--raise -100",

        11: "-fw",
        12: "-bw",
        13: "-left",
        14: "-rght",

        10: "--raise 10",
        9: "--raise -10"
        # Add more buttons as needed
    }

    command = switch.get(button, "unknown_command")

    if command != "unknown_command":
        print(f"Sending command: {command}")
        # Call your function to send the command here
        ssh.send_command(command, ssh_channel)
    else:
        print(f"Unknown Button Pressed: {button}")

joystick_threshold = 0.9  # You can adjust this value based on your needs



def handle_joystick_event(axis_values):
    x, y = axis_values

    angle = math.degrees(math.atan2(y, x))
    magnitude = math.sqrt(x**2 + y**2)

    if magnitude > joystick_threshold:
        rotation_degrees = angle  # You can adjust this based on your requirements
        command = f"--rotate {rotation_degrees}"
        print(f"Sending command: {command}")
        # Call your function to send the command here
        # ssh.send_command(command, ssh_channel)


try:
    print(controller.get_name())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:  # Assuming X-axis for left joystick
                    #handle_joystick_event((event.value, controller.get_axis(1)))  # Y-axis
                    None
            elif event.type == pygame.JOYBUTTONDOWN:
                handle_button_press(event.button)
            elif event.type == pygame.JOYBUTTONUP:
                None
                # print("Button Released:", event.button)
            

except KeyboardInterrupt:
    ssh.ssh_close(ssh_connection)
    print("EXITING NOW")
    controller.quit()



