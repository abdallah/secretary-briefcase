#qpy:console
import os
import os.path
import androidhelper
from django.http import HttpResponseRedirect, HttpResponseBadRequest

PROJECT_DIR = os.path.dirname(__file__)
DATABASE_FILE = os.path.join(PROJECT_DIR, 'nec.sqlite')
droid = androidhelper.Android()

def backup(request):
    if not os.path.exists(DATABASE_FILE):
        os.system("cd %s && python manage.py syncdb" % PROJECT_DIR)

    print "[nec] Backup"
    try:
        droid.sendEmail('', 'Backup NEC', 'NEC database backup', 'file://%s' % DATABASE_FILE)
        return HttpResponseRedirect('/')
    except:
        return HttpResponseBadRequest()