import inspect
import os

# Directory containing this file
this_dir = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))


def relative_path(path):
    return "{0}/{1}".format(this_dir, path)
