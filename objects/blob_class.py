import numpy as np
import random as rn

################################################
#Creates cloudy "blob" object. When combined with 
#other "blobs" in close proximity, a cloud-like
#image is created.
################################################

class blob:
    def __init__(self,x,y,height,max_alpha=0.9):
        self.x = x 
        self.y = y
        self.initial_x = x 
        self.initial_y = y
        self.radius = 0.05 + 0.1*rn.random()
        self.grey_perturbation = 0.05 - 0.1*rn.random()
        self.grey = height + self.grey_perturbation
        self.grey = min(0.65,self.grey)
        self.grey = max(0.35,self.grey)
        
        self.initial_max_alpha = max_alpha - 0.3*rn.random()
        self.max_alpha = self.initial_max_alpha
        
    def translate(self,dx,dy):
        self.x += dx
        self.y += dy
        
    def change_coordinates(self,x,y):
        self.x = x
        self.y = y
        
    def change_grey(self,height):
        self.grey = height + self.grey_perturbation
        self.grey = min(0.75,self.grey)
        self.grey = max(0.35,self.grey)
        
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
        
        x_starti = np.abs(x-(self.x-self.radius)).argmin()
        x_endi = np.abs(x-(self.x+self.radius)).argmin()
        y_startj = np.abs(y-(self.y-self.radius)).argmin()
        y_endj = np.abs(y-(self.y+self.radius)).argmin()
        
        if x_starti > x_endi:
            temp = x_starti
            x_starti = x_endi
            x_endi = temp
            
        if y_startj > y_endj:
            temp = y_startj
            y_startj = y_endj
            y_endj = temp
        
        for j in xrange(y_startj,y_endj+1):
            for i in xrange(x_starti,x_endi+1):
                r = np.sqrt((x[i]-self.x)**2 + (y[j]-self.y)**2)/self.radius
            
                if r < 1:
                    alpha = self.max_alpha*np.cos(r*np.pi/2.)**2
                    
                    image[j][i] = combine_colors(image[j][i],[self.grey,self.grey,self.grey,alpha])
                    
        return image