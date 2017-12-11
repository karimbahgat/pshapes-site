# imports
import sys
import os
import subprocess


# NOTE: ALL BEHAVIOUR ASSUMES THAT THIS SCRIPT MUST BE LOCATED IN PROJECT'S TOPLEVEL FOLDER
# NEXT TO manage.py

# TOFIX: need to shift to geo imports when auto creating admin.py and urls.py









###########
def cmd_manage(*args):
    sys.argv = list(args)
    sys.argv.insert(0, "manage.py")
    cmdstring = " ".join(sys.argv)
    print cmdstring
    return subprocess.check_output(cmdstring, shell=True, stderr=subprocess.STDOUT)

def cmd_admin(*args):
    import django
    djangopath = os.path.split(django.__file__)[0]
    adminpath = os.path.join(djangopath, "bin", "django-admin.py")
    sys.argv = list(args)
    sys.argv.insert(0, adminpath)
    cmdstring = " ".join(sys.argv)
    print cmdstring
    return subprocess.check_output(cmdstring, shell=False, stderr=subprocess.STDOUT)






############

def prereq():
    import pipy
    pipy.install("django-toolbelt")
    pipy.install("psycopg2")
    pipy.install("whitenoise")
    pipy.install("django-leaflet")
    pipy.install("django-geojson")








