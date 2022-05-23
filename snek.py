import curses
import time
from random import randint
from math import floor


def end(stdscr, snek_len) : 
    stdscr.clear()
    stdscr.addstr(0, std_x // 2 - 4, "Game Over")
    stdscr.nodelay(False)
    
    txt = f"Your Score was {snek_len // 3 - 1}"
    stdscr.addstr(
        1, std_x // 2 - len(txt) // 2, 
        txt, curses.color_pair(2)
    )
    txt = "[Press any key to continue]"
    stdscr.addstr(
        2, std_x // 2 - 13,
        txt, curses.color_pair(3) | curses.A_BOLD
    )
    stdscr.refresh()
    
    curses.napms(100)
    stdscr.getch()
    exit()



def main(stdscr) :
    curses.init_pair(1, curses.COLOR_RED, 0)
    curses.init_pair(2, curses.COLOR_GREEN, 0)
    curses.init_pair(3, curses.COLOR_BLACK, 0)
    
    stdscr.nodelay(True)
    stdscr.border()
    
    curses.curs_set(0)
    
    global std_y, std_x
    std_y = stdscr.getmaxyx()[0]
    std_x = stdscr.getmaxyx()[1]
    
    stdscr.addstr(0, std_x // 2 - 2, "Snek", curses.A_REVERSE)
    
    snek_pos = [randint(1, std_y - 2), randint(1, std_x // 2 - 2) * 2]
    apple_pos = [15, std_x // 2]
    
    snek_speed = 1
    delay = 0.15
    dir = 0, 0
    snek_len, bodies_pos = 5, []
    
    started = False
    prev_time = 0
    while True :
        key = stdscr.getch()
       
        # lowercase'd
        if key in (ord('W'), ord('A'), ord('S'), ord('D')) :
            key += 32

        # UP
        if key in (ord('w'), 450) :
            dir = (-snek_speed, 0) if dir[0] != snek_speed else dir
        # LEFT
        elif key in (ord('a'), 452) :
            dir = (0, -snek_speed * 2) if dir[1] != snek_speed * 2 else dir
        # DOWN
        elif key in (ord('s'), 456) :
            dir = (snek_speed, 0) if dir[0] != -snek_speed else dir
        # RIGHT
        elif key in (ord('d'), 454) :
            dir = (0, snek_speed * 2)  if dir[1] != -snek_speed * 2 else dir
        
        # screen resize
        elif key == curses.KEY_RESIZE :
            std_y, std_x = stdscr.getmaxyx()
            stdscr.clear()
            stdscr.border()
            
        if key in (119, 97, 115, 100) :
            started = True
        
        # halt any other process for a certain amount of 
        # time other than the inputs
        if time.perf_counter() - prev_time < delay :
            continue
        prev_time = time.perf_counter()
        
        
        #----- snek stuff -----#
        
        # set snek new pos
        snek_pos = [sum(x) for x in zip(snek_pos, dir)]
        
        # put snek's body pos into a list
        bodies_pos.append(snek_pos)
            
        # delete snek's tail
        if len(bodies_pos) > snek_len :
            stdscr.addstr(*bodies_pos[0], "  ")
            bodies_pos.pop(0) 
        
        # print the snek
        for i, body in enumerate(bodies_pos) :
            # if head
            attr = curses.color_pair(2) | curses.A_REVERSE
            stdscr.addstr(*body, "  ", attr)
        
        # if head hits body
        if bodies_pos[-1] in bodies_pos[:-1] and started :
            end(stdscr, snek_len)
        
        # if head hits border 
        head = bodies_pos[-1] 
        if head[0] in (0, std_y - 1) or head[1] in (0, std_x - 2) :
            end(stdscr, snek_len)
        
        
        #----- apple -----#
        
        # if snek eats apple
        if bodies_pos[-1] == apple_pos :
            # repeat if apple spawn inside the snek
            while apple_pos in bodies_pos :
                apple_pos[0] = randint(1, std_y - 2)
                apple_pos[1] = randint(1, std_x // 2 - 2) * 2
            snek_len += 3
        
        apple_attr = curses.color_pair(1) | curses.A_REVERSE
        stdscr.addstr(*apple_pos, "  ", apple_attr)
        stdscr.addstr(0, 1, f"Score : {snek_len // 3 - 1}")
        
            
        
time.sleep(0.05) # fuck. key. board. re. size
curses.wrapper(main)