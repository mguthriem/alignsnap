
import numpy

try:
    import cv2
except:
    print('ERROR: cv2 not found. Is conda env \"openCV\" activated?')
    exit()

ix,iy=-1,-1
  
# Initiating the webcam the argument is just an integer id for USB camera typically 0,1,2 etc
vid = cv2.VideoCapture(0) 

# Create empty list to story coordinates of all clicks

allClicks = []

# a function to update coordinates on left mouse click
def onMouse(event, x, y, flags, param):
    
    global ix,iy
    global allClicks

    if event == cv2.EVENT_LBUTTONDOWN:
       ix,iy=x,y
       allClicks.append((ix,iy))

def crossHair(crossx,crossy,frameheight,framewidth,colour):

    #draw cross hair centred on crossx,crossy
    cv2.line(frame,(0,crossy),(framewidth,crossy),colour, 1)
    cv2.line(frame,(crossx,0),(crossx,frameheight),colour, 1)

def hLine(liney,frameheight,framewidth,colour):
    # draw a horizontal line at liney
    cv2.line(frame,(0,liney),(framewidth,liney),colour, 1)

def vLine(linex,frameheight,framewidth,colour):
    # draw a vertical line at linex
    cv2.line(frame,(linex,0),(linex,frameheight),colour, 1)

        
#print some instructions
print('/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/')
print(' SNAP Aligner 1.0                  ')
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
while(True): 
    ret, frame = vid.read() 
  
    # Getting the width and height of the feed 
    height = int(vid.get(4)) 
    width = int(vid.get(3))

    #horizontal line
    hLine(int(height/2),height,width,(255,255,255)) 

    #initial crosshair at click location
    vLine(ix,height,width,(0,0,255))  
    
    if len(allClicks) >= 2:
        #retain previous cross hair
        vLine(allClicks[-2][0],height,width,(0,0,255))

        #plot cross hair at average of last two clicks
        avgx = int((allClicks[-2][0]+allClicks[-1][0])/2)
        avgy = int((allClicks[-2][1]+allClicks[-1][1])/2)
        vLine(avgx,height,width,(255,0,0))
    
    # Showing the video 
    cv2.imshow('LIVE', frame)

    
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
            
# At last release the camera 
vid.release() 
cv2.destroyAllWindows() 