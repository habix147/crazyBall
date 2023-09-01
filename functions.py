import config
import random
import pygame

# check location of circle and if circle recive the edge of screen it allow to change direction of circle
def circleDirection(center_x, center_y):
    condition1 = (center_x > config.window_width - (config.radius+config.distance_from_window+config.line_thick))
    condition2 = (center_x < (config.radius+config.distance_from_window+config.line_thick))
    condition3 = ((center_y > config.window_height - (config.radius+config.distance_from_window+config.line_thick)))
    condition4 = ((center_y < (config.radius+config.distance_from_window+config.line_thick)))
    if (condition1 or condition2 or condition3 or condition4):
        movement_flag = True
        # here gameover checked
        # Check location of circle and determine which side it has touched
        if center_x <= config.radius + config.distance_from_window + config.line_thick:
            # Circle touched the left side
            return movement_flag, 'left'

        elif center_x >= config.window_width - (config.radius + config.distance_from_window + config.line_thick):
            # Circle touched the right side
            return movement_flag, 'right'

        elif center_y <= config.radius + config.distance_from_window + config.line_thick:
            # Circle touched the top side
            return movement_flag, 'top'

        elif center_y >= config.window_height - (config.radius + config.distance_from_window + config.line_thick):
            # Circle touched the bottom side
            return movement_flag, 'bottom'
    else:
        return False, None #movement_flag, state

def zeroCorr(num, state, epsilon):
    if(num == 0):
        if(state == -1):
            return -epsilon
        else:
            return epsilon
    else:
        return num

# Generate random movement for the circle
def circleMovement(movement_fleg, center_x, center_y, p_center_x, p_center_y, edgeState):
    counter = 1
    epsilon = 0.01
    if movement_fleg:
        while True:
            center_x_test = center_x
            center_y_test = center_y
            if(p_center_x < center_x and p_center_y > center_y):
                if(edgeState == 'top'):
                    movement_x = random.randint(1, config.max_movement)
                    movement_y = random.randint(1, config.max_movement)
                else:#right
                    movement_x = random.randint(-config.max_movement, -1)
                    movement_y = random.randint(-config.max_movement, -1)
            elif(p_center_x > center_x and p_center_y > center_y):
                if(edgeState == "top"):
                    movement_x = random.randint(-config.max_movement, -1)
                    movement_y = random.randint(1, config.max_movement)
                else:#left
                    movement_x = random.randint(1, config.max_movement)
                    movement_y = random.randint(-config.max_movement, -1)
            elif(p_center_x > center_x and p_center_y < center_y):
                if(edgeState == 'left'):
                    movement_x = random.randint(1, config.max_movement)
                    movement_y = random.randint(1, config.max_movement)
                else:#bottom
                    movement_x = random.randint(-config.max_movement, -1)
                    movement_y = random.randint(-config.max_movement, -1)
            elif(p_center_x < center_x and p_center_y < center_y):
                if(edgeState == 'right'):
                    movement_x = random.randint(-config.max_movement, -1)
                    movement_y = random.randint(1, config.max_movement)
                else: #bottom
                    movement_x = random.randint(1, config.max_movement)
                    movement_y = random.randint(-config.max_movement, -1)
            else:
                movement_x = random.randint(-config.max_movement, config.max_movement)
                movement_y = random.randint(-config.max_movement, config.max_movement)

            if (counter > 10):
                center_x_test = center_x
                center_y_test = center_y
                if(edgeState == 'top'):
                    # if(p_center_x < center_x and p_center_y > center_y):
                    if(random.randint(0, 1)):
                        movement_x = 1
                        movement_y = 1
                    else:
                        movement_x = -1
                        movement_y = 1
                if(edgeState == 'right'):
                    # if(p_center_x < center_x and p_center_y < center_y):
                    if(random.randint(0, 1)):
                        movement_x = -1
                        movement_y = 1
                    else:
                        movement_x = -1
                        movement_y = -1
                if(edgeState == 'bottom'):
                    # if(p_center_x > center_x and p_center_y < center_y):
                    if(random.randint(0, 1)):
                        movement_x = 1
                        movement_y = -1
                    else:
                        movement_x = -1
                        movement_y = -1
                if(edgeState == 'left'):
                    # if(p_center_x > center_x and p_center_y > center_y):
                    if(random.randint(0, 1)):
                        movement_x = 1
                        movement_y = -1
                    else:
                        movement_x = 1
                        movement_y = 1
                # print('crash acqure')
                print('** ## **')
                break

            center_x_test += movement_x
            center_y_test += movement_y
            # check next location of circle and if the next locatio is out of screen determine new movement
            condition1 = (center_x_test <= config.window_width-(config.radius+config.distance_from_window+config.line_thick))
            condition2 = (center_x_test >= (config.radius+config.distance_from_window+config.line_thick))
            condition3 = (center_y_test <= config.window_height-(config.radius+config.distance_from_window+config.line_thick))
            condition4 = (center_y_test >= (config.radius+config.distance_from_window+config.line_thick))
            # print(counter)
            if(condition1 and condition2 and condition3 and condition4):
                break
            counter +=1
        movement_fleg = False
        return movement_fleg, movement_x, movement_y

def referee(mouse_y, center_y, y_opponent, edgeState):
    quitGame = False
    if(edgeState == 'left'):
        if(mouse_y-(config.width_of_lines/2)<center_y<mouse_y+(config.width_of_lines/2)):
            quitGame = False
            return quitGame
        else:
            quitGame = True
            return quitGame
    elif(edgeState == 'right'):
        if (y_opponent - (config.width_of_lines / 2) < center_y < y_opponent + (config.width_of_lines / 2)):
            quitGame = False
            return quitGame
        else:
            quitGame = True
            return quitGame
    else:
        quitGame = False
        return quitGame


def update_scores(player1_score, player2_score):
    font = pygame.font.Font(None, 36)
    score_text = font.render("Player 1: {}   Player 2: {}".format(player1_score, player2_score), True, (255, 255, 255))
    return(score_text)
