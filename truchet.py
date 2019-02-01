import ThermalPrinter
import Bitmap
import random
import math

kTileSize = 48
kWidth    = 384
kHeight   = 384

kBlack = 0
kWhite = 1


def blank_canvas():
    canvas = []
    for i in range(0, kHeight):
        canvas.append([1]*kWidth)
    return canvas

def draw_dot(canvas, x, y, colour=kBlack):
    if x < kWidth and x >= 0:
        if y < kHeight and y >= 0:
            canvas[y][x] = colour

def draw_line(canvas, x0, y0, x1, y1, colour=kBlack):
    dx = x1-x0
    dy = y1-y0
    if math.fabs(dx) >= math.fabs(dy): # iterate across x
        for x in range(x0, x1, int(math.fabs(x1-x0)/(x1-x0))):
            y = int(y0 + (x-x0)*dy/dx + 0.5)
            draw_dot(canvas, x, y)
    else: # iterate across y
        for y in range(y0, y1, int(math.fabs(y1-y0)/(y1-y0))):
            x = int(x0 + (y-y0)*dx/dy + 0.5)
            draw_dot(canvas, x, y)

#def draw_line(canvas, x0, y0, x1, y1, thickness=1, colour=kBlack)
#    for x in range(x0-thickness, x0+thickness):
#        draw_thin_line(canvas, x, y0, )

def draw_circle(canvas, cx, cy, r, colour=kBlack):
    for i in range(1,1001):
        theta = 1000*2*math.pi/i
        x = cx + r*math.cos(theta)
        y = cy + r*math.sin(theta)
        draw_dot(canvas, int(x+0.5), int(y+0.5), colour)

