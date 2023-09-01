import pygame
# this is config file:

# Set the maximum amount of movement for the circle
max_movement = 5

#dimention of game window
window_width, window_height = 600, 550

# Set the color of the circle (in RGB format)
circle_color = (255, 0, 0)  # Red

#color of window background
colorOfBackground = (0, 10, 0)

# Set the color of the line (in RGB format)
line_color = (255, 255, 255)  # blue
border_line_color = (80, 50, 80)  # blue
line_thick = 10

# width of line
width_of_lines = 100


distance_from_window = 10

line_start_x_left = distance_from_window
line_end_x_left = distance_from_window
line_start_x_right = window_width - distance_from_window
line_end_x_right = window_width - distance_from_window

radius = 30

# Set the font for the exit button
exit_button_text = "Exit Game"
button_color = (255, 0, 0)
exit_button_text_color = (255, 255, 255)
exit_button_width = 100
exit_button_height = 50
exit_button_x = (window_width - exit_button_width) // 2
exit_button_y = (window_height - exit_button_height) // 2 + 100

# final score of game
finalScore = 10000

# backUp addres
backUpFilePath = "./modelBackUp.h5"
