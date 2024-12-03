import tkinter as tk
from tkinter import messagebox
import random
import const
from datetime import datetime  
  
now = datetime.now()  

import pygame  
import sys  

# 初始化pygame的mixer模块  
pygame.mixer.init()  
sound = pygame.mixer.Sound('music_background.mp3')   
sound1 = pygame.mixer.Sound("Video_1719025015963_20240622_105712.mp3")   
def play_sound():  
    sound.play()  



def draw(screen, begin_x, begin_y, color="#CCCCCC"):
    x0 = begin_x * const.size
    y0 = begin_y * const.size
    x1 = x0 + const.size
    y1 = y0 + const.size
    screen.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=2)


# 绘制空白面板
def draw_blank_board(screen,block_exit_list):
    for i in range(const.y):
        for j in range(const.x):
            if block_exit_list[i][j]:
                draw(screen,j,i,color="red")
            else:
                draw(screen, j, i)


def draw_blocks(screen, begin_x ,begin_y,block_list, color="#CCCCCC"):
    for block in block_list:
        dx, dy = block
        x = begin_x + dx
        y = begin_y + dy
        # 判断该位置方格在画板内部(画板外部的方格不再绘制)
        if 0 <= x < const.x and 0 <= y < const.y:
            draw(screen, x, y, color)


def draw_block_move(screen, blocks, direction=[0,0]):
    block_list = blocks['block_list']
    begin_x ,begin_y = blocks['xy']
    color = const.SHAPESCOLOR[blocks['kind']]
    dx,dy = direction
    #更新初始坐标
    blocks['xy'] = [begin_x + dx,begin_y + dy]    
    draw_blocks(screen,begin_x,begin_y,block_list)
    draw_blocks(screen,begin_x + dx,begin_y + dy,block_list,color)


def game_fresh():
    screen.update()

    global cur_blocks
    if cur_blocks is None:
        cur_blocks = create_new_blocks()
        draw_block_move(screen,cur_blocks,[0,1])
        if not is_move(cur_blocks, [0, 0]):
            messagebox.showinfo("Game Over!", "Your Score is %s" % score)
            screen.destroy()
            return
    else:
        if is_move(cur_blocks,[0,1]):
            draw_block_move(screen,cur_blocks,[0,1])
        else:   
            save_blocks(cur_blocks)
            cur_blocks = None
            clear()
            

    
    screen.after(const.FPS, game_fresh)


def create_new_blocks():
    kind = random.choice(list(const.SHAPES.keys()))
    new_blocks = {
        'kind':kind,
        'block_list':const.SHAPES[kind],
        'xy':[const.x//2,0]
    }
    return new_blocks

def is_move(blocks,direction):
    begin_x,begin_y = blocks['xy']
    for block in blocks['block_list']:   #直接计算方块的坐标，不计算像素点
        x = block[0] + begin_x + direction[0]
        y = block[1] + begin_y + direction[1]
        if x < 0 or x >= const.x or y >= const.y or (y >= 0 and block_exit_list[y][x]):
            return False
    return True

def save_blocks(blocks):
    block_list = blocks['block_list']
    begin_x,begin_y = blocks['xy']
    for i in block_list:    #类似于draw_blocks
        dx,dy = i
        x = begin_x + dx
        y = begin_y + dy
        block_exit_list[y][x] = True

def left_right_move(event):
    global cur_blocks
    if event.keysym == 'Left':
        direction = [-1, 0]
    elif event.keysym == 'Right':
        direction = [1, 0]
    else:
        return
    if cur_blocks is not None and is_move(cur_blocks,direction):
        draw_block_move(screen,cur_blocks,direction)


def rotate_blocks(event):   #中心坐标不变，相对坐标，x,y变为y,-x
    global cur_blocks
    if cur_blocks is None:
        return
    block_list = cur_blocks['block_list']
    rotate_list = []
    for i in block_list:
        y = -(i[0])
        x = i[1]
        rotate_list.append((x,y))
        #不能直接改变原cur_blocks，若旋转后‘越界’，会失去原值
    rotate_after_blocks = {
        'kind':cur_blocks['kind'],
        'block_list': rotate_list,
        'xy': cur_blocks['xy']
    }
    if is_move(rotate_after_blocks,[0,0]):
        begin_x, begin_y= cur_blocks['xy']
        draw_blocks(screen, begin_x, begin_y, cur_blocks['block_list']) #类似于draw_move
        draw_blocks(screen, begin_x, begin_y, rotate_list,const.SHAPESCOLOR[cur_blocks['kind']])
        cur_blocks = rotate_after_blocks


def drop(event):     #直接落至‘底部’，各相对坐标能移动的max_y取最小的一个
    global cur_blocks
    if cur_blocks is None:
        return
    block_list = cur_blocks['block_list']
    begin_x,begin_y = cur_blocks['xy']
    min_drop_distance = const.y
    
    for i in block_list:
        dx,dy = i
        x = begin_x + dx
        y = begin_y + dy
        max_every = 0
        if y >= 0 and block_exit_list[y][x]:
            return 
        for j in range(begin_y+1,const.y):                    #一行一行的搜索
            if block_exit_list[j][x]:
                break
            else:
                max_every += 1
        if max_every < min_drop_distance:
            min_drop_distance = max_every

    if is_move(cur_blocks, [0,min_drop_distance]):
        draw_block_move(screen,cur_blocks,[0,min_drop_distance])



def check_complete(row):
    for i in row:
        if i == False:
            return False

    return True


def clear():
    has_complete_row = False
    global score
    for ri in range(len(block_exit_list)):
        if check_complete(block_exit_list[ri]):
            has_complete_row = True
            # 当前行可消除
            if ri > 0:
                for cur_ri in range(ri, 0, -1):
                    block_exit_list[cur_ri] = block_exit_list[cur_ri-1][:]
                score += 10
                sound1.play()

                
                # block_exit_list[0] = ['' for j in range(const.x)]
            else:
                block_exit_list[0] = ['' for j in range(const.x)]      
    if has_complete_row:
        draw_blank_board(screen, block_exit_list)

        root.title("SCORES: %s" % score)



cur_blocks = None

block_exit_list = []    #使用二维矩阵记录哪些位置存在方块，使用方块的坐标
for i in range(const.y):
    i_t = []
    for j in range(const.x):
        i_t.append(False)
    block_exit_list.append(i_t)


score = 0

root = tk.Tk()
play_sound()
root.title("俄罗斯方块\tSCORE:\t%d"%score)
screen = tk.Canvas(root, width=const.width, height=const.height)
screen.pack()




draw_blank_board(screen,block_exit_list)   #初始化

screen.focus_set() # 聚焦到画板对象上
screen.bind("<KeyPress-Left>", left_right_move)
screen.bind("<KeyPress-Right>", left_right_move)
screen.bind("<KeyPress-Up>", rotate_blocks)
screen.bind("<KeyPress-Down>", drop)
screen.update()
screen.after(const.FPS, game_fresh)  # 在FPS 毫秒后调用 game_loop方法




root.mainloop()



with open('info.txt', 'a',encoding='utf-8') as file:
    file.write(str(score)+'\t'+str(now)+'\n')
pygame.quit()     
sys.exit()