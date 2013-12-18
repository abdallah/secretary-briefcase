#qpy:console
import os
import os.path
import time
import multiprocessing
from multiprocessing import Process
import androidhelper
droid = androidhelper.Android()

def showurl(url='http://localhost:8000'):
    time.sleep(5)
    droid.webViewShow(url)

p=Process(target=showurl)
p.start()

#print "[nec] Syncdb" 
#os.system("cd %s && python manage.py syncdb" % os.path.dirname(__file__))
print "[nec] Runserver"
os.system("cd %s && python manage.py runserver 0.0.0.0:8000" % os.path.dirname(__file__))