class DjangoSite(object):

    def __init__(self, sitepath=None):
        if not sitepath:
            sitepath = os.path.split(__file__)[0]
            
        self.path = sitepath
        self.name = os.path.split(self.path)[1]

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" %self.name)
            





    ############

    def __getattr__(self, appname):
        """Accesses any sub app as an object"""
        return DjangoApp(appname) 
            
            




    ############

    def setup(self):
        # BELOW COMMENTS ARE OLD
        # TODO: maybe switch away from the heroku template,
        # instead manually write procfile, requirements.txt, runtime.txt,
        # DATABASES = dj_database_url()...
        # DATABASES["BACKEND"] = postgresgeodb...
        # also
        # STATIC ADDON
        # also
        # WSGI WITH WHITENOISE...
        # maybe also
        # add static folder
        # ...
        
        sys.argv = [r"C:\Python27\Lib\site-packages\django\bin\django-admin.py",
                    "startproject",
                    self.name,
                    "&pause"]
        os.system(" ".join(sys.argv))

        # custom edit some settings
        # maybe also add some basic leaflet settings, incl installing it during setup
        # ...
        with open("%s/%s/settings.py"%(self.name,self.name), "a") as writer:
            writer.write("""

#### CUSTOMIZATIONS ####

INSTALLED_APPS = list(INSTALLED_APPS)

# geo enable
import dj_database_url
DATABASES['default'] =  dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
if "NAME" not in DATABASES['default']:
    DATABASES['default']["NAME"] = os.path.split(BASE_DIR)[-1]
if "USER" not in DATABASES['default']:
    DATABASES['default']["USER"] = "postgres"
INSTALLED_APPS.append('django.contrib.gis')

# add root template
TEMPLATES[0]['DIRS'].append(os.path.join(BASE_DIR, '%s', "templates"))

# add static
STATIC_ROOT = "static"
STATIC_URL = "/static/"
## STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATICFILES_STORAGE = "whitenoise.django.GzipManifestStaticFilesStorage"

# add leaflet
INSTALLED_APPS.append('leaflet')
LEAFLET_CONFIG = {
                'SPATIAL_EXTENT': (-180, -90, 180, 90),
                "TILES": [
                        ('osm', 'http://a.tile.openstreetmap.org/{z}/{x}/{y}.png', {"noWrap":True}),
                        ('light', 'http://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {"noWrap":True}),
                        ('dark', 'http://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {"noWrap":True}),
                        ('watercolor', 'http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.png', {"noWrap":True}),
                        ],
                }

""" % self.name )

        os.makedirs("%s/%s/templates/%s"%(self.name,self.name,self.name))
        with open("%s/%s/templates/%s/base.html"%(self.name,self.name,self.name), "a") as writer:
            # add default base template with topmenu...
            writer.write("""

<!DOCTYPE html>
<html>

    <head>
        <title>Welcome to the {SITENAME} site</title>
    </head>

    <body>
	<div class="page-header" style="background-color: #ff9400; margin-top: 0; padding: 20px 20px 20px 40px; font-family: comic sans relief;">
    		<h1 style="color:white">
		Welcome to the {SITENAME} site
		</h1>
    		<h2 style="color:white">
		<em>- Some subtitle...</em>
		</h2>
	</div>

	<div class="topmenu" style="background-color: black; font-family: comic sans relief;">
	<a href="/" style="color: white;">Home</a>
        <a href="/admin/" style="color: white;">Admin</a>
	</div>

	<br><br>

	<div class="content">
	{{% block content %}}
	{{% endblock %}}
	</div>

    </body>

</html>

""".format(SITENAME=self.name))
    
        os.mkdir("%s/%s/static"%(self.name,self.name))
        with open("%s/%s/static/dummy.txt"%(self.name,self.name), "a") as writer:
            pass

        with open("%s/%s/wsgi.py"%(self.name,self.name), "a") as writer:
            writer.write("""

from whitenoise.django import DjangoWhiteNoise
application = DjangoWhiteNoise(application)

""")

        # create default frontpage
        with open("%s/%s/urls.py"%(self.name,self.name), "a") as writer:
            writer.write("""
from django.shortcuts import render

def index(request):
    return render(request, '{SITENAME}/base.html')

urlpatterns.append(url('^$', index))

""".format(SITENAME=self.name))

        # prep for heroku web hosting
        with open("%s/Procfile"%self.name, "w") as writer:
            writer.write("web: gunicorn %s.wsgi"%self.name)

        with open("%s/requirements.txt"%self.name, "w") as writer:
            writer.write("""
Django==1.9
dj-database-url==0.3.0
dj-static==0.0.6
gunicorn==19.1.1
psycopg2==2.5.1
static==0.4
wsgiref==0.1.2
whitenoise==2.0.6
""")

        with open("%s/runtime.txt"%self.name, "w") as writer:
            writer.write("python-%s"%sys.version.split()[0])

        # script for testing site on local server
        with open("%s/testserver.py"%self.name, "w") as writer:
            writer.write("""
import sys,os

sys.argv = ["manage.py", "runserver", "&pause"]
os.system(" ".join(sys.argv))
""")





    ############

    def new_db(self):
        # create the db
        import psycopg2
        print("To create a new database for your project, login as a valid user")
        user = raw_input("username:\n")
        password = raw_input("password:\n")
        con = psycopg2.connect(dbname="postgres",
                               user=user,
                               password=password)
        con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        
        curs = con.cursor()
        curs.execute('CREATE DATABASE %s;' % self.name)

        curs.close()
        con.close()

        # add postgis extension
        con = psycopg2.connect(dbname=self.name,
                               user=user,
                               password=password)
        con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        
        curs = con.cursor()
        curs.execute('CREATE EXTENSION POSTGIS;')

        curs.close()
        con.close()
        
        # create data tables in db (makemigration) or manually
        sys.argv = ["manage.py", "makemigrations"]#, "--settings=%s.settings" %self.name]
        print sys.argv
        os.system(" ".join(sys.argv)+" &pause")

        sys.argv = ["manage.py", "migrate"]#, "--settings=%s.settings" %self.name]
        print sys.argv
        os.system(" ".join(sys.argv)+" &pause")

        # create website superuser
        sys.argv = ["manage.py", "createsuperuser"]#, "--settings=%s.settings" %self.name]
        os.system(" ".join(sys.argv)+" &pause")






    ###########
    
    def clear_db(self):
        # create data tables in db (makemigration) or manually
        sys.argv = ["manage.py", "flush"]#, "--settings=%s.settings" %self.name]
        print sys.argv
        os.system(" ".join(sys.argv)+" &pause")






    ###########
    
    def update_db(self):
        # create data tables in db (makemigration) or manually
        sys.argv = ["manage.py", "makemigrations"]#, "--settings=%s.settings" %self.name]
        print sys.argv
        os.system(" ".join(sys.argv)+" &pause")

        sys.argv = ["manage.py", "migrate"]#, "--settings=%s.settings" %self.name]
        print sys.argv
        os.system(" ".join(sys.argv)+" &pause")







    ###########

    def new_app(self, appname):
        
        # python manage.py runserver
        sys.argv = ["manage.py", "startapp", appname, #"--settings=%s.settings" %self.name,
                    "&pause"]
        #management.execute_from_command_line(sys.argv)
        os.system(" ".join(sys.argv))

        # add app specific templates
        os.makedirs("%s/templates/%s"%(appname,appname))
        with open("%s/templates/%s/%s.html"%(appname,appname,appname), "a") as writer:
            writer.write("""
{{% extends '{SITENAME}/base.html' %}}

{{% block content %}}

	<div>
        Insert html or template content here...
        </div>
        
{{% endblock %}}
""".format(SITENAME=self.name))

        # add app specific static folder
        os.mkdir("%s/static"%appname)
        with open("%s/static/dummy.txt"%appname, "a") as writer:
            pass

        # register app to site
        with open("%s/settings.py"%self.name, "a") as writer:
            writer.write("""

INSTALLED_APPS.append('%s')

""" % appname)
        






    ###########

    def testserver(self):
        
        # python manage.py runserver
        sys.argv = ["manage.py", "runserver", #"--settings=%s.settings" %self.name,
                    "&pause"]
        #management.execute_from_command_line(sys.argv)
        os.system(" ".join(sys.argv))







