import cv2
import numpy as np
import glob
import numpy

def reorder(myPoints):
    #baslayalım
    myPoints = myPoints.reshape((4, 2))
    #baslayalım2
    myPointsNew = np.zeros((4, 1, 2), np.int32) 
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]  #[0,0]
    myPointsNew[3] =myPoints[np.argmax(add)]   #[w,h]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]  #[w,0]
    myPointsNew[2] = myPoints[np.argmax(diff)] #[h,0]
    #print(diff)

    return myPointsNew

file = open("results.txt","w")
images = glob.glob('C:/Users/hp/Downloads/drive-download-20210914T193949Z-001/*.jpg')
chars = ['A','B','C','Ç','D','E','F','G','Ğ','H','I','İ','J','K','L','M','N','O','Ö','P','R','S','Ş','T','U','Ü','V','Y','Z']
nums = [0,1,2,3,4,5,6,7,8,9]
for image in images:
    img=cv2.imread(image) #read image
    img = cv2.resize(img, (3518, 2506))
    print('\n')
    print(image)
    
    ad = ""; soyad = ""; cinsiyet = ""; ogrnum = ""; kurumno = ""; sinif = ""; ktm = ""; ktdy = "";
    hayat = ""; türk = ""; mat = ""; fen = ""; ing = "";
    sosyal = ""; türkOrta = ""; matOrta = ""; din = ""; fenOrta = ""; ingOrta = "";

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #turn image to gray
    blur = cv2.GaussianBlur(gray,(3, 3), 0) #add blur

  #  cv2.imshow("blur",blur)
    edges = cv2.Canny(blur,5,130) #find edges
    
    contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #find contours
    sorted_contours= sorted(contours, key=cv2.contourArea, reverse= False)
    num = len(sorted_contours)-1
    temp = 15
    while temp > 0 :
        a = False
        area = 0
        y1 = [-10,-10,-10,-10,-10,-10]
        
        counter = 0
        questNum = [0,0,0,0,0,0]
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
        cv2.imshow("crpImg",crpImg)
        cv2.waitKey(0)
        rect = cv2.minAreaRect(item) # get a rectangle rotated to have minimal area
        angle = rect[2]
        rows,cols = crpImg.shape[0], crpImg.shape[1]
        #M = cv2.getRotationMatrix2D((cols/2,rows/2),angle-90.3,1)
        img_rot = crpImg
       # img_rot = cv2.warpAffine(crpImg,M,(cols,rows))
        kernel = np.ones((3, 3), np.uint8)
        if f > 160 and f < 260 and e > 660 and e < 760 and ((h > 1735 and h < 1835) and (g > 1250 and g < 1350)):
            area = 1
        elif f > 150 and f < 200 and e > 1630 and e < 1700 and ((h > 1730 and h < 1830) and (g > 2350 and g < 2450)) :
            kernel = np.ones((2, 2), np.uint8)
            a = True
            area = 2
        elif f > 820 and f < 900 and e > 1280 and e < 1370 and ((h > 1500 and h < 1570) and (g < 1590 and g > 1500)):
            area = 3
        elif f > 1560 and f < 1650 and e > 1300 and e < 1380 and ((h > 1740 and h < 1820) and (g > 1500 and g < 1600)):
           area = 4
        elif f > 1750 and f < 1850 and e > 600 and e < 700 and ((h > 3350 and h < 3440) and (g > 2375 and g < 2465)):
            kernel = np.ones((2, 2), np.uint8)
            a = True
            img_rot = img_rot[170:h,0:g]
            area = 5
        elif f > 160 and f < 250 and e > 1270 and e < 1360 and ((h > 790 and h < 870) and (g > 1585 and g < 1675)):
            area = 6
        elif f > 170 and f < 270 and e > 120 and e < 200 and ((h > 1750 and h < 1840) and (g > 650 and g < 750)):
            area = 7
            img_rot = img_rot[120:h,0:g]
        elif f > 1790 and f < 1870 and e > 150 and e < 250 and ((h > 2060 and h < 2135) and (g > 550 and g < 650)):
            area = 8
        elif f > 2080 and f < 2170 and e > 150 and e < 250 and ((h > 2710 and h < 2790) and (g > 560 and g < 660)):
            area = 9
        temp = temp - 1
        num = num - 1
        if area == 0 :
            continue
        lower_bound = np.array([0,0,10])
        upper_bound = np.array([255,255,195])
     #   image = crpImg
     #   cv2.imshow("img_rot1",img_rot)
         
        mask = cv2.inRange(img_rot, lower_bound, upper_bound)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1)   
       # cv2.imshow("mask",mask)       
        closing = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        conts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
        if a == False :
         #   img_rot = img_rot[11:h,0:g]
            conts.sort(key=lambda x:cv2.boundingRect(x)[0])
        else :
            conts.sort(key=lambda x:cv2.boundingRect(x)[1])
        
        for cr in conts:
            (x,y),r = cv2.minEnclosingCircle(cr)
            counter = counter + 1
            center = (int(x),int(y))         
            if r >= 13.5 and r <= 30:              
                if area == 7 :
                    char = chars[int((y)/50)]
                    ad = ad + char
                    
                elif area == 1 :
                    if ( y < 130 ) :
                        continue
                    char = chars[int((y-130)/50)]
                    soyad = soyad + char
                elif area == 4 :
                    char = chars[int((y-60)/50)]
                    if char == 'A':
                        cinsiyet = "KIZ"
                    else :
                        cinsiyet = "ERKEK"
                elif area == 9 or area == 6:
                    if y < 100:
                        continue
                    if area == 6:
                        ogrnum = ogrnum + str(int((y-100)/50))
                    else :
                        kurumno = kurumno + str(int((y-100)/50))
                elif area == 3:
                    if y < 110:
                        continue
                    char = chars[int((y-110)/50)]
                    if x < 100 and sinif == '':
                        sinif = sinif + str(int((y-120)/50)+2)
                    elif x > 100 and x < 150 :
                        sinif = sinif + char
                    elif x > 150 :
                        sinif = sinif + chars[int((y-120)/50)+12]
                elif area == 8 :
                    if x < 200 :
                        if y < 180 :
                            ktm = "A"
                        else :
                            ktdy = "A"
                    else : 
                        if y < 180 :
                            ktm = "B"
                        else :
                            ktdy = "B"
                elif area == 2 :
                    margin = e - 1650
                    margin = int(margin/2)
                    if x < 250:
                        a = int((y-120)/50)
                        if a < 14 :
                            hayat = hayat + str(int((y-120)/50))
                            if x < 105 + margin :
                                hayat = hayat + "A "
                            elif x < 155 + margin :
                                hayat = hayat + "B "
                            else :
                                hayat = hayat + "C "
                        else :
                            fen = fen + str(int((y-830)/50))
                            if x < 110 + margin :
                                fen = fen + "A "
                            elif x < 160 + margin :
                                fen = fen + "B "
                            else :
                                fen = fen + "C "
                    elif x < 500 :
                        türk = türk + str(int((y-120)/50))
                        if x < 360  + margin:
                            türk = türk + "A "
                        elif x < 410  + margin:
                            türk = türk + "B "
                        else :
                            türk = türk + "C "
                    elif x < 750:
                        b = int((y-120)/50)
                        if b < 16 :
                            mat = mat + str(int((y-120)/50))
                            if x < 605 + margin :
                                mat = mat + "A "
                            elif x < 655 + margin :
                                mat = mat + "B "
                            else :
                                mat = mat + "C "
                        else :
                            ing = ing + str(int((y-930)/50))
                            if x < 605 + margin:
                                ing = ing + "A "
                            elif x < 655 + margin :
                                ing = ing + "B "
                            else :
                                ing = ing + "C "
                if area == 5 :  
                    margin = 620 - e 
                    margin = int(margin*0.3)
                    prev = 0
                    number = int((y - 60)/50) + 1        
                    if x < 300:      
                        if number == prev :
                            türkOrta[-1] = "x "  
                            continue                   
                        türkOrta = türkOrta + str(number)
                        prev = number
                        if x < 110 + margin :
                            türkOrta = türkOrta + "A "
                        elif x < 160 + margin :
                            türkOrta = türkOrta + "B "
                        elif x < 210 + margin :
                            türkOrta = türkOrta + "C "
                        else :
                            türkOrta = türkOrta + "D "
                    elif x < 600 :
                        if number == prev :
                            matOrta[-1] = "x "
                            continue
                        matOrta = matOrta + str(number)
                        if x < 410 + margin :
                            matOrta = matOrta + "A "
                        elif x < 460 + margin :
                            matOrta = matOrta + "B "
                        elif x < 510 + margin :
                            matOrta = matOrta + "C "
                        else :
                            matOrta = matOrta + "D "
                    elif x < 900 :
                        if number == prev :
                            din[-1] = "x "
                            continue
                        din = din + str(number)
                        if x < 710 + margin :
                            din = din + "A "
                        elif x < 760 + margin :
                            din = din + "B "
                        elif x < 810 + margin :
                            din = din + "C "
                        else :
                            din = din + "D "
                    elif x < 1200 :
                        if number == prev :
                            fenOrta[-1] = "x "
                            continue
                        fenOrta = fenOrta + str(number)
                        if x < 1015 + margin :
                            fenOrta = fenOrta + "A "
                        elif x < 1065 + margin :
                            fenOrta = fenOrta + "B "
                        elif x < 1115 + margin :
                            fenOrta = fenOrta + "C "
                        else :
                            fenOrta = fenOrta + "D "
                    elif x < 1500 :
                        if number == prev :
                            sosyal[-1] = x
                            continue
                        sosyal = sosyal + str(number)
                        if x < 1315 + margin :
                            sosyal = sosyal + "A "
                        elif x < 1365 + margin :
                            sosyal = sosyal + "B "
                        elif x < 1415 + margin :
                            sosyal = sosyal + "C "
                        else :
                            sosyal = sosyal + "D "
                    elif x < 1800 :
                        if number > 27 or y > 1560 : 
                            continue
                        if number == prev :
                            ingOrta[-1] = x
                            continue
                        ingOrta = ingOrta + str(number)
                        if x < 1615 + margin :
                            ingOrta = ingOrta + "A "
                        elif x < 1665 + margin :
                            ingOrta = ingOrta + "B "
                        elif x < 1715 + margin :
                            ingOrta = ingOrta + "C "
                        else :
                            ingOrta = ingOrta + "D "
        
    print(ad + " " + soyad)
    print("Kurum No :",kurumno)
    print("Cinsiyet :", cinsiyet)
    print("Ogrenci No :", ogrnum)
    print("Sınıf :", sinif)
    print("Matematik Meb Kitapçık :",ktm)
    print("Matematik Diger Yayınlar :",ktdy)
    print("Türkçe Orta :",türkOrta)
    print("Matematik Orta :",matOrta)
    print("Din Kültürü :",din)
    print("Fen Bilgisi Orta :",fenOrta)
    print("Sosyal :",sosyal)
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
    file.write("Din Kültürü : " + din + '\n')
    file.write("Fen Bilgisi Orta : " + fenOrta + '\n')
    file.write("Sosyal : " + sosyal + '\n')
    file.write("İngilizce Orta : " + ingOrta + '\n')  
    file.write("Hayat Bilgisi : " + hayat + '\n')
    file.write("Türkçe : " + türk + '\n')
    file.write("Matematik : " + mat + '\n')
    file.write("Fen Bilgisi : " + fen + '\n')
    file.write("İngilizce : " + ing + '\n')
    file.write("end" + '\n')
    file.write('\n')
file.close() 