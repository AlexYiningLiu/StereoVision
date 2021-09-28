import numpy as np
from PIL import Image

imgL_location = ".\Vintage-perfect\imLeft.png"
imgR_location = ".\Vintage-perfect\imRight.png"
m = 6 #each matching window will be (m+1)x(m+1) pixels, chosen by me, m must be an even number 
half_m = int(m/2)
ndisp = 704 #the bound on the disparity value

#Loads the images into PILLOW objects, then convert to numpy arrays of intensity values, return arrays and the width and height 
def load_information(imgL, imgR):
    imgL = Image.open(imgL)
    imgR = Image.open(imgR)
    imgL = imgL.convert('L')
    imgR = imgR.convert('L') #convert images to greyscale because colour is not important, only care about intensity (luminescence)
    
    #imgL, imgR = downSize_Images(imgL, imgR)
    
    left_I = np.asarray(imgL)
    right_I = np.asarray(imgR) #convert images to numpy arrays of intensity values for later SSD calculations    
    (width, height) = imgL.size   
    return (left_I, right_I, width, height)
        


def new_DisparityMap(left_I, right_I, h, w):
    disparityMap = np.zeros((h, w))
    differenceMap = np.zeros((h,w))
    
    for off in range(ndisp-1):
        print("Now calculating for offset: ", off)
        
        for row in range(h):

            for col in range(w):

                differenceMap[row, col] = abs(int(left_I[row, col]) - int(right_I[row, col+off]))
        # compute the integral image
        integralImage = compute_IntegralImage(differenceMap, h, w)
        minCost = 1000000
        for row in range(half_m, h - half_m):

            for col in range(half_m, w - half_m):

                newCost = evalCostWithIntegralImage(integralImage, row, col)
                if minCost > newCost:
                    minCost = newCost
                    disparityMap[row, col] = off
                    
    return disparityMap

def evalCostWithIntegralImage(integralImage, row, col):
    #top left corner (x1,y1) and bottom right corner (x2, y2)
    x1 = col - half_m
    y1 = row - half_m
    x2 = col + half_m
    y2 = row + half_m 

    print (x1, y1, x2, y2)
    newCost = integralImage[y2, x2] - integralImage[y2, x1-1] - integralImage[y1-1, x2] + integralImage[y1-1, x1-1]
    return newCost 
    
                
def compute_IntegralImage(differenceMap, h, w):
    integralImage = np.zeros((h,w))
    integralImage[0,0] = differenceMap[0,0]
    for x in range(1, w):
        
        integralImage[0, x] = integralImage[0, x-1] + differenceMap[0, x]
        
    for y in range(1, h):
        
        s = differenceMap[y, 0]
        integralImage[y, 0] = integralImage[y-1, 0] + s
        
        for col in range(1, w):
            
            s = s + differenceMap[y, col]
            integralImage[y, col] = integralImage[y-1, col] + s

    print("Done integral image")
    return integralImage 
    

    
def main():
    left_I, right_I, width, height = load_information(imgL_location, imgR_location)
    disparityImage = Image.fromarray(new_DisparityMap(left_I, right_I, height, width))
    disparityImage.show()
    

main()









            