###########
class DjangoApp(object):

    def __init__(self, appname, sitepath=None):

        if not os.path.lexists(appname):
            raise Exception("No such app")
        
        self.name = appname
        self.siteobj = DjangoSite(sitepath)

    def __getattr__(self, attr):
        """Gets any app submodule and returns its variables as a dict for inspection"""

        class dict_as_obj:
            def __init__(self, dictdef):
                self.__dict__ = dictdef.copy()

        exec("import %s.%s as tempimport" %(self.name,attr) )

        return dict_as_obj(tempimport.__dict__)
    
    def define_geodata(self, path, modelname=None):
        # FIND WAY TO UPDATE EXISTING MODELS, OTHERWISE REPEAT DEFS LEAD TO ERROR
        
        # autogenerate the model and mapping definition for data source
        if not modelname:
            modelname = os.path.splitext(os.path.split(path)[1])[0]

        mappingdef = cmd_manage("ogrinspect",
                                '"'+path+'"', # path to geodata
                                modelname, # model name
                                "--mapping",
                                "--multi-geom",
                                )

        # write the generated python code by appending to existing models.py
        with open("%s/models.py"%self.name, "a") as writer:
            writer.write("\n"+mappingdef)

        # register the new model in the db
        self.siteobj.update_db()

    def load_geodata(self, path, modelname=None, encoding="utf8"):

        # autogenerate the model and mapping definition for data source
        print 99,modelname
        if not modelname:
            modelname = os.path.splitext(os.path.split(path)[1])[0]
        print 99,modelname
        
        # finally populate the new model to the db from the filesource
        # that would be the layermapping stuff:
        # (dont make load.py file as recommended, as it will only be needed this once)
        from django.contrib.gis.utils import LayerMapping

        modelobj = getattr(self.models, modelname)
        modelobj_mapping = getattr(self.models, modelname.lower()+"_mapping")

        lm = LayerMapping(modelobj, "%s"%path, modelobj_mapping,
                          transform=False, encoding=encoding)

        lm.save(strict=True, verbose=False)










###########

import tk2


class DjangoWidget(tk2.Frame):

    def __init__(self, master):
        tk2.Frame.__init__(self, master)

        # ...


