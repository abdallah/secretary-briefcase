#qpy:console
import os
import os.path
import time
import multiprocessing
from multiprocessing import Process
import androidhelper
#from jnius import autoclass
#from jnius import JavaException
from android import AndroidBrowser

PROJECT_DIR = os.path.dirname(__file__)
DATABASE_FILE = os.path.join(PROJECT_DIR, 'nec.sqlite')
droid = androidhelper.Android()

def showurl(url='http://localhost:8000'):
    time.sleep(5)
    print "[nec] Browser"
    droid.view(url)

if not os.path.exists(DATABASE_FILE):
    print "[nec] Syncdb" 
    os.system("cd %s && python manage.py syncdb" % PROJECT_DIR)
    
#print "[nec] Backup"
#droid.sendEmail('', 'Backup NEC', 'NEC database backup', 'file://%s' % DATABASE_FILE)

p=Process(target=showurl)
p.start()
print "[nec] Runserver"
os.system("cd %s && python manage.py runserver 0.0.0.0:8000" % PROJECT_DIR)
