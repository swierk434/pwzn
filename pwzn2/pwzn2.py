#python pwzn2.py 100 1 10 0 100 0.5 -a animation -m magnetization
#python pwzn2.py 500 1 10 0 100 0.5 -a animation for numba compare

import rich
import argparse
import numpy as np
import random as rn
from PIL import Image
from rich.progress import track
import time

rich.get_console().clear()

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

def deltaH(s, index1, index2, J, B):
    n = len(s)
    #print(s[index1][index2]*s[(index1+1)%n][index2], s[index1][index2]*s[(index1-1)%n][index2], s[index1][index2]*s[index1][(index2+1)%n], s[index1][index2]*s[index1][(index2-1)%n])
    return (J*(s[index1][index2]*s[(index1+1)%n][index2] + s[index1][index2]*s[(index1-1)%n][index2] + s[index1][index2]*s[index1][(index2+1)%n] + s[index1][index2]*s[index1][(index2-1)%n]) + B*s[index1][index2])*2

class simulation:
    def __init__(self, n, J, beta, B, N, ro, image_name = None, animation_name = None, magnetiztion_name = None):
        self.n = n
        self.J = J
        self.beta = beta
        self.B = B
        self.N = N
        self.ro = ro
        self.imgae_name = image_name
        self.animation_name = animation_name
        self.magnetiztion_name = magnetiztion_name
        self.grid = np.ones((n, n))
        self.step = 0
        
        for index1 in range(len(self.grid)):
            for index2 in range(len(self.grid[index1])):
                if rn.random() <= args.ro:
                    self.grid[index1][index2] = -1
    
    def M(self):
        return np.sum(self.grid)/(self.n*self.n)
        
    def mikro_step(self):
        index1 = rn.randint(0, self.n-1)
        index2 = rn.randint(0, self.n-1)
        #flags
        # print(self.grid)
        # print(index1, index2)
        # print(deltaH(self.grid, index1, index2, self.J, self.B))
        # print(np.exp(-self.beta*deltaH(self.grid, index1, index2, self.J, self.B)))
        if rn.random() < np.exp(-self.beta*deltaH(self.grid, index1, index2, self.J, self.B)):
            self.grid[index1][index2] *= -1

    def makro_step(self):
        for n in range(self.n*self.n):
            self.mikro_step()
        self.step += 1   
    
    def make_image(self):
        image_array = np.where(self.grid == 1, 255, 0).astype(np.uint8) 
        #print(image_array)
        image = Image.fromarray(image_array)
        return image

    def save_image(self):
        if not self.imgae_name == None:
            self.make_image().save(self.imgae_name + '_' + str(self.step) + '.png')

    def run(self):
        frames = []
        start = time.time()
        if not self.magnetiztion_name == None:
            with open(self.magnetiztion_name + '.txt', 'w') as file:
                file.write(str(self.M()) + " " + str(self.step) + "\n")
                for n in track(range(self.N)):
                    self.save_image()
                    image = self.make_image()
                    frames.append(image)
                    self.makro_step()
                    file.write(str(self.M()) + " " + str(self.step) + "\n")
        else:
            for n in track(range(self.N)):
                    self.save_image()
                    image = self.make_image()
                    frames.append(image)
                    self.makro_step()
        print(time.time()-start)
        if not self.animation_name == None:
            frames[0].save((self.animation_name + '.gif'), save_all=True, append_images=frames[1:], duration=100, loop=0)

sim = simulation(args.n, args.J, args.beta, args.B, args.N, args.ro, args.image_name, args.animation_name, args.magnetiztion_name)

#sim.mikro_step()
#print(sim.grid)
#sim.make_image()
#print(sim.grid)
#print(deltaH(sim.grid, 0, 0, 1, 0))
# sim.mikro_step()
#sim.makro_step()

sim.run()