class SiteWidget(tk2.Frame):

    def __init__(self, master, sitepath=None):
        tk2.Frame.__init__(self, master)

        # settings
        self.siteobj = DjangoSite(sitepath=sitepath)

        # header
        _row = tk2.Frame(self)
        _row.pack(fill="x")
        self.header = tk2.Label(_row, text="Django Site Manager",
                                font=("Cambria", 8))
        self.header.pack(side="left")
        
        _row = tk2.Frame(self)
        _row.pack(fill="x")
        self.projname = tk2.Label(_row, text="Project: %s" % self.siteobj.name,
                                font=("Cambria", 16))
        self.projname.pack()

        #### commands
        _butframe = tk2.Frame(self, text="Commands")
        _butframe.pack(fill="both", expand=1, padx=6, pady=6)

        # clear db button
        _row = tk2.Frame(_butframe)
        _row.pack(fill="x")
        self.createbut = tk2.Button(_row,
                                  text="Create DB",
                                  command=self.siteobj.new_db)
        self.createbut.pack()

        # clear db button
        _row = tk2.Frame(_butframe)
        _row.pack(fill="x")
        self.clearbut = tk2.Button(_row,
                                  text="Clear DB",
                                  command=self.siteobj.clear_db)
        self.clearbut.pack()

        # sync db button
        _row = tk2.Frame(_butframe)
        _row.pack(fill="x")
        self.syncbut = tk2.Button(_row,
                                  text="Sync DB",
                                  command=self.siteobj.update_db)
        self.syncbut.pack()

        # test site button
        _row = tk2.Frame(_butframe)
        _row.pack(fill="x")
        self.testbut = tk2.Button(_row,
                                  text="Test",
                                  command=self.siteobj.testserver)
        self.testbut.pack()

        #### apps (only those in defined inside the project folder that are actually yours)
        _appsframe = tk2.Frame(self, text="Site Apps")
        _appsframe.pack(fill="both", expand=1, padx=6, pady=6)

        def newappwin():
            newwin = tk2.Window()
            _row = tk2.Frame(newwin)
            _row.pack(fill="x")
            header = tk2.Label(_row, text="Enter name of new app")
            header.pack()
            _row = tk2.Frame(newwin)
            _row.pack(fill="x")
            newappname = tk2.Entry(_row)
            newappname.pack(side="left")
            def accept():
                self.siteobj.new_app(newappname.get())
                newwin.destroy()
            okbut = tk2.Button(_row, text="Create App", command=accept)
            okbut.pack(side="right")

        _row = tk2.Frame(_appsframe)
        _row.pack(fill="x")        
        self.newappbut = tk2.Button(_row,
                                    text="+++",
                                    command=newappwin
                                    )
        self.newappbut.pack()

        installed_apps = self.siteobj.pshapes_site.settings.INSTALLED_APPS
        for appname in os.listdir(os.path.abspath("")):
            if appname in installed_apps:
                print appname
                _row = tk2.Frame(_appsframe)
                _row.pack(fill="x")
                
                _app = tk2.Button(_row, text=appname)
                def commandfunc(appname=appname):
                    newwin = tk2.Window()
                    appwidg = AppWidget(newwin, appname)
                    appwidg.pack()
                _app["command"] = commandfunc
                _app.pack()


        # new app button
        _row = tk2.Frame(_butframe)
        _row.pack(fill="x")


class AppWidget(tk2.Frame):

    def __init__(self, master, appname, sitepath=None):
        tk2.Frame.__init__(self, master)
        
        # settings
        self.appobj = DjangoApp(appname, sitepath)

        # header
        _row = tk2.Frame(self)
        _row.pack(fill="x")
        self.header = tk2.Label(_row, text="Django App Manager",
                                font=("Cambria", 8))
        self.header.pack(side="left")
        
        _row = tk2.Frame(self)
        _row.pack(fill="x")
        self.appname = tk2.Label(_row, text="App: %s" % self.appobj.name,
                                font=("Cambria", 16))
        self.appname.pack()

        # commands
        _butframe = tk2.Frame(self, text="Commands")
        _butframe.pack(fill="both")

        # define geodata button
        _row = tk2.Frame(_butframe)
        _row.pack(fill="x")
        def defacceptfile(path):
            self.appobj.define_geodata(path)
        self.defdatabut = tk2.Button(_row, text="Define geodata",
                                      command=lambda: defacceptfile(tk2.filedialog.askopenfilename())
                                      )
        self.defdatabut.bind_dnddrop(lambda event: defacceptfile(event.data[0]),
                                      "Files")
        self.defdatabut.pack()

        # load geodata button
        _row = tk2.Frame(_butframe)
        _row.pack(fill="x")
        def loadacceptfile(path):
            self.appobj.load_geodata(path)
        self.loaddatabut = tk2.Button(_row, text="Load geodata",
                                      command=lambda: loadacceptfile(tk2.filedialog.askopenfilename())
                                      )
        self.loaddatabut.bind_dnddrop(lambda event: loadacceptfile(event.data[0]),
                                      "Files")
        self.loaddatabut.pack()


class ManageGUI(object):
    
    def __init__(self):
        # main
        self.window = tk2.Tk()

        # site commands
        siteframe = SiteWidget(self.window)
        siteframe.pack()

    def run(self):
        self.window.mainloop()



###########

if __name__ == "__main__":
    
    ManageGUI().run()



