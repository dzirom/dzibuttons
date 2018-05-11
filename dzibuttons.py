# -*- coding: utf-8 -*-

__author__ = 'Roman Domrachev'

''' 
dzi buttons game is my implementation of the Wrike buttons game I saw on the Codefest 2018 

author Roman Domrachev
email dzirom@gmail.com

'''

import random, sys

class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

class direction: 
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'

colors = [bcolors.PURPLE, bcolors.BLUE, bcolors.GREEN, bcolors.YELLOW, bcolors.RED]

def display_field():
    for i in range(buttons_len):
        for j in range(buttons_len):            
            print colors[buttons_colors[i][j]], 'X' if buttons_fixes[i][j] else 'O' ,
        print '\r', bcolors.ENDC

def run_color_chooser():
    for i in range(len(colors)):
        print colors[i], (i + 1),
    print bcolors.ENDC    
    strval = raw_input('Choose color (0 - exit): ')
    inputted_val = (int(strval) - 1) if strval.isdigit() else strval
    return inputted_val

class FieldNavigator(object):

    checks_map = {}
    pos_stack = []    

    def __init__(self):
        self.checks_map[direction.LEFT] = ([
                (self.check_up, self.shift_up), (self.check_left, self.shift_left), 
                (self.check_down, self.shift_down)
            ], self.shift_right)
        self.checks_map[direction.RIGHT] = ([
                (self.check_up, self.shift_up), (self.check_right, self.shift_right), 
                (self.check_down, self.shift_down)
            ], self.shift_left)
        self.checks_map[direction.UP] = ([
                (self.check_left, self.shift_left), (self.check_up, self.shift_up), 
                (self.check_right, self.shift_right)
            ], self.shift_down)
        self.checks_map[direction.DOWN] = ([
                (self.check_left, self.shift_left), (self.check_down, self.shift_down), 
                (self.check_right, self.shift_right), 
            ], self.shift_up)        

    def reset(self):
        del self.pos_stack[:]

    def navigate(self, direction, i, j, color_index, check_fixing = False, is_stack_disabled = False):
        checks, default_shift = self.checks_map[direction]
        result = None; si = 0; sj = 0; stack_item = None        
        for check, shift in checks:
            if check(i, j, color_index, check_fixing):
                if not result:
                    result = shift(i, j)
                elif not is_stack_disabled:
                    direction, si, sj = shift(i, j)
                    stack_item = (direction, i, j)
                    if (len(self.pos_stack) == 0 or self.pos_stack[-1] != stack_item): 
                        self.pos_stack.append(stack_item)       
        if result:
            return result
        elif len(self.pos_stack):    
            direction, si, sj = self.pos_stack.pop()
            return self.navigate(direction, si, sj, color_index, check_fixing, False)
        return (None, i, j)    

    def is_right_color(self, i, j, color_index):
        return (buttons_colors[i][j] == color_index)

    def shift_up(self, i, j):        
        return (direction.UP, i - 1, j)
    def shift_down(self, i, j):        
        return (direction.DOWN, i + 1, j)
    def shift_left(self, i, j):        
        return (direction.LEFT, i, j - 1)
    def shift_right(self, i, j):        
        return (direction.RIGHT, i, j + 1)

    def check_up(self, i, j, color_index, checkFixing):
        return i - 1 > 0 and self.is_right_color(i - 1, j, color_index) and (
            not checkFixing or checkFixing and not buttons_fixes[i - 1][j])
    def check_down(self, i, j, color_index, checkFixing):
        return i + 1 < buttons_len and (
            self.is_right_color(i + 1, j, color_index)) and (
                not checkFixing or checkFixing and not buttons_fixes[i + 1][j])
    def check_left(self, i, j, color_index, checkFixing):
        return j - 1 > 0 and self.is_right_color(i, j - 1, color_index) and (
            not checkFixing or checkFixing and not buttons_fixes[i][j - 1])
    def check_right(self, i, j, color_index, checkFixing):
        return j + 1 < buttons_len and (
            self.is_right_color(i, j + 1, color_index)) and (
                not checkFixing or checkFixing and not buttons_fixes[i][j + 1])

def fix_buttons(new_color_index):
    global fixed_buttons_count 
    cur_color_index = buttons_colors[0][0]

    # change color of the buttons    
    i = 0; j = 0; steps_count = 0
    fieldNavigator.reset()
    moving_direction = direction.RIGHT
    while (moving_direction != None):
        if buttons_colors[i][j] == cur_color_index:
            if buttons_fixes[i][j]:
                buttons_fixes[i][j] = False                 
                fixed_buttons_count -= 1
            buttons_colors[i][j] = new_color_index

        moving_direction, i, j = fieldNavigator.navigate(moving_direction, i, j, cur_color_index)
        steps_count += 1
        if steps_count > max_steps:
            print 'Warning there were too many steps. The algorithm will be interrupted'
            break

    # fix the buttons            
    i = 0; j = 0; steps_count = 0
    fieldNavigator.reset()
    moving_direction = direction.RIGHT
    
    while (moving_direction != None):
        if buttons_colors[i][j] == new_color_index and not buttons_fixes[i][j]:
            buttons_fixes[i][j] = True
            fixed_buttons_count += 1

        moving_direction, i, j = fieldNavigator.navigate(moving_direction, i, j, new_color_index, True)
        steps_count += 1
        if steps_count > max_steps:
            print 'Warning there were too many steps. The algorithm will be interrupted'
            break

    print 

def fill_field():
    for i in range(buttons_len):
        for j in range(buttons_len):
            color_index = random.randint(0, colors_len)
            buttons_colors[i][j] = color_index
            buttons_fixes[i][j] = False

# Initialization of the application
dem_str = '10'
dem = int(dem_str)
max_fixes = dem * dem
fieldNavigator = FieldNavigator()
print 'The field is %s x %s' % (dem, dem)

colors_len = len(colors) - 1
buttons_colors = [[0 for x in range(dem)] for y in range(dem)]
buttons_fixes = [[False for x in range(dem)] for y in range(dem)]
buttons_len = len(buttons_colors)
buttons_count = buttons_len * buttons_len
fixed_buttons_count = 0
max_steps = 2 * buttons_count

fill_field()
display_field()

def main():
    pressed_key = None
    choices_count = 0    
    global fixed_buttons_count

    while pressed_key != -1:    
        print 'Your choices count:', choices_count
        print 'Fixed buttons count: %s of %s' % (fixed_buttons_count, buttons_count)
        pressed_key = run_color_chooser()        
        if pressed_key == -1:
            break
        elif pressed_key >= 0 and pressed_key <= colors_len:    
            choices_count += 1
            fix_buttons(pressed_key)            
            if fixed_buttons_count == buttons_count:
                print 'Congratulations! :-) You won!'            
                pressed_key = raw_input('Press Enter to continue')
                if not pressed_key:
                    fixed_buttons_count = 0; choices_count = 0
                    fill_field()
                else:
                    break        
        display_field()
                    

if __name__ == '__main__':
    sys.exit(main())