import numpy as np
from update_arrows import *
from update_background import *
from update_clouds import *
from update_rain import *

def make_image(x_res, y_res, t, clouds, rain, version=""):
    #Set up coordinates
    xmin = 0.
    xmax = 1.*x_res/y_res
    xmid = (xmax+xmin)/2.
    xdiff = xmax - xmin
    ymin = 0.
    ymax = 1.
    ymid = (ymax+ymin)/2.
    ydiff = ymax - ymin
    dims = [xmin,xmax,xmid,xdiff,ymin,ymax,ymid,ydiff]
    border = 0.
    thickness = 0.1
    
    x = np.linspace(xmin-2*border, xmax+2*border, x_res)
    y = np.linspace(ymax+border, ymin-border, y_res)
    
    #Pre-defined colours for different regions in image
    color = [0.,0.,1.,1.]
    border_color = [1.,1.,1.,1.]
    background_color = [1.,1.,1.,1.]
    fluid_color = [1.,1.,1.,0.]
    arrow_color = [1.,0.,0.,1.]
    moisture_color = [0.7,0.7,0.7,0.7]
    
    if version == "updraft":
        fluid_color = [1.,0.,0.,1.]
        arrow_color = [1.,0.,0.,1.]
    elif version == "downdraft":
        fluid_color = [0.,0.,1.,1.]
        arrow_color = [0.,0.,1.,1.]
    
    image = np.zeros((len(y),len(x),4))
    image[:,:] = background_color

    #If first timestep, generate and store cloud pattern.
    if clouds == []:
        clouds = generate_clouds(x,y,dims)
        print "{} cloud particles generated.".format(len(clouds))
        
    #If first timestep, generate and store rain.
    if rain == []:
        rain = generate_rain_droplets(x, y, dims, rain)
        print "{} rain particles generated.".format(len(rain))
    
    #Add layers to image.
    if version == "downdraft":
        t = t - 9.
        image = update_background(image, x, y, t, dims, color=fluid_color)
        image = update_rain(image, x, y, t, dims,rain)
        image = update_arrows(image, x, y, t, dims, color=arrow_color)
        image = update_clouds_downdraft(image, x, y, t, dims,clouds)
    else:
        image = update_background(image, x, y, t, dims, color=fluid_color)
        image = update_arrows(image, x, y, t, dims, color=arrow_color)
        image = update_clouds_updraft(image, x, y, t, dims, clouds)
    
    return image, clouds, rain