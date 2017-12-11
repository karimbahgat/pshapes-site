import sys,os

sys.argv = ["manage.py", "runserver", "&pause"]
os.system(" ".join(sys.argv))
