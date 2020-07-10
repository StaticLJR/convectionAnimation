import numpy as np
import random as rn

########################################
#Object to create, track and draw
#rain droplets.
########################################

class rain_droplet:
    def __init__(self,x,y,max_alpha=1.):
        self.x = x 
        self.y = y
        self.initial_x = x 
        self.initial_y = y
        self.length = 0.005 + 0.01*rn.random()
        self.width = self.length/4.
        
        self.color = np.array([0.1,0.6,0.7])
        self.color_perturbation = 0.9 + 0.2*rn.random()
        self.color *= self.color_perturbation
        
        self.initial_max_alpha = max_alpha
        self.max_alpha = self.initial_max_alpha
        
    def change_coordinates(self,x,y):
        self.x = x
        self.y = y
        
    def change_alpha(self,factor):
        self.max_alpha = self.initial_max_alpha*factor

    def get_coordinates(self):
        return self.x,self.y
        
    def get_original_coordinates(self):
        return self.initial_x,self.initial_y
        
    def draw(self,image,x,y):
        
        def combine_colors(arr1,arr2):
            bottom = arr1
            top = arr2
            
            new = [0.,0.,0.,0.]
            new[3] = 1. - (1.-top[3])*(1.-bottom[3])
            if new[3] != 0.:
                for k in xrange(3):
                    new[k] = top[k]*top[3]/new[3] + bottom[k]*bottom[3]*(1.-top[3])/new[3]
            return new
        
        x_starti = np.abs(x-self.x).argmin()
        x_endi = np.abs(x-(self.x+self.width)).argmin()
        y_startj = np.abs(y-self.y).argmin()
        y_endj = np.abs(y-(self.y+self.length)).argmin()
        
        if y_startj > y_endj:
            temp = y_startj
            y_startj = y_endj
            y_endj = temp
            
        if x_starti > x_endi:
            temp = x_starti
            x_starti = x_endi
            x_endi = temp
        
        for j in xrange(y_startj,y_endj+1):
            for i in xrange(x_starti,x_endi+1):
                if image[j][i].tolist() != [1.,1.,1.,1.]:
                    image[j][i] = combine_colors(image[j][i],[self.color[0],self.color[1],self.color[2],self.max_alpha])
                    
        return image