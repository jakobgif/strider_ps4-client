import pygame

MAJOR = 0
MINOR = 1

print("Strider CLI Client")
print("Version:", str(MAJOR) + "." + str(MINOR))

pygame.init()

controller = pygame.joystick.Joystick(0)
controller.init()

try:
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                print("Button Pressed")
            elif event.type == pygame.JOYBUTTONUP:
                print("Button Released")

except KeyboardInterrupt:
    print("EXITING NOW")
    controller.quit()