def img_to_bytes(img):
    val = ""
    for row in img:
        row = [str(r) for r in row]
        row = "".join(row)
        val += row

    bts = int(val, 2).to_bytes(len(img[0])*(len(img))//8, "big")
    return bts

def print_work(canvas, title):
    data = img_to_bytes(canvas)
    P = ThermalPrinter.ThermalPrinter("/dev/ttyUSB0")
    B = Bitmap.Bitmap()
    B.image_data = data
    B.height = len(canvas)
    B.width_bytes = len(canvas[0])//8

    P.print_bitmap(B)
    P.feed(1)
    P.send_bytes(title)
    P.feed(3)

def draw_square_tile(tx, ty, canvas):
    for x in range((tx)*kTileSize, (tx+1)*kTileSize):
        for y in range((ty)*kTileSize, (ty+1)*kTileSize):
            canvas[y][x] = 0

def draw_truchet_tile(tx, ty, tri, canvas):
    if tri == 0 or tri == 1:
        tri_width = kTileSize
        diff      = -1
    else:
        tri_width = 1
        diff      = 1
    for x in range((tx)*kTileSize, (tx+1)*kTileSize):
        for y in range((ty)*kTileSize, (ty+1)*kTileSize):
            if tri == 1 or tri == 3:
                if y - (ty)*kTileSize < tri_width:
                    canvas[y][x] = 0
                else:
                    canvas[y][x] = 1
            else:
                if y - (ty)*kTileSize < tri_width - 1:
                    canvas[y][x] = 1
                else:
                    canvas[y][x] = 0

        tri_width += diff  

def full_truchet():
    canvas = blank_canvas()
    for x in range(0, kWidth//kTileSize):
        for y in range(0, kHeight//kTileSize):
            t = random.randint(0, 3)
            draw_truchet_tile(x,y,t, canvas)
    print_work(canvas, "Truchet ({}) - 2018".format(kTileSize))

def mess_of_lines(n):
    canvas = blank_canvas()
    x0, y0 = 0,0
    for i in range(n):
        x1 = random.randint(0, kWidth-1)
        y1 = random.randint(0, kHeight-1)
        draw_line(canvas, x0, y0, x1, y1)
        x0, y0 = x1, y1
    print_work(canvas, "mess of lines lines ({}) - 2018".format(n))

def star(p, r, cx, cy):
    canvas = blank_canvas()
    for i in range(p):
        theta = 2*math.pi*(i/p)
        x = int(r*math.cos(theta) + cx)
        y = int(r*math.sin(theta) + cy)
        draw_line(canvas, cx, cy, x, y)
    print_work(canvas, "Star ({}) - 2018".format(p))

def star2(p, r, cx, cy):
    canvas = blank_canvas()
    for i in range(p):
        theta = 2*math.pi*(i/p)
        x = int(r*math.cos(theta) + cx)
        y = int(r*math.sin(theta) + cy)
        draw_line(canvas, cx, cy, x, y)

        theta1 = 2*math.pi*((i-1)/p)
        x1 = int(r*math.cos(theta1) + x)
        y1 = int(r*math.sin(theta1) + y)
        draw_line(canvas, x, y, x1, y1)

        theta2 = 2*math.pi*((i+1)/p)
        x2 = int(r*math.cos(theta2) + x)
        y2 = int(r*math.sin(theta2) + y)
        draw_line(canvas, x, y, x2, y2)
    print_work(canvas, "Star2 ({}) - 2018".format(p))

def gradient():
    canvas = blank_canvas()
    for y in range(kHeight):
        for x in range(kHeight):
            a = random.uniform(0,1)
            if x/kWidth < a:
                canvas[y][x] = kBlack
    print_work(canvas, "Random Dither - 2018")

def dithered_circle(canvas, r, cx, cy):
    for y in range(kHeight):
        for x in range(kWidth):
            a = random.uniform(0,1)
            if math.sqrt((x-cx)**2 + (y-cy)**2) <= r:
                if ((x-cx)+r)/(2*r) <= a:
                    canvas[y][x] = kBlack

def gradient2(r):
    cx = kWidth//2
    cy = kHeight//2
    canvas = blank_canvas()
    for y in range(kHeight):
        for x in range(kWidth):
            a = random.uniform(0,1)

            if math.sqrt((x-cx)**2 + (y-cy)**2) < r:
                if x/kWidth < a:
                    canvas[y][x] = kBlack
            else:
                if (x/kWidth) > a:
                    canvas[y][x] = kBlack

    print_work(canvas, "Circular Dither ({}) - 2018".format(r))

def worm(n):
    canvas = blank_canvas()
    x, y = kWidth//2, kHeight//2
    for i in range(0, n):
        x += random.randint(-1,1)
        y += random.randint(-1,1)
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > kWidth-1:
            x = kWidth-1
        if y > kHeight-1:
            y = kHeight-1
        canvas[y][x] = 0

    print_work(canvas, "Worm {} - 2018".format(n))

def circles(canvas, n, r0, d):
    cx, cy = kWidth//2, kHeight//2
    r = r0
    a = 1
    for i in range(0, n):
        draw_circle(canvas, cx, cy, r)
        cx = cx + a * d
        r  = r  + d
        a = -1 * a

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def norm_exp(x, a=1):
    return (math.e**(a*x) - 1)/(math.e**a - 1)

def spheres(max_r, min_r, n):
    P = ThermalPrinter.ThermalPrinter("/dev/ttyUSB0")
    B = Bitmap.Bitmap()
    B.height = kHeight
    B.width_bytes = kWidth//8
    step = (max_r - min_r)//n
    radii = [max_r]
    while max_r - step > min_r:
        max_r -= step
        radii.append(max_r)
        radii.insert(0, max_r)
    canvas = blank_canvas()
    cx, cy = kWidth//2, kHeight//2
    for r in radii:
        for x in range(kWidth):
            for y in range(kHeight):
                a = random.uniform(0,1)
                if math.sqrt((x-cx)**2 + (y-cy)**2) < r:
                    D = 0.5 + ( math.asin( (x-cx)/math.sqrt(r**2 - (y-cy)**2) ) ) / math.pi
                    a = random.uniform(0,1)
                    a = norm_exp(a,-1)
                    #a = sigmoid(a)
                    if a >= D:
                        canvas[y][x] = kBlack
                    else:
                        canvas[y][x] = kWhite
                else:
                    if (x/kWidth) > a:
                        canvas[y][x] = kBlack
                    else:
                        canvas[y][x] = kWhite
        data = img_to_bytes(canvas)
        B.image_data = data
        P.print_bitmap(B)
    P.feed(1)
    P.send_bytes("spheres - chog 2018")
    P.feed(3)

def etch(canvas, n, longest=100, shortest=10):
    x0, y0 = random.randint(0, kWidth), random.randint(0, kHeight)
    previous_direction = 0
    for i in range(0, n):
        if previous_direction == 0 or previous_direction == 1:
            directions = [2,3]
        else:
            directions = [0,1]

        direction = directions[random.randint(0,1)]

        length = random.randint(shortest, longest)
        if direction == 0 or direction == 1:
            if x0 == 0:
                x1 = length
            elif x0 == kWidth-1:
                x1 = kWidth-length
            else:
                x1 = x0 + length*[-1, 1][random.randint(0,1)]
            y1 = y0
            previous_direction = direction
        else:
            if y0 == 0:
                y1 = length
            elif y0 == kHeight-1:
                y1 = kHeight-length
            else:
                y1 = y0 + length*[-1, 1][random.randint(0,1)]
            x1 = x0
            previous_direction = direction

        if x1 >= kWidth:
            x1 = kWidth-1
        if x1 < 0:
            x1 = 0
        if y1 >= kHeight:
            y1 = kHeight - 1
        if y1 < 0:
            y1 = 0
        draw_line(canvas,x0,y0,x1,y1)
        x0, y0 = x1, y1

def sphere(r):
    canvas = blank_canvas()
    cx, cy = kWidth//2, kHeight//2
    for x in range(kWidth):
        for y in range(kHeight):
            a = random.uniform(0,1)
            if math.sqrt((x-cx)**2 + (y-cy)**2) < r:
                D = 0.5 + ( math.asin( (x-cx)/math.sqrt(r**2 - (y-cy)**2) ) ) / math.pi
                a = random.uniform(0,1)
                a = norm_exp(a,-1)
                #a = sigmoid(a)
                if a >= D:
                    canvas[y][x] = kBlack
                else:
                    canvas[y][x] = kWhite
            else:
                if (x/kWidth) > a:
                    canvas[y][x] = kBlack

    data = img_to_bytes(canvas)
    P = ThermalPrinter.ThermalPrinter("/dev/ttyUSB0")
    B = Bitmap.Bitmap()
    B.image_data = data
    B.height = kHeight
    B.width_bytes = kWidth//8

    P.print_bitmap(B)
    canvas.reverse()
    P.image_data = img_to_bytes(canvas)
    P.print_bitmap(B)
    P.feed(1)
    P.send_bytes("title1")
    P.feed(3)
    #print_work(canvas, "Spherical Dither ({}) - 2018".format(r))

def bw_image(canvas, threshold=1, invert=False):
    for y in range(len(canvas)):
        for x in range(len(canvas[0])):
            if canvas[y][x] > threshold:
                if not invert:
                    canvas[y][x] = kBlack
                else:
                    canvas[y][x] = kWhite
            else:
                if not invert:
                    canvas[y][x] = kWhite
                else:
                    canvas[y][x] = kBlack                

def nothing(x):
    pass

def cam_print():
    import cv2 as cv
    P = ThermalPrinter.ThermalPrinter("/dev/ttyUSB0")
    B = Bitmap.Bitmap()
    run = False
    cap = cv.VideoCapture(1)
    cv.namedWindow('image')
    cv.createTrackbar('A','image',0,255,nothing)
    cv.createTrackbar('B','image',0,255,nothing)
    canvas = []

    while True:
        ret, frame = cap.read()
        frame = frame[0:kWidth, 0:kHeight]

        a = cv.getTrackbarPos('A','image')
        b = cv.getTrackbarPos('B','image')
        edges = cv.Canny(frame,a,b)
        cv.imshow("image", edges)

        if run:
            canvas = [edges[100]]
            bw_image(canvas, invert=False)
            data = img_to_bytes(canvas)
            B.image_data = data
            B.height = 1
            B.width_bytes = len(canvas[0])//8
            P.print_bitmap(B)

        key = cv.waitKey(1) & 0xff
        if key == ord('q'):
            break
        elif key == ord('p'):
            if not run:
                canvas = edges.tolist()
                bw_image(canvas, invert=False)
                print_work(canvas, "")
                break
        elif key == ord('r'):
            run = True

    cap.release()
    cv.destroyAllWindows()

def long_truchet():
    canvas = blank_canvas()
    for x in range(0, kWidth//kTileSize):
        for y in range(0, kHeight//kTileSize):
            t = random.randint(0, 3)
            draw_truchet_tile(x,y,t, canvas)

    P = ThermalPrinter.ThermalPrinter("/dev/ttyUSB0")
    B = Bitmap.Bitmap()
    B.width_bytes = len(canvas[0])//8
    B.height = 1

    repeat = 1
    for c in canvas:
        data = img_to_bytes([c])
        repeat = repeat + random.randint(-1,1)
        if repeat < 0:
            repeat = 0
        if repeat > 10:
            repeat = 10
        B.image_data = data
        for i in range(repeat):
            P.print_bitmap(B)
    P.feed(1)
#long_truchet()

def wolfram_pattern():
    import wolfram

    row = [0]*kWidth
    row[kWidth//2] = 1
    rule = 30

    P = ThermalPrinter.ThermalPrinter("/dev/ttyUSB0")
    B = Bitmap.Bitmap()
    B.width_bytes = len(row)//8
    B.height = 1

    while 1:
        data = img_to_bytes([row])
        P.print_bitmap(B)
        next_row(row, rule, wrap=True)
        
wolfram_pattern()

#cam_print()

#if __name__ == "__main__":
#    canvas = blank_canvas()
#    etch(canvas, 300)
#    for i in range(0, 3):
#        dithered_circle(canvas, random.randint(10,100), random.randint(0, kHeight), random.randint(0, kWidth))
#    print_work(canvas, "lines - 2018")

    #spheres(150, 50, 3)
    #sphere(150)
    #gradient2(150)
    #star2(7, 150, kHeight//2, kWidth//2)
#full_truchet()
    #worm(100000)
