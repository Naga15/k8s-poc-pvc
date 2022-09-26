import os.path
import time
from datetime import datetime 


f= open("test.txt", "w")

i=0 

while(True):
   
    dt_string = datetime.now()
    f.write("Current Time: "+str(dt_string.strftime("%d/%m/%Y %H:%M:%S")) +"\n")

    print ("Current Time: " +str(dt_string.strftime("%d/%m/%Y %H:%M:%S")) + "\n")

    time.sleep(1200)

    elapsed_time1= datetime.now()
    f.write("Time after 20 minutes: " +str(elapsed_time1.strftime("%d/%m/%Y %H:%M:%S")) +"\n")

    print ("Time after 20 minutes: "+str(elapsed_time1.strftime("%d/%m/%Y %H:%M:%S")))

    time.sleep(1800)
    elapsed_time2= datetime.now()


    if(((elapsed_time2-dt_string).seconds) == 3000):
        i=i+1
        print("Time after 50 minutes: " +"Hello"+ str(i) + " " +str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        f.write("Time after 50 minutes: " +"Hello"+ str(i) + " " +str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) +"\n")
      
    
    