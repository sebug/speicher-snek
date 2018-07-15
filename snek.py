import time
import random

# Hack to get ticks_ms() method in Tigerjython working
if not hasattr(time, 'ticks_ms'):
    from types import MethodType
    def ticks_ms(self):
        return int(round(self.time() * 1000))
    time.ticks_ms = MethodType(ticks_ms, time)
    
    def sleep_ms(self,a):
        time.sleep(a/1000.0)
    time.sleep_ms = MethodType(sleep_ms, time)
# END of Hack

board_width = 10
board_height = 15

class SnakeInstance:
    def __init__(self, corner, color):
        self.is_alive = True
        self.color = color
        self.to_remove = False
        self.autopilot = False
        start_x = 0
        start_y = 0
        if (corner == 0): # bottom left
            self.direction_x = 0
            self.direction_y = 1
        elif (corner == 1): # bottom right
            self.direction_x = -1
            self.direction_y = 0
            start_x = board_width - 1
            start_y = 0
        elif (corner == 2): # top right
            self.direction_x = 0
            self.direction_y = -1
            start_x = board_width - 1
            start_y = board_height - 1
        else: # top left
            self.direction_x = 1
            self.direction_y = 0
            start_x = 0
            start_y = board_height - 1
        self.coordinates = []
        x = start_x
        y = start_y
        for i in range(0,3):
            c = (x, y)
            self.coordinates.append(c)
            x += self.direction_x
            y += self.direction_y
            
    def move(self, mouse):
        if not self.is_alive:
            return False
        last_coordinate = self.coordinates[-1]
        x = last_coordinate[0]
        y = last_coordinate[1]
        eat_mouse = False
        if x == mouse.position[0] and y == mouse.position[1]:
            eat_mouse = True
        
        if (eat_mouse):
            self.to_remove = False
            self.coordinates.append((x + self.direction_x,y + self.direction_y))
            mouse.place_random(mouse.snakes)
        else:
            self.to_remove = self.coordinates[0]
            for i in range(0, len(self.coordinates) - 1):
                self.coordinates[i] = self.coordinates[i + 1]
            self.coordinates[len(self.coordinates) - 1] = (x + self.direction_x,y + self.direction_y)

    def die(self):
        self.is_alive = False
        self.color = [0,0,200]

    def check_collision(self, other_snake):
        last_coordinate = self.coordinates[-1]
        for c in other_snake.coordinates:
            if c[0] == last_coordinate[0] and c[1] == last_coordinate[1]:
                self.die()
        for c in self.coordinates[0:-1]:
            if c[0] == last_coordinate[0] and c[1] == last_coordinate[1]:
                self.die()    

    def paint(self, helper):
        if self.to_remove:
            helper.setPixel(self.to_remove[0], self.to_remove[1], [0,0,0])
        for coordinate in self.coordinates:
            helper.setPixel(coordinate[0], coordinate[1], self.color)
    
    def left(self):
        if self.direction_x == -1:
            self.direction_x = 0
            self.direction_y = -1
        elif self.direction_x == 1:
            self.direction_x = 0
            self.direction_y = 1
        elif self.direction_y == -1:
            self.direction_y = 0
            self.direction_x = 1
        else:
            self.direction_y = 0
            self.direction_x = -1
    
    def right(self):
        if self.direction_x == -1:
            self.direction_x = 0
            self.direction_y = 1
        elif self.direction_x == 1:
            self.direction_x = 0
            self.direction_y = -1
        elif self.direction_y == -1:
            self.direction_y = 0
            self.direction_x = -1
        else:
            self.direction_y = 0
            self.direction_x = 1

    def choose_automatically(self, mouse):
        snake_head = self.coordinates[-1]
        have_to_choose_random = False
        if self.direction_x == 0:
            if mouse.position[0] < snake_head[0]:
                if self.direction_y == 1:
                    self.left()
                else:
                    self.right()
            elif mouse.position[0] > snake_head[0]:
                if self.direction_y == 1:
                    self.right()
                else:
                    self.left()
            else:
                if mouse.position[1] > snake_head[1]:
                    have_to_choose_random = self.direction_y == -1
                elif mouse.position[1] < snake_head[1]:
                    have_to_choose_random = self.direction_y == 1
        else:
            if mouse.position[1] < snake_head[1]:
                if self.direction_x == 1:
                    self.right()
                else:
                    self.left()
            elif mouse.position[1] > snake_head[1]:
                if self.direction_x == 1:
                    self.left()
                else:
                    self.right()
            else:
                if mouse.position[0] > snake_head[0]:
                    have_to_choose_random = self.direction_x == -1
                elif mouse.position[0] < snake_head[0]:
                    have_to_choose_random = self.direction_x == 1
        if have_to_choose_random: # get unstuck if we're on the same line in the other direction
            if random.randint(0, 1) == 0:
                self.left()
            else:
                self.right()
    
    def contains_point(self, p):
        for p2 in self.coordinates:
            if p2[0] == p[0] and p2[1] == p[1]:
                return True
        return False
            
