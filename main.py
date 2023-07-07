import cv2
import torch
from tracker import *
import numpy as np
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

cap=cv2.VideoCapture('/home/sadiaprome/Downloads/yolov5peoplecounterwin11-main/cctv.mp4')


def POINTS(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)
        

cv2.namedWindow('FRAME')
cv2.setMouseCallback('FRAME', POINTS)

tracker = Tracker()

#area_1=[(0,0),(0,500),(1020,500),(1020,0)]
#area1=set()
while True:
    ret,frame=cap.read()
    frame=cv2.resize(frame,(1020,500))
    #cv2.polylines(frame,[np.array(area_1,np.int32)],True,(0,255,0),3)
    results=model(frame)
    #frame=np.squeeze(results.render())
    list=[]
    for index,row in results.pandas().xyxy[0].iterrows():
        x1=int(row['xmin'])
        y1=int(row['ymin'])
        x2=int(row['xmax'])
        y2=int(row['ymax'])
        b=str(row['name'])
        if 'person' in b:
             list.append([x1,y1,x2,y2])
    boxes_ids=tracker.update(list)
    for box_id in boxes_ids:
        x,y,w,h,id=box_id        
        cv2.rectangle(frame,(x,y),(w,h),(255,0,255),2)
        cv2.putText(frame,str(id),(x,y),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2 )
        #result=cv2.pointPolygonTest(np.array(area_1,np.int32),(int(w),int(h)),False)
        #print(results)
        #if results > 0:
         #   area1.add(id)
    
    print(len(boxes_ids),'len of the boxes ids')  
    cv2.putText(frame,str(len(boxes_ids)),(20,30),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2 ) 
    #print(area1)
    #p=len(area1)
    cv2.imshow('FRAME',frame)
    if cv2.waitKey(1)&0xFF==27:
        break

cap.release()
cv2.destroyAllWindows()




    
    
