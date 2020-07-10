import numpy as np

def combine_colors(bottom,top):
    new = [0.,0.,0.,0.]
    new[3] = 1. - (1.-top[3])*(1.-bottom[3])
    if new[3] != 0.:
        for k in xrange(3):
            new[k] = top[k]*top[3]/new[3] + bottom[k]*bottom[3]*(1.-top[3])/new[3]
    return new

def find_line(p1,p2,max_grad=1e+10):
    if p1[0] != p2[0]:
        gradient = (p2[1] - p1[1])/(p2[0] - p1[0])
    else:
        gradient = max_grad
    intercept = p1[1] - gradient*p1[0]
    return gradient,intercept

def curved_rectangle(image,x,y,length,height,xcentre,ycentre,color,theta=np.pi/4.):
    curve_radius = min(length,height)/2.
    
    #Calculate corners of rectangular region based on central point, width and height.
    corner1 = [xcentre + height/2.*np.sin(theta) + (length/2.-curve_radius)*np.cos(theta), ycentre - height/2.*np.cos(theta) + (length/2.-curve_radius)*np.sin(theta)]
    corner2 = [xcentre - height/2.*np.sin(theta) + (length/2.-curve_radius)*np.cos(theta), ycentre + height/2.*np.cos(theta) + (length/2.-curve_radius)*np.sin(theta)]
    corner3 = [xcentre + height/2.*np.sin(theta) - (length/2.-curve_radius)*np.cos(theta), ycentre - height/2.*np.cos(theta) - (length/2.-curve_radius)*np.sin(theta)]
    corner4 = [xcentre - height/2.*np.sin(theta) - (length/2.-curve_radius)*np.cos(theta), ycentre + height/2.*np.cos(theta) - (length/2.-curve_radius)*np.sin(theta)]
    
    #Find equations for edges of rectangles.
    m1,c1 = find_line(corner1,corner2)
    m2,c2 = find_line(corner3,corner4)
    m3,c3 = find_line(corner1,corner3)
    m4,c4 = find_line(corner2,corner4)
    
    #Calculate relevant region of image to scan and print shape to save computation time.
    x_starti = (np.abs(x-np.min([corner1[0],corner2[0],corner3[0],corner4[0]])+curve_radius)).argmin()
    x_endi = (np.abs(x-np.max([corner1[0],corner2[0],corner3[0],corner4[0]])-curve_radius)).argmin()
    y_endj = (np.abs(y-np.min([corner1[1],corner2[1],corner3[1],corner4[1]])+curve_radius)).argmin()
    y_startj = (np.abs(y-np.max([corner1[1],corner2[1],corner3[1],corner4[1]])-curve_radius)).argmin()
    
    #Centres for curve on one side of rectangle.
    x1 = xcentre + (length/2.-curve_radius)*np.cos(theta)
    y1 = ycentre + (length/2.-curve_radius)*np.sin(theta)
    #Centres for curve on other side of rectangle.
    x2 = xcentre - (length/2.-curve_radius)*np.cos(theta)
    y2 = ycentre - (length/2.-curve_radius)*np.sin(theta)
    for j in xrange(y_startj,y_endj):
        for i in xrange(x_starti,x_endi):
            if (y[j] - (m1*x[i]+c1))*(y[j] - (m2*x[i]+c2)) <= 0:
                if (y[j] - (m3*x[i]+c3))*(y[j] - (m4*x[i]+c4)) <= 0:
                    image[j][i] = combine_colors([1.,1.,1.,1.],color)
            if np.sqrt((x[i]-x1)**2 + (y[j]-y1)**2) <= curve_radius or np.sqrt((x[i]-x2)**2 + (y[j]-y2)**2) <= curve_radius:
                image[j][i] = combine_colors([1.,1.,1.,1.],color)
    
    return image

