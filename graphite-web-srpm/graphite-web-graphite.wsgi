import sys
# In case of multi-instance graphite, uncomment and set appropriate name
# import os
# os.environ['GRAPHITE_SETTINGS_MODULE'] = 'graphite.local_settings'
sys.path.append('/usr/share/graphite/webapp')

from graphite.wsgi import application
