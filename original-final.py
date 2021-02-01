import cv2
import numpy as np
import os

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
path = 'Imagesquery'
path2 = 'Testvideos1'
orb = cv2.ORB_create(nfeatures=3000)
images = []
classNames = []
myList = os.listdir(path)
print('Total Classes Detected', len(myList))
for cl in myList:
    imgCur = cv2.imread(f'{path}/{cl}', 0)
    images.append(imgCur)
    classNames.append(imgCur)
print(classNames)

desList = []
keypnts = []
for img in images:
    kp1, des1 = orb.detectAndCompute(img, None)
    desList.append(des1)
    keypnts.append(kp1)

# Import videos
videos = []
classNames2 = []
imgVideo = []
pts = []
HT = []
WT = []
myList2 = os.listdir(path2)
#print("lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll")
print(myList2)
print('Total Classes Detected', len(myList2))
for cl2 in myList2:
    print(cl2)
    myVid = cv2.VideoCapture(f'{path2}/{cl2}')
    success, imgV = myVid.read()
    for cl in images:
        print(cl)
        hT, wT = cl.shape
        HT.append(hT)
        WT.append(wT)
        imgV = cv2.resize(imgV, (wT, hT))
        pts1 = np.float32([[0, 0], [0, hT], [wT, hT], [wT, 0]]).reshape(1, -1, 2)
        pts.append(pts1)
        imgVideo.append(imgV)
    videos.append(myVid)
    classNames2.append(cl2)
print(classNames2)
uy= zip(HT, WT)
xyz=[]
for i,j in uy:
    xyz.append([i,j])

#xyz = list(uy)
#print("fdkjghiuhergbfjkhgkjfhghfjhfjkhskfjhskjfhkafsdkjfhkjdshfshueibf")
print(len(imgVideo[1]))
#print("nnnnnnnnnnnnnnnnnnnnnn ")
print(WT)

detection = False
frameCounter = 0

# print("gjghhjghjgjh")


while True:
    sucess, imgwebcam = cap.read()
    imgAug = imgwebcam.copy()
    he, wi, cll = imgwebcam.shape
    print("shape of imagewebcam")

    print(wi)

    thres = 15
    kp2, des2 = orb.detectAndCompute(imgwebcam, None)
    bf = cv2.BFMatcher()
    matchList = []
    finalVal = -1
    good3 = []

    for des in desList:
        matches = bf.knnMatch(des, des2, k=2)
        good = []

        for m, n in matches:
            if m.distance < 0.70 * n.distance:
                good.append([m])

        # print("len of good")
        # print(len(good))
        matchList.append(len(good))
        good3.append(good)

    # print(matchList)
    print("matchlist")
    print(matchList)


    def vvalue(matchList, thres=15):
        val = -1
        if len(matchList) != 0:
            if max(matchList) > thres:
                val = matchList.index(max(matchList))
        return val

    print("hfdjdsfkjdsfhkjdshfjdshfjdskfhdskjfhdjfhjkfhdskjfdskjfhdsjfhdksjfhkdskjsdfhkdsjfhjdskhfkjfhkdskdsjskjdhfdkjkfksfkdsfdffkdfsdhfjsdfds")
    print(xyz[vvalue(matchList)][0])
    if detection == False:
        videos[vvalue(matchList)].set(cv2.CAP_PROP_POS_FRAMES,0)
        frameCounter = 0
    else:
        if frameCounter == videos[vvalue(matchList)].get(cv2.CAP_PROP_FRAME_COUNT):
            videos[vvalue(matchList)].set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0
        success, imgVideo[vvalue(matchList)] = videos[vvalue(matchList)].read()
        imgVideo[vvalue(matchList)] = cv2.resize(imgVideo[vvalue(matchList)], (xyz[vvalue(matchList)][1], xyz[vvalue(matchList)][0]))

    print("vvalue")
    imgvideoo=imgVideo
    print(vvalue(matchList))
    print("good matchlisthghjghg")
    print(len(good3[vvalue(matchList)]))
 #   print(good3[vvalue(matchList)][0][0])
    if matchList[vvalue(matchList)] > 20:
        detection = True
        #for i in good3[vvalue(matchList)]:
        d = []
        e = good3[vvalue(matchList)]
        i = 0
        while (i < len(e)):
            d.append(e[i][0])
            i = i + 1
        print(d)
        scrPts = np.float32([keypnts[vvalue(matchList)][m.queryIdx].pt for m in d]).reshape(-1, 1, 2)
        print("strpts")
        print(scrPts)
        dstPts = np.float32([kp2[m.trainIdx].pt for m in d]).reshape(-1, 1, 2)
        matrix, mask = cv2.findHomography(scrPts, dstPts, cv2.RANSAC, 5)
        print(matrix)
        print("step1")
        pts = np.float32([[0, 0], [0, xyz[vvalue(matchList)][0]], [xyz[vvalue(matchList)][1], xyz[vvalue(matchList)][0]],[xyz[vvalue(matchList)][1], 0]]).reshape(-1, 1, 2)
        print("step2")
        print(pts)
        dst = cv2.perspectiveTransform(pts, matrix)
        imgWarp = cv2.warpPerspective(imgVideo[vvalue(matchList)], matrix, (wi, he))
        maskNew = np.zeros((he, wi), np.uint8)
        cv2.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255))
        maskInv = cv2.bitwise_not(maskNew)
        imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskInv)
        imgAug = cv2.bitwise_or(imgWarp, imgAug)
    cv2.imshow('maskNew', imgAug)
    # print(matchList)
    # print(vvalue(matchList))
    cv2.waitKey(1)
    frameCounter += 1000
