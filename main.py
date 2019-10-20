import pyautogui, time, random, keyboard, pytweening
# Packages needed: pyautogui, keyboard 
# This script is made with https://steamcommunity.com/sharedfiles/filedetails/?id=823274093 in mind.

###################
# Your variables
###################
chanceCleanScreen = 10 # Chance that we'll clean the screen (1,1000)
chanceDragginess = 5 # Chance that we stop dragging the mouse (1,1000)
chanceChangeColor = 10 # Chance that the color will change (1,100)
chanceChangeRotationalSym = 7 # Chance that the rotational symmetry will change (1,100)
chanceMirroring = 7 # Chance that the rotational symmetry will change (1,100)
drawInterval = .3 # Every n seconds a line will be drawn
cleanScreenInterval = 100 # After n drawn lines the screen will be cleaned
minDuration = 200 # No need to change these
maxDuration = 1000 # No need to change these

###################
# Monitor positions
# left, left 4k
###################
# Define our grid (From top left to bottom right)
gridXMinMax = (-6016, -2151)
gridYMinMax = (0, 2159)
# Depending on your screen size you might want to change these offsets
minCurveOffset = 50
maxCurveOffset = 2100

# left, left 4k
posNew = (-2094, 41)
posColors = [
    (-2076, 146), # Pink
    (-2001, 151), # Purple
    (-1972, 203), # Cyan
    (-2010, 258), # Green
    (-2070, 261), # Yellow
    (-2106, 204), # Orange
    (-2041, 202) # Gray
]

posRotSym = [
    (-2126, 372), # No 
    (-2097, 372), # 2-fold
    (-2065, 372), # 3-fold
    (-2015, 372), # 4-fold
    (-1972, 372), # 5-fold
    (-1946, 372) # 6-fold
]
posCenter = (-3964, 1083)
posMirrorCenter = (-2119, 451)
#posSpiralCenter = (-204, 486)

###################
# left, 1080p
###################
# These variables depend on your monitor resolution and position
#posNew = (-175, 34)
#posColors = [
#    (-151, 151), # Pink
#    (-86, 154), # Purple
#    (-63, 208), # Cyan
#    (-85, 267), # Green
#    (-152, 267), # Yellow
#    (-183, 208), # Orange
#    (-118, 208) # Gray
#]
#posRotSym = [
#    (-206, 374), # No 
#    (-176, 376), # 2-fold
#    (-148, 376), # 3-fold
#    (-117, 376), # 4-fold
#    (-60, 376), # 5-fold
#    (-30, 376) # 6-fold
#]
#posMirrorCenter = (-204, 456)
#posSpiralCenter = (-204, 486)
# posCenter = (-1000, 540)


###################
# Make curvey lines 
# thanks to https://github.com/asweigart/pyautogui/issues/80
###################

def getPointOnCurve(x1, y1, x2, y2, n, tween=None, offset=0):
    """Returns the (x, y) tuple of the point that has progressed a proportion
    n along the curve defined by the two x, y coordinates.
    If the movement length for X is great than Y, then Y offset else X
    """
    # for compatibility Backward
    if getPointOnCurve.tween and getPointOnCurve.offset:  # need DEL
        tween = getPointOnCurve.tween                     # need DEL
        offset = getPointOnCurve.offset                   # need DEL

    x = ((x2 - x1) * n) + x1
    y = ((y2 - y1) * n) + y1
    if tween and offset:
        offset = (n - tween(n)) * offset
        if abs(x2 - x1) > abs(y2 - y1):
            y += offset
        else:
            x += offset
    return (x, y)

getPointOnCurve.tween = None
getPointOnCurve.offset = 0

def setCurve(func, tween=None, offset=0):
   func.tween = tween
   func.offset = offset
pyautogui.getPointOnLine = getPointOnCurve # Replacement

# Move to the center of the screen
def returnToCenter():
    pyautogui.moveTo(posCenter[0], posCenter[1])

def clickControllButton(x, y):
    pyautogui.mouseUp()
    pyautogui.moveTo(x, y, tween='linear')
    pyautogui.mouseDown(duration=0.2)
    pyautogui.mouseUp()

def cleanScreen():
    clickControllButton(posNew[0], posNew[1])

def changeColor():
    color = random.choice(posColors)
    clickControllButton(color[0], color[1])

def changeRotationalSym():
    rotSym = random.choices(posRotSym, weights=[40, 5, 5, 20, 20, 20])
    clickControllButton(rotSym[0][0], rotSym[0][1])

def toggleMirroring():
    clickControllButton(posMirrorCenter[0], posMirrorCenter[1])
    
# Tweening functions
tweening = [
    pyautogui.easeInQuad, 
    pyautogui.easeOutQuad,
    pyautogui.easeInOutQuad,
    pyautogui.easeInBounce,
    pyautogui.easeInElastic
]

cleanScreen()
i = 0
while True:
    if (i == cleanScreenInterval): cleanScreen; i = 0
    # If q is pressed we stop the madness
    if keyboard.is_pressed('q'): pyautogui.mouseUp(); break
    # On a pressed r we clean the screen
    if keyboard.is_pressed('r'): cleanScreen(); i = 0
    # Get our random numbers
    random.seed()

    # Get a new color maybe?
    if (random.randint(1,100) <= chanceChangeColor): changeColor()
    # Chance rotational symmetry or mirroring maybe?
    if (random.randint(1,100) <= chanceChangeRotationalSym): changeRotationalSym(); changeColor(); toggleMirroring()
    elif (random.randint(1,100) <= chanceMirroring): toggleMirroring()
    # Clean our screen maybe?
    if (random.randint(1,1000) <= chanceCleanScreen): cleanScreen(); i = 0

    # Get our new position
    randX = random.randint(gridXMinMax[0], gridXMinMax[1])
    randY = random.randint(gridYMinMax[0], gridYMinMax[1])
    randDuration = random.randint(minDuration, maxDuration) / 1000
    # Go to next position
    # Curve and tweening with a random offset
    setCurve(getPointOnCurve, random.choice(tweening), random.randint(minCurveOffset, maxCurveOffset))
    pyautogui.moveTo(randX, randY, randDuration)
    pyautogui.click(clicks=1)
    pyautogui.mouseDown()

    time.sleep(drawInterval)
    # Decide if we want to stop dragging
    if (random.randint(1,1000) <= chanceDragginess): pyautogui.mouseUp()
    i += 1
