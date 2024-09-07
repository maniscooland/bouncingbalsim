import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the sound mixer

# Set up the display
width, height = 8000, 6000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ball Simulation")

# Circle properties
center_x = width // 2
center_y = height // 2
initial_radius = 250
circle_thickness = 2
hole_angle = random.uniform(0, 2 * math.pi)
hole_size = 30  # Size of the hole in degrees

# Ball properties
ball_radius = 10
ball_x = center_x
ball_y = center_y
ball_speed = 3
angle = random.uniform(0, 2 * math.pi)
ball_speed_x = ball_speed * math.cos(angle)
ball_speed_y = ball_speed * math.sin(angle)

# Gravity
gravity = 0.5
min_speed = 10  # Minimum speed to ensure the ball always moves

# Colors
ball_color = (255, 0, 0)  # Red
circle_color = (0, 0, 255)  # Blue
background_color = (0, 0, 0)  # Black
hole_color = (0, 255, 0)  # Green
# Load the sound files
bounce_sound = pygame.mixer.Sound("bounce.wav")  # Replace with your .wav file
bounce_sound.set_volume(0.3)  # Set the volume to 30% of the original
hole_sound = pygame.mixer.Sound("hole.wav")  # Replace with your hole sound .wav file
hole_sound.set_volume(200000.0)  # Set the volume to 200% of the original

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Main game loop
clock = pygame.time.Clock()

fps = 1 / 60
circles = [initial_radius]
current_circle = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Apply gravity
    ball_speed_y += gravity

    # Ensure minimum speed
    speed = math.sqrt(ball_speed_x**2 + ball_speed_y**2)
    if speed < min_speed:
        angle = math.atan2(ball_speed_y, ball_speed_x)
        ball_speed_x = min_speed * math.cos(angle)
        ball_speed_y = min_speed * math.sin(angle)

    ball_x += ball_speed_x
    ball_y += ball_speed_y

    dist = distance(ball_x, ball_y, center_x, center_y)
    if dist > circles[current_circle] - ball_radius:
        ball_angle = math.atan2(ball_y - center_y, ball_x - center_x)
        angle_diff = (ball_angle - hole_angle + math.pi) % (2 * math.pi) - math.pi
        
        if abs(angle_diff) > math.radians(hole_size / 2):
            nx = ball_x - center_x
            ny = ball_y - center_y
            norm = math.sqrt(nx**2 + ny**2)
            nx /= norm
            ny /= norm

            dot_product = ball_speed_x * nx + ball_speed_y * ny

            ball_speed_x -= 2 * dot_product * nx
            ball_speed_y -= 2 * dot_product * ny

            # Increase speed by 0.5 after each bounce
            speed = math.sqrt(ball_speed_x**2 + ball_speed_y**2)
            speed += 0.5
            angle = math.atan2(ball_speed_y, ball_speed_x)
            ball_speed_x = speed * math.cos(angle)
            ball_speed_y = speed * math.sin(angle)

            ball_x = center_x + (circles[current_circle] - ball_radius) * nx
            ball_y = center_y + (circles[current_circle] - ball_radius) * ny

            bounce_sound.play()
        else:
            if current_circle == len(circles) - 1:
                new_radius = circles[current_circle] + 100
                circles.append(new_radius)
            current_circle += 1
            hole_angle = random.uniform(0, 2 * math.pi)
            hole_sound.play()  # Play the hole sound when the ball goes through the hole

    screen.fill(background_color)
    for i, radius in enumerate(circles):
        if i == current_circle:
            pygame.draw.arc(screen, circle_color, (center_x - radius, center_y - radius, radius * 2, radius * 2),
                            hole_angle - math.radians(hole_size / 2), hole_angle + math.radians(hole_size / 2), circle_thickness)
            pygame.draw.arc(screen, circle_color, (center_x - radius, center_y - radius, radius * 2, radius * 2),
                            hole_angle + math.radians(hole_size / 2), hole_angle - math.radians(hole_size / 2) + 2 * math.pi, circle_thickness)
            
            # Draw the hole
            hole_start = (center_x + radius * math.cos(hole_angle - math.radians(hole_size / 2)),
                          center_y + radius * math.sin(hole_angle - math.radians(hole_size / 2)))
            hole_end = (center_x + radius * math.cos(hole_angle + math.radians(hole_size / 2)),
                        center_y + radius * math.sin(hole_angle + math.radians(hole_size / 2)))
            pygame.draw.line(screen, hole_color, hole_start, hole_end, 5)
        else:
            pygame.draw.circle(screen, circle_color, (center_x, center_y), radius, circle_thickness)
    
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)
    pygame.display.flip()
    fps = clock.tick(60) / 1000
