#qpy:console
import os
import os.path
import time
import importlib
from multiprocessing import Process
import webbrowser
try:
    import androidhelper
    from android import AndroidBrowser
    droid = androidhelper.Android()
except ImportError:
    droid = None


PROJECT_DIR = os.path.dirname(__file__)
try:
    settings = importlib.import_module('conf.settings')
    DATABASE_FILE = settings.DATABASES['default']['NAME']
except:
    DATABASE_FILE = os.path.join(PROJECT_DIR, 'congregation.sqlite')



def showurl(url='http://localhost:8000'):
    time.sleep(5)
    print "[nec] Browser"
    if droid is not None:
        droid.view(url)
    else:
        webbrowser.open(url, 0)

if not os.path.exists(DATABASE_FILE):
    print "[nec] Syncdb"
    os.system("cd %s && python manage.py syncdb" % PROJECT_DIR)


p=Process(target=showurl)
p.start()
print "[nec] Runserver"
os.system("cd %s && python manage.py runserver 0.0.0.0:8000" % PROJECT_DIR)
