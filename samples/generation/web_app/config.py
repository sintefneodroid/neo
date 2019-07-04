from os.path import dirname, join, realpath

PROJECT = 'DemoWebApp'
CONFIG_NAME = __name__
CONFIG_FILE = __file__
VERBOSE = False
USE_LOGGING = True

# class Config(object):
#  pass

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'uploads')  # where uploaded files are stored

ALLOWED_EXTENSIONS = {'png',
                      'PNG',
                      'jpg',
                      'JPG',
                      'jpeg',
                      'JPEG',
                      'gif',
                      'GIF'}
