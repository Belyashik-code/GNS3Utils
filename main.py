import gns3apimanagement.gns3apimanagement as gns
import json
import re
import tarfile
import bz2
import paramiko
import shutil
import config
import os
import argparse
import time
import subprocess
import sys
from flask import Flask
app = Flask(__name__)
import web_app.routes as routes


# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/
# preparing step

# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/
# running script step

# получение полного пути до папки с файлом main.py
path_root = f'{os.path.abspath(os.path.dirname(sys.argv[0]))}'


# инсталяция необходимых pip

# /-/-/-/-/-/-/-/-/-/-/-/-/-/-/

