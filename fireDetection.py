import cv2
import threading   
import playsound  
import smtplib     

fire_cascade = cv2.CascadeClassifier('fire_detection.xml')                                                                      

vid = cv2.VideoCapture("istockphoto-1455772765-640_adpp_is.mp4")
runOnce = False 
runOnce1 = False 
def play_alarm_sound_function():
    playsound.playsound('fire_alarm.mp3',True)
    print("Fire alarm end")
def send_mail_function(): 
    recipientmail = "mail id"
    recipientmail = recipientmail.lower()
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("users mail", 'czkuahlgjdzetykr')
        server.sendmail('users mail', recipientmail, "Warning fire accident has been reported")
        print("Alert mail sent sucesfully to {}".format(recipientmail))
        server.close()     
    except Exception as e:
        print(e)		
while(True):
    Alarm_Status = False
    ret, frame = vid.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(frame, 1.2, 3)
    for (x,y,w,h) in fire:
        cv2.rectangle(frame,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        print("Fire alarm initiated")
        threading.Thread(target=play_alarm_sound_function).start()

        if runOnce == False:
            print("Mail send initiated")
            threading.Thread(target=send_mail_function).start()
            runOnce = True
        if runOnce == False:
            print("Mail is already sent once")
            runOnce = True
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
