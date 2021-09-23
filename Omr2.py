import cv2
import numpy as np
import glob
import numpy
import utlis

########################################################################
heightImg2 = 1500
widthImg2  = 2000
heightImg = 1200
widthImg  = 750
########################################################################

file = open("results.txt","w")
images = glob.glob('C:/Users/hp/Downloads/drive-download-20210914T193949Z-001/*.jpg')
chars = ['A','B','C','Ç','D','E','F','G','Ğ','H','I','İ','J','K','L','M','N','O','Ö','P','R','S','Ş','T','U','Ü','V','Y','Z']
marks = ['A','B','C','D','D','D']
nums = [0,1,2,3,4,5,6,7,8,9]
numberY = [0,0,0,0,0,0]
prev = [-1,-1,-1,-1,-1,-1]
for image in images:
    img=cv2.imread(image) #read image
    img = cv2.resize(img, (widthImg2, heightImg2)) # RESIZE IMAGE
    print('\n')
    print(image)
    
    ad = ""; soyad = ""; cinsiyet = ""; ogrnum = ""; kurumno = ""; sinif = ""; ktm = ""; ktdy = "";
    hayat = ""; türk = ""; mat = ""; fen = ""; ing = "";
    sosyalOrta = ""; türkOrta = ""; matOrta = ""; dinOrta = ""; fenOrta = ""; ingOrta = "";

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #turn image to gray
    blur = cv2.GaussianBlur(gray,(3, 3), 0) #add blur

  #  cv2.imshow("blur",blur)
    edges = cv2.Canny(blur,5,130) #find edges
    
    contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #find contours
    cv2.drawContours(img, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS
    rectCon = utlis.rectContour(contours) # FILTER FOR RECTANGLE CONTOURS
    p1 = utlis.getCornerPoints(rectCon[0]) # GET CORNER POINTS OF THE BIGGEST RECTANGLE
    p1 = utlis.reorder(p1) # REORDER FOR WARPING
    p2 = utlis.getCornerPoints(rectCon[1]) # GET CORNER POINTS OF THE BIGGEST RECTANGLE
    p2 = utlis.reorder(p2) # REORDER FOR WARPING
    p3 = utlis.getCornerPoints(rectCon[2]) # GET CORNER POINTS OF THE BIGGEST RECTANGLE
    p3 = utlis.reorder(p3) # REORDER FOR WARPING
    p4 = utlis.getCornerPoints(rectCon[3]) # GET CORNER POINTS OF THE BIGGEST RECTANGLE
    p4 = utlis.reorder(p4) # REORDER FOR WARPING
    pts1 = np.float32(p1) # PREPARE POINTS FOR WARP
    pts2 = np.float32([[0, 0],[widthImg2, 0], [0, heightImg2],[widthImg2, heightImg2]]) # PREPARE POINTS FOR WARP
    matrix = cv2.getPerspectiveTransform(pts1, pts2) # GET TRANSFORMATION MATRIX
    ImgOrta = cv2.warpPerspective(img, matrix, (widthImg2, heightImg2)) # APPLY WARP PERSPECTIVE
    pts3 = np.float32(p2) # PREPARE POINTS FOR WARP
    pts4 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
    matrix = cv2.getPerspectiveTransform(pts3, pts4) # GET TRANSFORMATION MATRIX
    ImgIlk = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) # APPLY WARP PERSPECTIVE
    pts5 = np.float32(p3) # PREPARE POINTS FOR WARP
    pts6 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
    matrix = cv2.getPerspectiveTransform(pts5, pts6) # GET TRANSFORMATION MATRIX
    ImgSoyad = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) # APPLY WARP PERSPECTIVE
    pts7 = np.float32(p4) # PREPARE POINTS FOR WARP
    pts8 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
    matrix = cv2.getPerspectiveTransform(pts7, pts8) # GET TRANSFORMATION MATRIX
    ImgAd = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) # APPLY WARP PERSPECTIVE  
    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= False)
    num = len(sorted_contours)-1
    temp = 15
    
    while temp > 0 :
        a = False
        area = 0
        yPrev = [0,510,0,0,590]
        
        counter = 0
        questNum = [0,0,0,0,0]
        item= sorted_contours[num]
        peri = cv2.arcLength(item, True)  
        approx = cv2.approxPolyDP(item, 0.001 * peri, True)
        minInColumns = numpy.amin(approx, axis=0)
        maxInColumns = numpy.amax(approx, axis=0)
      #  print(minInColumns[0],"---",maxInColumns[0])
        e, f, g, h = cv2.boundingRect(approx)
        h = f+h
        g = e+g
        crpImg = img[f:h, e:g]
        
        rect = cv2.minAreaRect(item) # get a rectangle rotated to have minimal area
        angle = rect[2]
        rows,cols = crpImg.shape[0], crpImg.shape[1]
        #M = cv2.getRotationMatrix2D((cols/2,rows/2),angle-90.3,1)
        img_rot = crpImg
        #cv2.imshow("img",img_rot)
        #cv2.waitKey(0)
       # img_rot = cv2.warpAffine(crpImg,M,(cols,rows))
        kernel = np.ones((3, 3), np.uint8)
        if f > 30 and f < 150 and e > 490 and e < 650 and ((h > 680 and h < 850) and (g > 930 and g < 1150)):
            area = 1    #soyad
            img_rot = ImgSoyad[90:heightImg,0:widthImg]
        elif f > 0 and f < 100 and e > 1240 and e < 1400 and ((h > 680 and h < 820) and (g > 1850 and g < 2020)) :
            kernel = np.ones((2, 2), np.uint8)
            a = True
            img_rot = ImgIlk[110:heightImg,0:widthImg]
            area = 2    #ilkokul
        elif f > 260 and f < 450 and e > 990 and e < 1180 and ((h > 550 and h < 770) and (g > 1170 and g < 1370)):
            area = 3    #sınıf
            img_rot = img_rot[50:h,0:g]
         #   cv2.imshow("sinif",img_rot)
         #   cv2.waitKey(0)
        elif f > 600 and f < 750 and e > 990 and e < 1180 and ((h > 670 and h < 830) and (g > 1180 and g < 1320)):
            area = 4     #cinsiyet
           # cv2.imshow("cins",img_rot)
           # cv2.waitKey(0)
        elif f > 690 and f < 810 and e > 430 and e < 590 and ((h > 1350 and h < 1510) and (g > 1840 and g < 2020)):
            kernel = np.ones((2, 2), np.uint8)
            a = True    
            img_rot = ImgOrta[200:heightImg2,0:widthImg2]
            area = 5    #ortaokul
        elif f > 20 and f < 120 and e > 960 and e < 1160 and ((h > 270 and h < 420) and (g > 1245 and g < 1420)):
            area = 6    #ogrenci no
            img_rot = img_rot[55:h,0:g]
          #  cv2.imshow("Ogrenci",img_rot)
          #  cv2.waitKey(0)
        elif f > 20 and f < 130 and e > 60 and e < 210 and ((h > 690 and h < 860) and (g > 450 and g < 650)):
            area = 7    #ad
            img_rot = ImgAd[90:heightImg,0:widthImg]
           # cv2.imshow("img_rot",img_rot)
           # cv2.waitKey(0)
        elif f > 690 and f < 850 and e > 60 and e < 220 and ((h > 810 and h < 970) and (g > 400 and g < 570)):
            area = 8    #kitapçık
            img_rot = img_rot[50:h,0:g]
           # cv2.imshow("Kitapcik",img_rot)
           # cv2.waitKey(0)
        elif f > 800 and f < 970 and e > 50 and e < 210 and ((h > 1080 and h < 1250) and (g > 360 and g < 580)):
            area = 9    #Kurum
            img_rot = img_rot[55:h,0:g]
            #cv2.imshow("Kurum",img_rot)
           # cv2.waitKey(0)
        temp = temp - 1
        num = num - 1
        if area == 0 :
            continue
        lower_bound = np.array([0,0,10])
        upper_bound = np.array([255,255,190])
     #   image = crpImg
        
        mask = cv2.inRange(img_rot, lower_bound, upper_bound)
        for i in range(2):
            mask = cv2.dilate(mask, kernel, iterations=2)
            mask = cv2.erode(mask, kernel, iterations=4)
            mask = cv2.dilate(mask, kernel, iterations=2)
                
        closing = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        conts = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
        cv2.drawContours(img_rot, conts, -1, (0, 255, 0), 2) 
        prevR = [0, 0, 0, 0, 0, 0]
        if a == False :
            conts.sort(key=lambda x:cv2.boundingRect(x)[0])
        else :
            conts.sort(key=lambda x:cv2.boundingRect(x)[1])
        for cr in conts:
            (x,y),r = cv2.minEnclosingCircle(cr)
            counter = counter + 1
            center = (int(x),int(y))         
            if r >= 14 and r <= 35 :              
                if area == 7 :
                    char = chars[int((y)/38)]
                    ad = ad + char                   
                elif area == 1 :
                    char = chars[int((y)/38)]
                    soyad = soyad + char
                elif area == 4 :
                    char = chars[int((y)/45)]
                    if char == 'A':
                        cinsiyet = "KIZ"
                    else :
                        cinsiyet = "ERKEK"
                elif area == 9 or area == 6:
                    if area == 6:
                        ogrnum = ogrnum + str(int((y-10)/20))
                    else :
                        kurumno = kurumno + str(round((y)/22))
                elif area == 3:
                    if x < 80 and sinif == '':
                        sinif = sinif + str(int((y)/20)+2)
                    elif x > 80 and x < 130 :
                        char = chars[int((y)/20)]
                        sinif = sinif + char
                    elif x > 130 :
                        sinif = sinif + chars[int((y)/20)+12]
                elif area == 8 :
                    if x < 190 :
                        if y < 40 :
                            ktm = "A"
                        else :
                            ktdy = "A"
                    else : 
                        if y < 40 :
                            ktm = "B"
                        else :
                            ktdy = "B"
                elif area == 2 :
                    if x < 250:
                        a = round((y)/40)
                        if a < 14 :
                            if((y - yPrev[0]) < 20) :
                                if abs(r - prevR[0]) < 7 :
                                    hayat = hayat[0:-2] + 'X '
                                elif prevR[0] < r :
                                    hayat = hayat[0:-2]
                                    hayat = hayat + str(questNum[0]) + marks[int((x-70)/50)] + " "
                                else :
                                    continue
                            else :
                                prevQNum = questNum[0]
                                questNum[0] = questNum[0] + round((y - yPrev[0])/48)
                                if ((questNum[0] - prevQNum) > 1) :
                                    while ((questNum[0] - prevQNum) > 1) :
                                        prevQNum = prevQNum + 1
                                        hayat = hayat + str(prevQNum) + "  "
                                hayat = hayat + str(questNum[0]) + marks[int((x-70)/50)] + " "
                            yPrev[0] = y
                            prevR[0] = r
                        else :
                            if ((y - yPrev[1]) < 20) :
                                if abs(r - prevR[1]) < 7 :
                                    fen = fen[0:-2] + 'X '
                                elif prevR[1] < r :
                                    fen = fen[0:-2]
                                    fen = fen + str(questNum[0]) + marks[int((x-70)/50)] + " "
                                else :
                                    continue
                            else :
                                prevQNum = questNum[1]
                                questNum[1] = questNum[1] + round((y - yPrev[1])/48)
                                if ((questNum[1] - prevQNum) > 1) :
                                    while ((questNum[1] - prevQNum) > 1) :
                                        prevQNum = prevQNum + 1
                                        fen = fen + str(prevQNum) + "  "
                                fen = fen + str(questNum[1]) + marks[int((x-70)/50)] + " "
                            yPrev[1] = y
                            prevR[1] = r
                    elif x < 500 :
                        if((y - yPrev[2]) < 20) :
                            if abs(r- prevR[2]) < 7 :
                                türk = türk[0:-2] + 'X '
                            elif prevR[0] < r :
                                türk = türk[0:-2]
                                türk = türk + str(questNum[0]) + marks[int((x-70)/50)] + " "
                            else :
                                continue
                        else :
                            prevQNum = questNum[2]
                            questNum[2] = questNum[2] + round((y - yPrev[2])/48)
                            if ((questNum[2] - prevQNum) > 1) :
                                while ((questNum[2] - prevQNum) > 1) :
                                    prevQNum = prevQNum + 1
                                    türk = türk + str(prevQNum) + "  "
                            türk = türk + str(questNum[2]) + marks[int((x-340)/50)] + " "
                        yPrev[2] = y
                        prevR[2] = r
                    elif x < 750:
                        b = int((y)/40)
                        if b < 16 :
                            if((y - yPrev[3]) < 20) :
                                if abs(r- prevR[3]) < 7 :
                                    mat = mat[0:-2] + 'X '
                                elif prevR[3] < r :
                                    mat = mat[0:-2]
                                    mat = mat + str(questNum[0]) + marks[int((x-70)/50)] + " "
                                else :
                                    continue
                            else :
                                prevQNum = questNum[3]
                                questNum[3] = questNum[3] + round((y - yPrev[3])/48)
                                if ((questNum[3] - prevQNum) > 1) :
                                    while ((questNum[3] - prevQNum) > 1) :
                                        prevQNum = prevQNum + 1
                                        mat = mat + str(prevQNum) + "  "
                                mat = mat + str(questNum[3]) + marks[int((x-600)/50)] + " "
                            yPrev[3] = y
                            prevR[3] = r
                        else :
                            if((y - yPrev[4]) < 20) :
                                if abs(r- prevR[4]) < 7 :
                                    ing = ing[0:-2] + 'X '
                                elif prevR[4] < r :
                                    ing = ing[0:-2]
                                    ing = ing + str(questNum[0]) + marks[int((x-70)/50)] + " "
                                else :
                                    continue
                            else :
                                prevQNum = questNum[4]
                                questNum[4] = questNum[4] + round((y - yPrev[4])/48)
                                if ((questNum[4] - prevQNum) > 1) :
                                    while ((questNum[4] - prevQNum) > 1) :
                                        prevQNum = prevQNum + 1
                                        ing = ing + str(prevQNum) + "  "
                                ing = ing + str(questNum[4]) + marks[int((x-600)/50)] + " "
                            yPrev[4] = y
                            prevR[4] = r
                if area == 5 :    
                    if x < 350:
                        prevQNum = numberY[0]
                        numberY[0] = round((y)/48)                        
                        if ((numberY[0] - prevQNum) > 1) :
                            while ((numberY[0] - prevQNum) > 1) :
                                prevQNum = prevQNum + 1
                                türkOrta = türkOrta + str(prevQNum) + "  "
                        numberX = int((x - 70)/50)      
                        if numberY[0] == prev[0]:
                            if abs(r - prevR[0]) < 7 :
                                türkOrta = türkOrta[0: -2]
                                türkOrta = türkOrta + "X "  
                                continue
                            elif prevR[0] < r:
                                türkOrta = türkOrta[0: -2]
                            elif prevR[0] > r:
                                continue
                        türkOrta = türkOrta + str(numberY[0]) + marks[numberX] + " "
                        prev[0] = numberY[0]
                        prevR[0] = r
                    elif x < 670 :
                        prevQNum = numberY[1]
                        numberY[1] = round((y)/48)                        
                        if ((numberY[1] - prevQNum) > 1) :
                            while ((numberY[1] - prevQNum) > 1) :
                                prevQNum = prevQNum + 1
                                matOrta = matOrta + str(prevQNum) + "  "    
                        numberX = int((x - 415)/50)      
                        if numberY[1] == prev[1] :
                            if abs(r - prevR[1]) < 7 :
                                matOrta = matOrta[0:-2]
                                matOrta = matOrta + "X "  
                                continue
                            elif prevR[1] < r:
                                matOrta = matOrta[0: -2]
                            elif prevR[1] > r:
                                continue                   
                        matOrta = matOrta + str(numberY[1]) + marks[numberX] + " "
                        prev[1] = numberY[1]
                        prevR[1] = r
                    elif x < 1000 :
                        prevQNum = numberY[2]
                        numberY[2] = round((y)/48)                        
                        if ((numberY[2] - prevQNum) > 1) :
                            while ((numberY[2] - prevQNum) > 1) :
                                prevQNum = prevQNum + 1
                                dinOrta = dinOrta + str(prevQNum) + "  "
                        numberX = int((x - 755)/50)      
                        if numberY[2] == prev[2] :
                            if abs(r - prevR[2]) < 7 :
                                dinOrta = dinOrta[0:-2]
                                dinOrta = dinOrta + "X "    
                                continue
                            elif prevR[1] < r:
                                dinOrta = dinOrta[0: -2]
                            elif prevR[1] > r:
                                continue
                        dinOrta = dinOrta + str(numberY[2]) + marks[numberX] + " "
                        prev[2] = numberY[2]
                        prevR[2] = r
                    elif x < 1340 :
                        prevQNum = numberY[3]
                        numberY[3] = round((y)/48)                        
                        if ((numberY[3] - prevQNum) > 1) :
                            while ((numberY[3] - prevQNum) > 1) :
                                prevQNum = prevQNum + 1
                                fenOrta = fenOrta + str(prevQNum) + "  "
                        numberX = int((x - 1090)/50)      
                        if numberY[3] == prev[3] :
                            if abs(r - prevR[3]) < 7 :
                                fenOrta = fenOrta[0:-2]
                                fenOrta = fenOrta + "X "  
                                continue
                            elif prevR[3] < r:
                                fenOrta = fenOrta[0: -2]
                            elif prevR[3] > r:
                                continue                 
                        fenOrta = fenOrta + str(numberY[3]) + marks[numberX] + " "
                        prev[3] = numberY[3]
                        prevR[3] = r
                    elif x < 1670 :
                        prevQNum = numberY[4]
                        numberY[4] = round((y)/48)
                        if ((numberY[4] - prevQNum) > 1) :
                            while ((numberY[4] - prevQNum) > 1) :
                                prevQNum = prevQNum + 1
                                sosyalOrta = sosyalOrta + str(prevQNum) + "  "
                        numberX = int((x - 1440)/50)      
                        if numberY[4] == prev[4] :
                            if abs(r - prevR[4]) < 7 :
                                sosyalOrta = sosyalOrta[0:-2]
                                sosyalOrta = sosyalOrta + "X "  
                                continue
                            elif prevR[4] < r:
                                sosyalOrta = sosyalOrta[0: -2]
                            elif prevR[4] > r:
                                continue       
                        sosyalOrta = sosyalOrta + str(numberY[4]) + marks[numberX] + " "
                        prev[4] = numberY[4]
                        prevR[4] = r
                    elif x < 2000 :
                        prevQNum = numberY[5]
                        numberY[5] = round((y)/48)
                        if ((numberY[5] - prevQNum) > 1) :
                            while ((numberY[5] - prevQNum) > 1) :
                                prevQNum = prevQNum + 1
                                ingOrta = ingOrta + str(prevQNum) + "  "
                        numberX = int((x - 1780)/50)   
                        if numberY[5] > 27 : 
                            continue   
                        if numberY[5] == prev[5] :
                            if abs(r - prevR[5]) < 7 :
                                ingOrta = ingOrta[0:-2]
                                ingOrta = ingOrta + "X "  
                                continue         
                            elif prevR[5] < r:
                                ingOrta = ingOrta[0: -2]
                            elif prevR[5] > r:
                                continue          
                        ingOrta = ingOrta + str(numberY[5]) + marks[numberX] + " "
                        prev[5] = numberY[5]
                        prevR[5] = r
    print(ad + " " + soyad)
    print("Kurum No :",kurumno)
    print("Cinsiyet :", cinsiyet)
    print("Ogrenci No :", ogrnum)
    print("Sınıf :", sinif)
    print("Matematik Meb Kitapçık :",ktm)
    print("Matematik Diger Yayınlar :",ktdy)
    print("Türkçe Orta :",türkOrta)
    print("Matematik Orta :",matOrta)
    print("Din Kültürü :",dinOrta)
    print("Fen Bilgisi Orta :",fenOrta)
    print("Sosyal :",sosyalOrta)
    print("İngilizce Orta :",ingOrta)  
    print("Hayat Bilgisi :",hayat)
    print("Türkçe :",türk)
    print("Matematik :",mat)
    print("Fen Bilgisi :",fen)
    print("İngilizce :",ing)
    print("end")

    file.write(image + '\n')
    file.write(ad + " " + soyad + '\n')
    file.write("Kurum No : " + kurumno + '\n')
    file.write("Cinsiyet :" + cinsiyet + '\n')
    file.write("Ogrenci No :" + ogrnum + '\n')
    file.write("Sınıf :" + sinif + '\n')
    file.write("Matematik Meb Kitapçık :" + ktm + '\n')
    file.write("Matematik Diger Yayınlar :" + ktdy + '\n')
    file.write("Türkçe Orta : " + türkOrta + '\n')
    file.write("Matematik Orta : " + matOrta + '\n')
    file.write("Din Kültürü : " + dinOrta + '\n')
    file.write("Fen Bilgisi Orta : " + fenOrta + '\n')
    file.write("Sosyal : " + sosyalOrta + '\n')
    file.write("İngilizce Orta : " + ingOrta + '\n')  
    file.write("Hayat Bilgisi : " + hayat + '\n')
    file.write("Türkçe : " + türk + '\n')
    file.write("Matematik : " + mat + '\n')
    file.write("Fen Bilgisi : " + fen + '\n')
    file.write("İngilizce : " + ing + '\n')
    file.write("end" + '\n')
    file.write('\n')
file.close() 