class Mouse:
    def __init__(self, snakes):
        self.snakes = snakes
        self.color = [200, 200, 0]
        self.place_random(snakes)
    
    def get_random_position(self):
        x = random.randint(0, board_width - 1)
        y = random.randint(0, board_height - 1)
        return (x,y)
    
    def is_in_snakes(self, p):
        for snake in self.snakes:
            if snake.contains_point(p):
                return True
        return False
    
    def place_random(self, snakes):
        p = self.get_random_position()
        while self.is_in_snakes(p):
            p = self.get_random_position()
        self.position = p
    
    def paint(self, helper):
        helper.setPixel(self.position[0], self.position[1], self.color)

class Snek:
    def __init__(self, helper):
        self.helper = helper;
        self.set_start_position()

    def set_start_position(self):
        self.snake1 = SnakeInstance(1, [200,0,0])
        self.snake2 = SnakeInstance(3, [0,200,0])
        self.snake2.autopilot = True
        self.mouse = Mouse([self.snake1, self.snake2])

    def reset(self):
        for i in range(0,150):
            self.helper.np[i]=(0,0,0)
        self.helper.np.write()
        
    def restart_game(self):
        self.set_start_position()
        self.play()

    def play(self):
        self.reset()
        
        interval = 500
        
        next_paint = time.ticks_ms() + interval
        bold = 0
        while True:
            ticks = time.ticks_ms()
            b = self.helper.getButtons() ^ 255 # Invert buttonsb = self.helper.getButtons() ^ 255
            while b!=0:  # Warten bis losgelassen
                bold = b
                b = self.helper.getButtons()^255
                self.helper.setLeds(b^255)
            if ticks > next_paint or b != 0:
                if bold&1 == 1:
                    self.snake1.left()
                elif bold&2 == 2:
                    self.snake1.right()
                elif bold&16 == 16:
                    self.snake2.autopilot = False
                    self.snake2.left()
                elif bold&32 == 32:
                    self.snake2.autopilot = False
                    self.snake2.right()
                elif bold&64 == 64:
                    self.snake2.autopilot = not self.snake2.autopilot
                elif bold&128 == 128:
                    self.restart_game()

                if self.snake2.autopilot:
                    self.snake2.choose_automatically(self.mouse)
                    
                if not self.snake1.is_alive and not self.snake2.is_alive:
                    self.restart_game()
                    
                bold = 0
                self.snake1.paint(self.helper)
                self.snake2.paint(self.helper)
                self.mouse.paint(self.helper)
                self.snake1.move(self.mouse)
                self.snake2.move(self.mouse)
                self.snake1.check_collision(self.snake2)
                self.snake2.check_collision(self.snake1)
                self.helper.np.write()
                if ticks > next_paint:
                    next_paint += interval

    
            
            
        
