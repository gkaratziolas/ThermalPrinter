import cv2 as cv
cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_HEIGHT ,384)
cap.set(cv.CAP_PROP_FRAME_WIDTH  ,384)

while True:
    ret, frame = cap.read()
    edges = cv.Canny(frame,100,200)
    (thresh, im_bw) = cv.threshold(edges, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    cv.imshow("frame", edges)
    print(im_bw[0])
    if cv.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
