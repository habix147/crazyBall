import random

import pygame
import time
import config
import functions
import opponentCircleMovement
import os

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
window = pygame.display.set_mode((config.window_width, config.window_height))

# Set the center coordinates
center_x, center_y = config.window_width // 2, config.window_height // 2
p_center_x = center_x
p_center_y = center_y
# y position of opponent plate in game
y_opponent = center_y
# define postoin of circle in window
edgeState = None
# delay of end of every frame to slow down game
sleepTime = 0

# if this flag set to True mean that the direction of circle should be changed
movement_fleg = False
movement_x = 1
movement_y = 1
faultForMOveToCourner = False;
# Main game loop
running = True

# score of players in the game
player1_score = 0
player2_score = 0

# control line parameter
    # Define the RL Environment
state_size = 3  # Assuming the state is represented by center_y and y_opponent
action_size = 1  # Assuming the action is a single continuous value
action_min_value = -4
action_max_value = 4
buffer_size = 100000  # Set your preferred buffer size
discount_factor = 0.95
opponentRl = opponentCircleMovement.RLAgent(state_size, action_size, action_min_value, action_max_value, discount_factor, buffer_size   )
# if recently model trained
if os.path.exists(config.backUpFilePath):
    opponentRl.load_backup_model(config.backUpFilePath)
reward = 0

circle_movement_sample_counter = 0

howManyTimeLearnCyckeHappen = 1

howManyTimeLearnCyckeHappenNum = 5
howManyTimeLearnCyckeHappenCof = 10

predictActionNumber = 4
predictActionNumber_counter = 0
y_opponent_movement = 0

while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Generate random movement for the circle
    if movement_fleg:
        movement_fleg, movement_x, movement_y = functions.circleMovement(movement_fleg, center_x, center_y, p_center_x, p_center_y, edgeState)

    # Update the center coordinates of the circle
    p_center_x = center_x
    p_center_y = center_y
    center_x += movement_x
    center_y += movement_y

    # check location of circle and if circle recive the edge of screen it allow to change direction of circle
    movement_fleg, edgeState = functions.circleDirection(center_x, center_y)

    # Fill the window with a background color
    window.fill(config.colorOfBackground)  # Black

    # Get the current position of the mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    #opponent action
    if predictActionNumber_counter == predictActionNumber:
        y_opponent_movement = opponentRl.get_action(center_x, center_y, y_opponent)
        predictActionNumber_counter = 0
    predictActionNumber_counter +=1
    # print(y_opponent_movement)
    y_old_state = y_opponent # this variable used in add_experiment function of RLAgent class
    if( ((y_opponent + y_opponent_movement) <= (config.window_height - (config.width_of_lines/2))) and ((y_opponent + y_opponent_movement) >= (config.width_of_lines/2)) ):
        y_opponent += y_opponent_movement
        faultForMOveToCourner = False
    else:
        faultForMOveToCourner = True

    # Draw the circle on the window
    pygame.draw.circle(window, config.circle_color, (center_x, center_y), config.radius) #circle
    # Draw the control line on the window
    pygame.draw.line(window, config.line_color, (config.line_start_x_left, mouse_y-(config.width_of_lines/2)), (config.line_end_x_left, mouse_y+(config.width_of_lines/2)), config.line_thick)  # line3 left of window
    #  Draw the control line of opponent on the window
    pygame.draw.line(window, config.line_color, (config.line_start_x_right, y_opponent-(config.width_of_lines/2)), (config.line_end_x_right, y_opponent+(config.width_of_lines/2)), config.line_thick)  # line4 right of window
    # Draw windows border
    pygame.draw.line(window, config.border_line_color, (0, config.window_height-config.line_thick), (config.window_width, config.window_height-config.line_thick), config.line_thick+12)
    pygame.draw.line(window, config.border_line_color, (0, config.line_thick), (config.window_width, config.line_thick), config.line_thick+12)

    # display score of two player on screen:
    window.blit(functions.update_scores(player1_score, player2_score), (config.window_width/4, 1))  # Adjust the position as per your preference

    # Update the display
    pygame.display.flip()
    time.sleep(sleepTime)

    # referee part
    quitGame = functions.referee(mouse_y, center_y, y_opponent, edgeState)
    if(quitGame & (player2_score == config.finalScore or player1_score == config.finalScore) ):
        running = False
    else:
        if(edgeState == 'left' and not quitGame):
            player1_score += 1
        elif(edgeState == 'right' and not quitGame):
            player2_score += 1

    # reward function for take reward to action of opponent movement in game
    reward = opponentCircleMovement.opponentReward(y_opponent_movement, y_opponent, center_y, quitGame, edgeState, faultForMOveToCourner)

    # create train dataset to train model for y_controller of opponent player, (s, a, R(s), s')
    opponentRl.add_experience((p_center_x, p_center_y, y_old_state), y_opponent_movement, reward, (center_x, center_y, y_opponent))

    # training model
    #if(edgeState == 'right'):
     #   if howManyTimeLearnCyckeHappen == (howManyTimeLearnCyckeHappenNum * howManyTimeLearnCyckeHappenCof):
      #      thereshold = 500
       #     opponentRl.train_q_value_function_threaded(thereshold)
        #    circle_movement_sample_counter = 0
         #   opponentRl.free_up_buffer()
          #  howManyTimeLearnCyckeHappen = -1
           # howManyTimeLearnCyckeHappenCof +=1
        #howManyTimeLearnCyckeHappen += 1
    #circle_movement_sample_counter += 1


#------------------------------------final score display-----------------------------------------

exit_button_font = pygame.font.Font(None, 24)
finalScore = True
finalWindow = pygame.display.set_mode((config.window_width, config.window_height))
while finalScore:
    # Check for events in the final score window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finalScore = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if the mouse click is within the button's bounds
            if config.exit_button_x <= mouse_x <= config.exit_button_x + config.exit_button_width and config.exit_button_y <= mouse_y <= config.exit_button_y + config.exit_button_height:
                finalScore = False

    # Fill the final score window with a background color
    finalWindow.fill(config.colorOfBackground)

    # Render and display the final score
    finalWindow.blit(functions.update_scores(player1_score, player2_score), (config.window_width // 4, config.window_height // 2))

    # Draw the exit button
    pygame.draw.rect(finalWindow, config.button_color, (config.exit_button_x, config.exit_button_y, config.exit_button_width, config.exit_button_height))
    config.exit_button_text_surface = exit_button_font.render(config.exit_button_text, True, config.exit_button_text_color)
    config.exit_button_text_x = config.exit_button_x + (config.exit_button_width - config.exit_button_text_surface.get_width()) // 2
    config.exit_button_text_y = config.exit_button_y + (config.exit_button_height - config.exit_button_text_surface.get_height()) // 2
    finalWindow.blit(config.exit_button_text_surface, (config.exit_button_text_x, config.exit_button_text_y))

    # Update the final score window display
    pygame.display.flip()


# Quit Pygame
pygame.quit()
