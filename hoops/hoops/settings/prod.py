from base import *

TEMPLATE_DIRS = ('/var/www/peaches/hoops/hoops/templates',)
TEMPLATE_DEBUG=True

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    '/var/www/static/',
)
STATIC_ROOT = '/var/www/peaches/static'
