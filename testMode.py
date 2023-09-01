import time
import config
import functions
import opponentCircleMovement
import os

# Set the center coordinates
center_x, center_y = config.window_width // 2, config.window_height // 2
p_center_x = center_x
p_center_y = center_y
# y position of opponent plate in game
y_opponent = center_y
# define postoin of circle in window
edgeState = None

# if this flag set to True mean that the direction of circle should be changed
movement_fleg = False
movement_x = 1
movement_y = 1
# Main game loop
running = True


# control line parameter
# Define the RL Environment
state_size = 3  # Assuming the state is represented by center_y and y_opponent
action_size = 1  # Assuming the action is a single continuous value
action_min_value = -4
action_max_value = 4
buffer_size = 15000  # Set your preferred buffer size
discount_factor = 0.95
opponentRl = opponentCircleMovement.RLAgent(state_size, action_size, action_min_value, action_max_value, discount_factor, buffer_size)

# if recently model trained
if os.path.exists(config.backUpFilePath):
    opponentRl.load_backup_model(config.backUpFilePath)


howManyTimeLearnCyckeHappen = 1


predictActionNumber = 4
predictActionNumber_counter = 0
y_opponent_movement = 0


number_of_true_prediction = 0
number_of_true_prediction_old = 0


number_of_test_mode_cycle = int(input("how many sample need for this test? "))

print("test begin.")

while running:
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

    mouse_y = 0  # this value just for referee function

    # opponent action
    if predictActionNumber_counter == predictActionNumber:
        y_opponent_movement = opponentRl.get_action(center_x, center_y, y_opponent)
        predictActionNumber_counter = 0
    predictActionNumber_counter += 1

    if (((y_opponent + y_opponent_movement) <= (config.window_height - (config.width_of_lines / 2))) and ((y_opponent + y_opponent_movement) >= (config.width_of_lines / 2))):
        y_opponent += y_opponent_movement

    # referee part
    quitGame = functions.referee(mouse_y, center_y, y_opponent, edgeState)

    if (not quitGame):
        if (edgeState == 'right'):
            number_of_true_prediction += 1


    if howManyTimeLearnCyckeHappen == (number_of_test_mode_cycle):
        print("*******************************")
        print("*                             *")
        print("number of true prediction: ", number_of_true_prediction)
        print("rate", (number_of_true_prediction/number_of_test_mode_cycle))
        print("*                             *")
        print("*******************************")
        number_of_true_prediction = 0
        print("test mode ended")
        break

    if (edgeState == 'right'):
        howManyTimeLearnCyckeHappen += 1

    if (edgeState == 'right'):
        if (howManyTimeLearnCyckeHappen % 10 == 0):
            print("test mode: ")
            print("Ball Cycle: ", howManyTimeLearnCyckeHappen)
