import numpy as np
from PIL import Image

imgL_location = ".\Vintage-perfect\imLeft.png"
imgR_location = ".\Vintage-perfect\imRight.png"
m = 6 #each matching window will be mxm pixels, chosen by me 
half_m = int(m/2)
ndisp = 30 #the bound on the disparity value, provided already

#Loads the images into PILLOW objects, then convert to numpy arrays of intensity values, return arrays and the width and height 
def load_information(imgL, imgR):
    imgL = Image.open(imgL)
    imgR = Image.open(imgR)
    imgL = imgL.convert('L')
    imgR = imgR.convert('L') #convert images to greyscale because colour is not important, only care about intensity (luminescence)
    
    imgL, imgR = downSize_Images(imgL, imgR)
    
    left_I = np.asarray(imgL)
    right_I = np.asarray(imgR) #convert images to numpy arrays of intensity values for later SSD calculations    
    (width, height) = imgL.size   
    return (left_I, right_I, width, height)
        

#This function computes the SSD for a particular window at a particular disparity value 
def get_SSD(left_I, right_I, row, col, current_disparity):
    SSD = 0 
    #u and v are the starting x and y coordinates for this specific window
    for v in range (-half_m, half_m):
        for u in range(-half_m, half_m):
            #calculate the intensity difference between left and right pixels, accounting for supposed disparity
            I_difference = int(left_I[row+v, col+u]) - int(right_I[row+v, col+u - current_disparity]) 
            SSD += I_difference * I_difference
    return SSD

def get_DisparityMap(left_I, right_I, width, height):
    disparityMap = np.zeros((height, width)) #create an empty disparity map to be populated     

    for row in range(half_m, height - half_m): #start 1 row away from the edge of the picture
        
        for col in range (half_m, width - half_m): #start 1 column away from the edge of the picture
            print("Currently on row: ", row, " column: ", col)        

            min_SSD = 1000000 #choosing 1 million since I just need a very large number to start off
            actual_disparity = 0 #default starting value for the disparity estimate for this window 
            
            for current_disparity in range(ndisp - 1): #iterate through the possible disparity range values
                #print("Now testing disparity: ", current_disparity)
                calculated_SSD = get_SSD(left_I, right_I, row, col, current_disparity)
                if min_SSD > calculated_SSD:
                    min_SSD = calculated_SSD
                    actual_disparity = current_disparity #the best disparity estimate is associated with the minimum SSD value, they go hand in hand

            disparityMap[row, col] = actual_disparity #populate the disparity map with the estimated value for this particular pixel
    return disparityMap

#Used to increase processing speed if needed 
def downSize_Images(imgL, imgR):
    
    basewidth = 364
    wpercent = (basewidth/float(imgL.size[0]))
    hsize = int((float(imgL.size[1])*float(wpercent)))
    imgL = imgL.resize((basewidth,hsize), Image.ANTIALIAS)
    imgR = imgR.resize((basewidth,hsize), Image.ANTIALIAS)

    return imgL, imgR
    
def main():
    left_I, right_I, width, height = load_information(imgL_location, imgR_location)
    disparityImage = Image.fromarray(get_DisparityMap(left_I, right_I, width, height))
    disparityImage.show()
    

main()









            
