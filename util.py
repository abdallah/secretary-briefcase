#qpy:console
import os
import os.path
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.core.servers.basehttp import FileWrapper

try:
    from androidhelper import Android
    droid = Android()
except ImportError:
    droid = None
    print "on server"

PROJECT_DIR = os.path.dirname(__file__)
DATABASE_FILE = os.path.join(PROJECT_DIR, 'nec.sqlite')

def backup(request):
    if not os.path.exists(DATABASE_FILE):
        os.system("cd %s && python manage.py syncdb" % PROJECT_DIR)

    print "[nec] Backup"
    try:
        if droid:
            droid.sendEmail('', 'Backup NEC', 'NEC database backup', 'file://%s' % DATABASE_FILE)
            return HttpResponseRedirect('/')
        else: 
            print '[nec] send %s' % DATABASE_FILE
            f = open(DATABASE_FILE, 'r')
            response = HttpResponse(f, content_type='application/*')
            response['Content-Disposition'] = 'attachment; filename=sec.sqlite'
            return response
    except:
        return HttpResponseBadRequest()
