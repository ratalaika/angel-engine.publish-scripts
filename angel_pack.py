#!/usr/bin/env python

import sys
import os
import subprocess
import time
import math
import json
import shutil

if (sys.platform[:3] == 'win'):
    timer = time.clock
else:
    timer = time.time

start = timer()

# a simple way to execute quietly
def do_quietly(exec_array):
    subprocess.call(exec_array, stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)

def get_quietly(exec_array):
    return subprocess.Popen(exec_array, stdout=subprocess.PIPE).communicate()[0]

# load configuration data
DISTRO_CONFIG_FILENAME = "pub_config.json"
config_data_file = open(DISTRO_CONFIG_FILENAME, "r")
config_data = config_data_file.read()
config_data_file.close()
config = json.loads(config_data)
FILENAME = "%s%s" % (config["base_name"], sys.argv[1])
REPO = config["repository"]

# get a clean version of the latest code
if not os.path.exists(FILENAME):
    print "Exporting code..."
    do_quietly(['hg', 'clone', REPO, FILENAME])

# zip, clean up original
print "\tFull Distro:"
print "\t\tZipping..."
shutil.move(os.path.join(FILENAME, ".hg"), "TEMPHG")
shutil.move(os.path.join(FILENAME, ".hgtags"), "TEMPHGTAGS")
do_quietly(['zip', '-r9', FILENAME + ".zip", FILENAME])
shutil.move("TEMPHG", os.path.join(FILENAME, ".hg"))
shutil.move("TEMPHGTAGS", os.path.join(FILENAME, ".hgtags"))
if not os.path.exists(config["output_dir_name"]):
    os.mkdir(config["output_dir_name"])
do_quietly(['mv', FILENAME + ".zip", os.path.join(config["output_dir_name"], FILENAME + ".zip")])

# script timer
finish = timer()
seconds = finish - start
minutes = 0
if seconds >= 60:
    minutes = seconds / 60
    seconds = seconds % 60
print "\n\nScript took %i:%02d." % (minutes, seconds)

# # resulting file sizes
# print "File sizes:"
# # distros = list(config["distros"].iterkeys())
# distros = list()
# distros.insert(0, "")
# for dist in distros:
#     if len(dist) > 0:
#         dist_zip = FILENAME + "-" + dist + ".zip"
#     else:
#         dist_zip = FILENAME + ".zip"
#     size_string = "\t" + dist_zip
#     if len(dist) > 0:
#         size_string += "\t\t"
#     else:
#         size_string += "\t\t\t"
#     file_size = os.path.getsize(dist_zip)
#     units = ["bytes", "KB", "MB", "GB", "TB"]
#     if file_size < 1024:
#       size_string += "%i %s" % (file_size, units[0])
#     else:
#         max_exp = len(units) - 1
#         file_size = float(file_size)
#         exponent = int(math.log(file_size) / math.log(1024))
#         if exponent > max_exp:
#             exponent = max_exp
#         file_size /= 1024 ** exponent
#         size_string += "%.1f %s" % (file_size, units[exponent])
#     print size_string

