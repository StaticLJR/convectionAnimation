import sys
import os
import numpy as np
import random as rn
import scipy.misc

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "objects"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "utilities"))
from update_image import *
from utilities import *

''''''''''''''''''''''''''''''''''''''''''
''' IMAGEMAGICK MUST BE INSTALLED      '''
''''''''''''''''''''''''''''''''''''''''''
##########################################
#Generates animation of convective
#circulations in the atmosphere.
#Requires imagemagick (imagemagick.org)
#to join images together and 
#to generate gif animations.
##########################################


''''''''''''''''''''''''''''''''''''''''''
'''         USER SETTINGS              '''
''''''''''''''''''''''''''''''''''''''''''
make_gif = True            #Stich images into gif (REQUIRES IMAGEMAGICK)
resolution_x = 800         #Horizontal resolution of image
resolution_y = 400         #Vertical resolution of image
seed = 111222333           #Seed for random distribution of cloud and rain
system = "windows"         #Operating system needed for imagemagick commands
                           #Optimised for windows
output_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "output")



def main(resolution_x, resolution_y, seed, output_folder, make_gif, system="windows"):
    ''''''''''''''''''''''''''''''''''''''''''
    if make_gif:
        print 50*"="
        print "\n\nWARNING: You have chosen to generate a gif animation. You must have imagemagick installed or this will not work.\n\n"
        print 50*"="

    #Imagemagick commands
    if system == "windows":
        convert = "magick convert"
    else:
        convert = "convert"
    
    #Seed used to randomise locations of clouds and rain droplets.
    rn.seed(seed)

    #Storage arrays for cloud regions and rain droplets.
    clouds = []
    rain = []

    ''''''''''''''''''''''''''''''''''''''''''
    ''' CONSTRUCT FIRST PART OF ANIMATION  '''
    ''''''''''''''''''''''''''''''''''''''''''
    image_count = 0
    t = np.linspace(0.,6.,80)[:-1]
    console = "{0} -delay 5 -dispose previous ".format(convert)

    for n in xrange(len(t)):
        image_count += 1
        sys.stdout.write("\rStage 1 of 3, Image {0} of {1}__________".format(n+1, len(t)))
        sys.stdout.flush()
        
        #Generate right half of image which represents hot rising air
        image, clouds, rain = make_image(resolution_x/2, resolution_y, t[n], clouds, rain, version="updraft")    
        directory1 = os.path.join(output_folder, 'image_{}.png'.format(image_count))
        scipy.misc.toimage(image, cmin=0, cmax=1).save(directory1)
        
        os.system("{0} {1} -flop {2}".format(convert, directory1, directory1))
        os.system("{0} {1} -flip {2}".format(convert, directory1, directory1))
        
        #Generate left half of image which represents cold descending air
        image, clouds, rain = make_image(resolution_x/2, resolution_y, t[n], clouds, rain, version="downdraft")    
        directory2 = os.path.join(output_folder, 'image_temp.png'.format(image_count))
        scipy.misc.toimage(image, cmin=0, cmax=1).save(directory2)
        
        append_hor(directory1, directory2, directory1, output_folder, convert=convert)
        os.system("{0} {1} -flop {2}".format(convert, directory1, directory1))
        os.system("{0} {1} -flip {2}".format(convert, directory1, directory1))
        console += directory1 + " "
        
    if make_gif:
        gif1 = os.path.join(output_folder, "animation_part1.gif")
        console += "-loop 1 {0}".format( gif1 )
        os.system(console)



    ''''''''''''''''''''''''''''''''''''''''''
    ''' CONSTRUCT SECOND PART OF ANIMATION '''
    ''''''''''''''''''''''''''''''''''''''''''
    console = "{0} -delay 5 -dispose previous ".format(convert)
    t = np.linspace(6.,12.,80)[:-1]

    for n in xrange(len(t)):
        image_count += 1
        sys.stdout.write("\rStage 2 of 3, Image {0} of {1}__________".format(n+1, len(t)))
        sys.stdout.flush()
        
        #Generate right half of image which represents hot rising air
        image, clouds, rain = make_image(resolution_x/2, resolution_y, t[n], clouds, rain, version="updraft")    
        directory1 = os.path.join(output_folder, 'image_{}.png'.format(image_count))
        scipy.misc.toimage(image, cmin=0, cmax=1).save(directory1)
        
        os.system("{0} {1} -flop {2}".format(convert, directory1, directory1))
        os.system("{0} {1} -flip {2}".format(convert, directory1, directory1))
        
        #Generate left half of image which represents cold descending air
        image, clouds, rain = make_image(resolution_x/2, resolution_y, t[n], clouds, rain, version="downdraft")    
        directory2 = os.path.join(output_folder, 'image_temp.png'.format(image_count))
        scipy.misc.toimage(image, cmin=0, cmax=1).save(directory2)
        
        append_hor(directory1, directory2, directory1, output_folder, convert=convert)
        os.system("{0} {1} -flop {2}".format(convert, directory1, directory1))
        os.system("{0} {1} -flip {2}".format(convert, directory1, directory1))
        
        os.system("{0} {1} -flop {2}".format(convert, directory1, directory2))
        console += directory1 + " "
        
    if make_gif:
        gif2 = os.path.join(output_folder, "animation_part2.gif")
        console += "-loop 1 {0}".format( gif2 )
        os.system(console)



    ''''''''''''''''''''''''''''''''''''''''''
    ''' CONSTRUCT THIRD PART OF ANIMATION  '''
    ''''''''''''''''''''''''''''''''''''''''''
    console = "{0} -delay 5 -dispose previous ".format(convert)
    t = np.linspace(12.,15.,40)[:-1]

    for n in xrange(len(t)):
        image_count += 1
        sys.stdout.write("\rStage 3 of 3, Image {0} of {1}__________".format(n+1, len(t)))
        sys.stdout.flush()
        
        #Generate right half of image which represents hot rising air
        image, clouds, rain = make_image(resolution_x/2, resolution_y, t[n], clouds, rain, version="updraft")    
        directory1 = os.path.join(output_folder, 'image_{}.png'.format(image_count))
        scipy.misc.toimage(image, cmin=0, cmax=1).save(directory1)
        
        #Generate left half of image which represents cold descending air
        image, clouds, rain = make_image(resolution_x/2, resolution_y, t[n], clouds, rain, version="downdraft")    
        directory2 = os.path.join(output_folder, 'image_temp.png'.format(image_count))
        scipy.misc.toimage(image, cmin=0, cmax=1).save(directory2)
        
        os.system("{0} {1} -flop {2}".format(convert, directory2, directory2))
        os.system("{0} {1} -flip {2}".format(convert, directory2, directory2))
        
        append_hor(directory2, directory1, directory1, output_folder, convert=convert)
        console += directory1 + " "

    if make_gif:
        gif3  = os.path.join(output_folder, "animation_part3.gif")
        console += "-loop 0 {0}".format( gif3 )
        os.system(console)




    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    ''' STITCH 3 GIFS TOGETHER TO CREATE FULL ANIMATION SEQUENCE   '''
    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    if make_gif:
        #Make the thired gif repeat 10 times
        gif3 = 10*(" "+gif3)
        console = "{0} -delay 5 -dispose previous {1} {2}{3} -loop 1 {4}".format(convert, gif1, gif2, gif3, os.path.join(output_folder, "animation_total_single.gif"))
        os.system(console)
        console = "{0} -delay 5 -dispose previous {1} {2}{3} -loop 0 {4}".format(convert, gif1, gif2, gif3, os.path.join(output_folder, "animation_total_repeating.gif"))
        os.system(console)





main(resolution_x, resolution_y, seed, output_folder, make_gif)