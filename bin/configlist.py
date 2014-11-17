#! /usr/bin/python

import os
import sys

"""Crawl through configuration file directory and create list of INI files
in the format required for input into thw GWsumm processing code, gw_summary
"""

# prefix (IFO) should be first argument
prefix = sys.argv[1]

# determine configuration-file location
if len(sys.argv) == 2:
    rootdir = '/home/max.isi/summary/config'
elif len(sys.argv)>2:
    rootdir = sys.argv[2]

# loop over subdirectories and add paths to INI files to string
config_string = ''
for dir_name, subdir_list, file_list in os.walk(rootdir):
    for f_name in file_list:
        rightstart = f_name.startswith(prefix) or f_name.startswith('all')
        if f_name[-3:] == 'ini' and rightstart:
            config_string += ' --config-file ' + os.path.join(dir_name, f_name)

# write string to file
dest_dir = os.path.join(os.environ['TMPDIR'], 'summary/configstr.txt')
with open(dest_dir, 'w') as f:
    f.write(config_string)

print 'Configuration file parameters written: %s' % dest_dir
