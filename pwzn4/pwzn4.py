#python pwzn4.py 100 1 10 0 100 0.5 -a animation -m magnetization
#python pwzn4.py 500 1 10 0 100 0.5 -a animation

import numba
import argparse
import numpy as np
import random as rn
from PIL import Image
import time


parser = argparse.ArgumentParser()
parser.add_argument('n', default = 5, type=int)
parser.add_argument('J', type=float)
parser.add_argument('beta', type=float)
parser.add_argument('B', type=float)
parser.add_argument('N', type=int)
parser.add_argument('ro', default=0.5 ,type=float)
parser.add_argument('-i','--image_name', default = None)
parser.add_argument('-a','--animation_name', default = None)
parser.add_argument('-m','--magnetiztion_name', default = None)

args = parser.parse_args()

@numba.njit    
def M(grid, n):
    out = np.sum(grid)
    out = out / (n*n)
    return out

@numba.njit
def deltaH(s, index1, index2, J, B):
    n = len(s)
    return (J*(s[index1][index2]*s[(index1+1)%n][index2] + s[index1][index2]*s[(index1-1)%n][index2] + s[index1][index2]*s[index1][(index2+1)%n] + s[index1][index2]*s[index1][(index2-1)%n]) + B*s[index1][index2])*2

@numba.njit
def mikro_step(grid, n, beta , J, B):
        index1 = rn.randint(0, n-1)
        index2 = rn.randint(0, n-1)
        if rn.uniform(0, 1) < np.exp(-beta*deltaH(grid, index1, index2, J, B)):
            grid[index1][index2] *= -1

@numba.njit
def makro_step(grid, n, beta, J, B, step):
        for m in range(n*n):
            mikro_step(grid, n, beta, J, B)
            step += 1 
        return grid 

def make_image(grid):
    image_array = np.where(grid == 1, 255, 0).astype(np.uint8) 
    image = Image.fromarray(image_array)
    return image

def save_image(grid, imgae_name, step):
        if not imgae_name == None:
            make_image(grid).save(imgae_name + '_' + str(step) + '.png')

@numba.njit
def make_grid(n):
    grid = np.ones((n, n))
    for index1 in range(len(grid)):
        for index2 in range(len(grid[index1])):
            if rn.random() <= ro:
                grid[index1][index2] = -1
    return grid

n = args.n
J = args.J
beta = args.beta
B = args.B
N =args.N
ro = args.ro
image_name = args.image_name
animation_name = args.animation_name
magnetization_name = args.magnetiztion_name
grid = make_grid(n)
step = 0
frames = []
start = time.time()
if not magnetization_name == None:
    with open(magnetization_name + '.txt', 'w') as file:
        file.write(f'{M(grid, n)}  {str(step)}\n')
        for m in range(N):
            save_image(grid, image_name, step)
            image = make_image(grid)
            frames.append(image)
            grid = makro_step(grid, n, beta, J, B, step)
            file.write(str(M(grid, n)) + " " + str(step) + "\n")
else:
    for m in range(N):
            save_image(grid, image_name, step)
            image = make_image(grid)
            frames.append(image)
            grid = makro_step(grid, n, beta, J, B, step)
print(time.time()-start)
if not animation_name == None:
    frames[0].save((animation_name + '.gif'), save_all=True, append_images=frames[1:], duration=100, loop=0)