from base import *

TEMPLATE_DIRS = ('/home/chris/peaches/hoops/hoops/templates',)
TEMPLATE_DEBUG=True

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    '/var/www/static/',
)
