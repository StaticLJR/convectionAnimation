import numpy as np
import random as rn
import math
from blob_class import blob

def combine_colors(bottom,top):
    new = [0.,0.,0.,0.]
    new[3] = 1. - (1.-top[3])*(1.-bottom[3])
    if new[3] != 0.:
        for k in xrange(3):
            new[k] = top[k]*top[3]/new[3] + bottom[k]*bottom[3]*(1.-top[3])/new[3]
    return new

def generate_clouds(x,y,dims):
    print "\nGenerating initial cloud profile."
    
    clouds = []
    xmin,xmax,xmid,xdiff,ymin,ymax,ymid,ydiff = dims
    
    radius = ymax/2.
    # circle_centre_x = xmax - radius - radius/2. 
    circle_centre_x = xmax - radius - radius/2. - radius/20.
    circle_centre_y = ymid
    
    cloud_probability = 110*10/(1.*len(x)*len(y))
    
    for j in xrange(0,len(y)):
        temp = radius**2 - (y[j]-circle_centre_y)**2
        if temp >= 0.:
            x_start = np.sqrt(temp) + circle_centre_x
            
            dx = x[1]-x[0]
            x_starti = np.abs(x-x_start).argmin()
            x_endi = x_starti + int( (xmax - circle_centre_x)/dx )
            for i in xrange(x_starti,x_endi):
                if rn.random() < cloud_probability:
                    grey_scale  = 0.25 + 0.5*(y[j]-ymin)/ydiff
                    clouds.append(blob(x_start + (i-x_starti)*dx,y[j],grey_scale))
    
    return clouds
    
def update_clouds_updraft(image,x,y,t,dims,clouds,omega=np.pi/3.,startup_time=3.):
    xmin,xmax,xmid,xdiff,ymin,ymax,ymid,ydiff = dims
    
    radius = ymax/2.
    circle_centre_y = ymid
    
    theta = omega*t
    
    alpha_factor = 1.
    if t <= startup_time:
        alpha_factor = 0.
    elif t < 2*startup_time:
        temp = (t - startup_time)/startup_time
        alpha_factor = 1. - 0.5*(1. + np.cos(temp * np.pi))
    
    if alpha_factor != 0.:
        for cloud in clouds:
            xcloud,ycloud = cloud.get_coordinates()
            xcloud_init,ycloud_init = cloud.get_original_coordinates()
            temp = radius**2 - (ycloud_init-circle_centre_y)**2
            if temp >= 0.:
                circle_centre_x = xcloud_init - np.sqrt(temp)
                angle = math.atan2(ycloud_init-circle_centre_y,xcloud_init-circle_centre_x)
                angle = (angle+theta+np.pi/2.)%(np.pi) - np.pi/2. #+ np.pi/8.
                
                x_new = circle_centre_x + radius*np.cos(angle)
                y_new = circle_centre_y + radius*np.sin(angle)
                cloud.change_coordinates(x_new,y_new)
            
                grey_scale  = 0.25 + 0.5*(y_new-ymin)/ydiff
                cloud.change_grey(grey_scale)
                
                alpha = 1.
                
                alpha = 1. - max( abs(angle - np.pi/4.) - np.pi/8. , 0. )/(np.pi/8.)
                if angle >= np.pi/4.:
                    alpha = 1. - ( angle - np.pi/4.)/(np.pi/4.)
                    alpha = 0.5*(1. + np.cos( (1.-alpha) * np.pi))
                    alpha = alpha**2
                else:
                    alpha = 1. - 0.5*(1. + np.cos( (angle+np.pi/2.) * 4./3.))
                    
                alpha *= 1 - np.cos( (y_new-ymin)/ydiff * np.pi/2. )**2
                if x_new < xmid:
                    alpha *= np.sin( (x_new-xmin)/(xdiff/2.) * np.pi/2. )**2
                
                alpha *= alpha_factor
                cloud.change_alpha(alpha)
            
            cloud.draw(image,x,y)
        
    return image
    
def update_clouds_downdraft(image,x,y,t,dims,clouds,omega=np.pi/3.,startup_time=3.):
    xmin,xmax,xmid,xdiff,ymin,ymax,ymid,ydiff = dims
    
    radius = ymax/2.
    circle_centre_y = ymid
    
    theta = omega*t
    
    alpha = 0.
    alpha_factor = 1.
    if t <= startup_time:
        alpha_factor = 0.
    elif t < 2*startup_time:
        temp = (t - startup_time)/startup_time
        alpha_factor = 1. - 0.5*(1. + np.cos(temp * np.pi))
    
    if alpha_factor != 0.:
        for cloud in clouds:
            xcloud,ycloud = cloud.get_coordinates()
            xcloud_init,ycloud_init = cloud.get_original_coordinates()
            temp = radius**2 - (ycloud_init-circle_centre_y)**2
            if temp >= 0.:
                circle_centre_x = xcloud_init - np.sqrt(temp)
                angle = math.atan2(ycloud_init-circle_centre_y,xcloud_init-circle_centre_x)
                angle = (angle+theta+np.pi)%(np.pi) - np.pi/2.
                
                x_new = circle_centre_x + radius*np.cos(angle)
                y_new = circle_centre_y + radius*np.sin(angle)
                cloud.change_coordinates(x_new,y_new)
            
                grey_scale  = 0.25 + 0.5*(y_new-ymin)/ydiff
                grey_scale = 1 - grey_scale
                cloud.change_grey(grey_scale)
                
                alpha = 1.
                    
                padding = 0.1*xdiff
                if y_new > ymax-padding or y_new < ymin+padding or x_new > xmax-padding or x_new < xmin+padding:
                    alpha = 0.
                    
                if y_new <= ymin + ydiff/3.:
                    alpha *= np.sin( (y_new-ymin)/(ydiff/3.) * np.pi )**2
                else:
                    alpha = 0.
                alpha *= np.cos( 2*(x_new-xmid)/xdiff * np.pi/2. )**2
                    
                alpha *= alpha_factor
                cloud.change_alpha(alpha)
            
            if alpha != 0.:
                cloud.draw(image,x,y)
        
    return image