import numpy as np
import random as rn
from rain_droplet_class import rain_droplet

def combine_colors(bottom,top):
    new = [0.,0.,0.,0.]
    new[3] = 1. - (1.-top[3])*(1.-bottom[3])
    if new[3] != 0.:
        for k in xrange(3):
            new[k] = top[k]*top[3]/new[3] + bottom[k]*bottom[3]*(1.-top[3])/new[3]
    return new

def generate_rain_droplets(x,y,dims,rain_droplets):
    print "Generating initial cloud profile."

    xmin,xmax,xmid,xdiff,ymin,ymax,ymid,ydiff = dims
    
    droplet_probability = 300/(1.*len(x)*len(y))
    
    for j in xrange(0,len(y)):
        for i in xrange(0,len(x)-len(x)/10):
            if rn.random() < droplet_probability:
                rain_droplets.append(rain_droplet(x[i],y[j]))
    
    return rain_droplets
    
def update_rain(image,x,y,t,dims,rain_droplets,omega=np.pi/3.,startup_time=3.):
    xmin,xmax,xmid,xdiff,ymin,ymax,ymid,ydiff = dims
    
    theta = omega*t
    
    alpha_factor = 1.
    if t <= startup_time:
        alpha_factor = 0.
    elif t < 2*startup_time:
        temp = (t - startup_time)/startup_time
        alpha_factor = 1. - 0.5*(1. + np.cos(temp * np.pi))
    
    if alpha_factor != 0.:
        for droplet in rain_droplets:
            xdroplet_init,ydroplet_init = droplet.get_original_coordinates()

            x_new = xdroplet_init
            y_new = ( ydroplet_init - ymin + (t%startup_time)/startup_time*ydiff )%ydiff + ymin
            droplet.change_coordinates(x_new,y_new)
            
            alpha = np.cos( 2*(y_new-ymid)/ydiff * np.pi/2. )**2
            if x_new < xmid:
                alpha *= np.sin( (x_new-xmin)/xdiff * np.pi/2. )**2
            alpha *= alpha_factor
            droplet.change_alpha(alpha)
            
            if alpha != 0.:
                droplet.draw(image,x,y)
        
    return image