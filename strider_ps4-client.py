#startup
import version_info as v
print("Strider CLI PS4 Controller Client")
print("Version:", str(v.CLIENT_VERSION_MAJOR) + "." + str(v.CLIENT_VERSION_MINOR))

#connect to ssh
print()
import ssh_client as ssh
ssh_connection, ssh_channel = ssh.ssh_connect()

if ssh_connection == None: #connection not sucessful
    quit()


import pygame
pygame.init()

controller = pygame.joystick.Joystick(0)
controller.init()

def handle_button_press(button):
    switch = {
        11: "--version",
        12: "Backwards",
        13: "Left",
        14: "Right",
        # Add more buttons as needed
    }

    command = switch.get(button, "unknown_command")

    if command != "unknown_command":
        print(f"Sending command: {command}")
        # Call your function to send the command here
        ssh.send_command(command, ssh_channel)
    else:
        print("Unknown Button Pressed")


try:
    print(controller.get_name())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                handle_button_press(event.button)
            elif event.type == pygame.JOYBUTTONUP:
                None
                #print("Button Released:", event.button)

except KeyboardInterrupt:
    ssh.ssh_close(ssh_connection)
    print("EXITING NOW")
    controller.quit()



