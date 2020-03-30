from os.path import dirname, join, realpath

PROJECT = "DemoWebApp"
CONFIG_NAME = __name__
import pathlib

CONFIG_FILE_PATH = pathlib.Path(__file__)
VERBOSE = False
USE_LOGGING = True

# class Config(object):
#  pass

UPLOAD_FOLDER = join(
    dirname(realpath(__file__)), "uploads"
)  # where uploaded files are stored

ALLOWED_EXTENSIONS = {"png", "PNG", "jpg", "JPG", "jpeg", "JPEG", "gif", "GIF"}