def arrow(image,x,y,centre,length,thickness,color,theta=0.):
    curve_radius = thickness/2.

    #Base of arrow.
    image = curved_rectangle(image,x,y,length,thickness,centre[0],centre[1],color,theta=theta)
    
    #End tip of arrow.
    tip_length = length/2.4
    tip1_theta = theta - np.pi/4.
    tip2_theta = theta + np.pi/4.
    tip1_centre = [centre[0] + (length/2.-curve_radius)*np.cos(theta) - tip_length/2.*np.cos(tip1_theta), centre[1] + (length/2.-curve_radius)*np.sin(theta) - tip_length/2.*np.sin(tip1_theta)]
    tip2_centre = [centre[0] + (length/2.-curve_radius)*np.cos(theta) - tip_length/2.*np.cos(tip2_theta), centre[1] + (length/2.-curve_radius)*np.sin(theta) - tip_length/2.*np.sin(tip2_theta)]
    
    image = curved_rectangle(image,x,y,tip_length,thickness,tip1_centre[0],tip1_centre[1],color,theta=tip1_theta)
    image = curved_rectangle(image,x,y,tip_length,thickness,tip2_centre[0],tip2_centre[1],color,theta=tip2_theta)
    return image
    
def update_arrows(image,x,y,t,dims,omega=np.pi/3.,color=[1.,0.,0.,1.],startup_time=3.):
    xmin,xmax,xmid,xdiff,ymin,ymax,ymid,ydiff = dims
    
    radius = ymax/2.
    arrow_path_radius = 0.8*radius
    arrow_thickness = 0.015
    arrow_length = 5.5*arrow_thickness
    circle_centre_x = xmax - radius - radius/2.
    circle_centre_y = ymid
    
    if t <= 0.:
        return image
    #Start up phase.
    elif t < startup_time:
        #Angle of 4 arrows during startup phase.
        theta1 = omega*t + np.pi/2
        theta2 = omega*t + np.pi/4.
        theta3 = omega*t 
        theta4 = omega*t - np.pi/4. + 2*np.pi
    else:
        #Angle of arrows for infinite loop.
        theta1 = (omega*t + np.pi/2)%np.pi + np.pi/2
        theta2 = (omega*t + np.pi/4.)%np.pi + np.pi/2
        theta3 = (omega*t)%np.pi + np.pi/2
        theta4 = (omega*t - np.pi/4. + 2*np.pi)%np.pi + np.pi/2
        
    #Draw arrows.
    arrow_centre = [circle_centre_x-arrow_path_radius*np.cos(theta1), circle_centre_y-arrow_path_radius*np.sin(theta1)]
    image = arrow(image,x,y,arrow_centre,arrow_length,arrow_thickness,[color[0],color[1],color[2],max(0,np.sin(theta1-np.pi/2.))*color[3]],theta=theta1-np.pi/2.)
    
    arrow_centre = [circle_centre_x-arrow_path_radius*np.cos(theta2), circle_centre_y-arrow_path_radius*np.sin(theta2)]
    image = arrow(image,x,y,arrow_centre,arrow_length,arrow_thickness,[color[0],color[1],color[2],max(0,np.sin(theta2-np.pi/2.))*color[3]],theta=theta2-np.pi/2.)
    
    arrow_centre = [circle_centre_x-arrow_path_radius*np.cos(theta3), circle_centre_y-arrow_path_radius*np.sin(theta3)]
    image = arrow(image,x,y,arrow_centre,arrow_length,arrow_thickness,[color[0],color[1],color[2],max(0,np.sin(theta3-np.pi/2.))*color[3]],theta=theta3-np.pi/2.)
    
    arrow_centre = [circle_centre_x-arrow_path_radius*np.cos(theta4), circle_centre_y-arrow_path_radius*np.sin(theta4)]
    image = arrow(image,x,y,arrow_centre,arrow_length,arrow_thickness,[color[0],color[1],color[2],max(0,np.sin(theta4-np.pi/2.))*color[3]],theta=theta4-np.pi/2.)
              
    return image 