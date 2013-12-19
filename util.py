#qpy:console
import os
import importlib
import os.path
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse

try:
    from androidhelper import Android
    droid = Android()
except ImportError:
    droid = None
    print "on server"

try: 
    settings = importlib.import_module('conf.settings')
    DATABASe_FILE = settings.DATABASES['default']['NAME']
except:
    DATABASE_FILE = os.path.join(PROJECT_DIR, 'congregation.sqlite')

PROJECT_DIR = os.path.dirname(__file__)

def backup(request):
    if not os.path.exists(DATABASE_FILE):
        os.system("cd %s && python manage.py syncdb" % PROJECT_DIR)

    print "[nec] Backup"
    try:
        if droid:
            droid.sendEmail('', 'Congregation Database Backup ', 'congregation database backup', 'file://%s' % DATABASE_FILE)
            return HttpResponseRedirect('/')
        else: 
            print '[nec] send %s' % DATABASE_FILE
            f = open(DATABASE_FILE, 'r')
            response = HttpResponse(f, content_type='application/*')
            response['Content-Disposition'] = 'attachment; filename=sec.sqlite'
            return response
    except:
        return HttpResponseBadRequest()
