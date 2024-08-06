
import numpy

try:
    import cv2
except:
    print('ERROR: cv2 not found. Is conda env \"openCV\" activated?')
    exit()

ix,iy=-1,-1
zoomx,zoomy=-1,-1
shiftX,shiftY =0,0
  
# Initiating the webcam the argument is just an integer id for USB camera typically 0,1,2 etc
vid = cv2.VideoCapture(0) 

# Create empty list to story coordinates of all clicks

allClicks = []

# a function to update coordinates on left mouse click
def onMouse(event, x, y, flags, param):
    
    global ix,iy,zoomx,zoomy
    global allClicks
    global shiftX,shiftY

    if event == cv2.EVENT_LBUTTONDOWN:
       ix,iy=x,y
       allClicks.append((ix,iy))

    # if event == cv2.EVENT_RBUTTONDOWN:
    #     zoomx,zoomy=x,y

def crossHair(image, crossx,crossy,frameheight,framewidth,colour):

    #draw cross hair centred on crossx,crossy
    cv2.line(image,(0,crossy),(framewidth,crossy),colour, 1)
    cv2.line(image,(crossx,0),(crossx,frameheight),colour, 1)

def hLine(image,liney,frameheight,framewidth,colour):
    # draw a horizontal line at liney
    cv2.line(image,(0,liney),(framewidth,liney),colour, 1)

def vLine(image,linex,frameheight,framewidth,colour):
    # draw a vertical line at linex
    cv2.line(image,(linex,0),(linex,frameheight),colour, 1)

        
#print some instructions
print('/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/')
print(' SNAP Aligner 1.1                  ')
print('                                   ')
print(' M. Guthrie 23/Jul/2024            ')
print(' (uses openCV https://opencv.org/) ')
print('/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/\n')

print('Instructions:')
print('1. Click in window to draw vertical line')
print('2. After two clicks, average location is shown\n')
print('keyboard actions:')
print('p - print position of last click')
print('c - clear alignment lines')
print('z/x - zoom/unzoom. Use four keys: i,m,j,k to adjust zoom centre')
print('q - quit\n')

#select camera, initiate webcam capture, manage errors
while(True):
    camID = int(input("First enter ID of camera (usually a number like 0,1,2 etc)"))
    vid = cv2.VideoCapture(camID) 
    ret, frame = vid.read()

    if ret:
        break
    else:
        print('try a different number')

# Start capturing frames and show as a video 
scale=100

while(True): 
    ret, frame = vid.read() 
  
    # Getting the width and height of the feed 
    height = int(vid.get(4)) 
    width = int(vid.get(3))

    cenX,cenY = int(height/2)+shiftX,int(width/2)+shiftY
     
    sclHeight = height*(scale/100)
    sclWidth = width*(scale/100)

    minX,maxX = cenX-int(sclHeight/2),cenX+int(sclHeight/2)
    minY,maxY = cenY-int(sclWidth/2),cenY+int(sclWidth/2)
    

    #handle case where zoom region goes off edge of image
    if minX <0:
        #reset to previous centre
        cenX,cenY=cenX_old+11,cenY_old
        minX,maxX = cenX-int(sclHeight/2),cenX+int(sclHeight/2)
        minY,maxY = cenY-int(sclWidth/2),cenY+int(sclWidth/2)
        shiftX = shiftX+11
    if minY <0:
        #reset to previous centre
        cenX,cenY=cenX_old,cenY_old+11
        minX,maxX = cenX-int(sclHeight/2),cenX+int(sclHeight/2)
        minY,maxY = cenY-int(sclWidth/2),cenY+int(sclWidth/2)
        shiftY = shiftY+11
    if maxX > height:
        #reset to previous centre
        cenX,cenY=cenX_old-11,cenY_old
        minX,maxX = cenX-int(sclHeight/2),cenX+int(sclHeight/2)
        minY,maxY = cenY-int(sclWidth/2),cenY+int(sclWidth/2)
        shiftX=shiftX-11
    if maxY > width:
        #reset to previous centre
        cenX,cenY=cenX_old,cenY_old-11
        minX,maxX = cenX-int(sclHeight/2),cenX+int(sclHeight/2)
        minY,maxY = cenY-int(sclWidth/2),cenY+int(sclWidth/2)
        shiftY=shiftY-11

    cropped = frame[minX:maxX, minY:maxY]
    zoomFrame = cv2.resize(cropped, (width,height))

    #horizontal line
    hLine(zoomFrame,int(height/2),height,width,(255,255,255)) 

    #initial crosshair at click location
    vLine(zoomFrame,ix,height,width,(0,0,255))  
    
    if len(allClicks) >= 2:
        #retain previous cross hair
        vLine(zoomFrame,allClicks[-2][0],height,width,(0,0,255))

        #plot cross hair at average of last two clicks
        avgx = int((allClicks[-2][0]+allClicks[-1][0])/2)
        avgy = int((allClicks[-2][1]+allClicks[-1][1])/2)
        vLine(zoomFrame,avgx,height,width,(255,0,0))
    
    # Showing the video 
    cv2.imshow('LIVE', zoomFrame)
    
    #bind function to window to capture mouse click    
    cv2.setMouseCallback('LIVE', onMouse)

    # configure actions on key press
    # q: quit
    # c: print current coordinates
    k = cv2.waitKey(20) & 0xFF
    if k == ord('q'):
        break
    elif k == ord('p'):
        try:
            print(ix,iy)
        except:
            print("cursor coordinates absent")
    elif k == ord('c'):
            ix,iy=-1,-1
            allClicks = []
    elif k == ord('z'):
        scale -= 5
        # print(f"zoom centre: {cenX},{cenY}")
        # print(f"xlims: {minX},{maxX}")
        # print(f"ylims: {minY},{maxY}")
        # print(f"image size: {maxX-minX}x{maxY-minY}")
        if scale < 5:
            print('max Zoom reached')
            scale = 5
        # else:
        #     print(f'cropping to {100*scale/100:.0f}%')
    elif k == ord('x'):
        scale += 5

        if scale > 95:
            print('max unzoom')
            scale = 95
        # else:
        #     print(f'cropping to {100*scale/100:.0f}%')
    elif k == ord('j'):
        shiftY -= 10
        # store values in case need to revert
        cenX_old,cenY_old=cenX,cenY
    elif k == ord('k'):
        shiftY += 10
        cenX_old,cenY_old=cenX,cenY
    elif k == ord('i'):
        shiftX -= 10
        cenX_old,cenY_old=cenX,cenY
    elif k == ord('m'):
        shiftX += 10
        cenX_old,cenY_old=cenX,cenY

            
# At last release the camera 
vid.release() 
cv2.destroyAllWindows() 