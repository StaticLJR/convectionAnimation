import numpy as np
import math

def update_background(image,x,y,t,dims,omega=np.pi/3.,color=[1.,0.,0.,1.],startup_time=3.):
    xmin,xmax,xmid,xdiff,ymin,ymax,ymid,ydiff = dims
    
    radius = ymax/2.
    circle_centre_x = xmax - radius - radius/2.
    # circle_centre_x = xmin
    circle_centre_y = ymid
    
    if t <= 0.:
        return image
    #Start up phase.
    elif t <= startup_time:
        #Angle up to which contents are visible.
        theta = omega*t - np.pi/2
        gradient = np.tan(theta)
        
        for j in xrange(len(y)):
            # x-perturbation of circle edge from circle centre.
            x_temp = np.sqrt(radius**2 - (y[j]-circle_centre_y)**2)
            # x-coord of circle edge
            x_start = circle_centre_x + x_temp
            # x-index of circle edge
            x_starti = (np.abs(x-x_start)).argmin()
            
            if np.sqrt( (x[x_starti]-circle_centre_x)**2 + (y[j]-circle_centre_y)**2 ) >= radius:
                if (y[j]-circle_centre_y) < gradient*(x[x_starti]-circle_centre_x):
                    image[j][x_starti] = color
            for i in xrange(x_starti+1,len(x)):
                if (y[j]-circle_centre_y) < gradient*(x[i]-circle_centre_x):
                    image[j][i] = color
    #Wave phase.
    # elif t > 2*startup_time + 1./omega/2.:
    # elif t > 2*startup_time:
    else:
        time_period = 0.6
        time_period = 1./omega/2.
        amplitude = radius/30.
        number_of_waves = 20.
    
        # radius -= amplitude
        for j in xrange(len(y)):
            if (radius-amplitude)**2 > (y[j]-circle_centre_y)**2:
                # x-perturbation of circle edge (plus wave attribute) from circle centre.
                x_temp = np.sqrt((radius-amplitude)**2 - (y[j]-circle_centre_y)**2)
                # x-coord of circle edge
                x_start = circle_centre_x + x_temp
                # x-index of circle edge
                x_starti = (np.abs(x-x_start)).argmin()
            else:
                x_starti = (np.abs(x-circle_centre_x)).argmin()
            
            for i in xrange(x_starti,len(x)):
                #Find angle relative to circle circle centre and calculate what amplitude should be at angle.
                theta = math.atan2(y[j]-circle_centre_y,x[i]-circle_centre_x)
                wave_amplitude = amplitude*np.sin(number_of_waves*theta + np.pi/2.)*np.sin((t-startup_time)/time_period)
                wave_amplitude *= np.sin(theta + np.pi/2.)
                if np.sqrt( (x[i]-circle_centre_x)**2 + (y[j]-circle_centre_y)**2 ) >= radius + wave_amplitude:
                    image[j][i] = color
                    
    return image