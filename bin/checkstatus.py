#! /usr/bin/python

import os
import sys
from glob import glob
import datetime
from numpy import loadtxt
import subprocess

if len(sys.argv) == 2:
    logdir = os.path.abspath(sys.argv[1])
else:
    logdir = os.getcwd()

TODAY = datetime.datetime.utcnow().strftime('%Y-%m-%d')

# GET LOGS
filedict = {}
filesfound = 0
if os.path.isdir(logdir):
    pathmask = os.path.join(logdir, "gw_summary_pipe-*.out")
    print "Looking for files matching: %s." % pathmask
    # get all out log files
    for outfile in glob(pathmask):
        filename = os.path.basename(outfile)
        print("Checking %s. " % filename)
        fileid = filename.strip('gw_summary_pipe').strip('.out')
        tablist = []
        with open(outfile, 'r') as fout:
            lines = fout.readlines()
            # check file has the right date
            if lines[6].startswith("Start time") and lines[6].split()[2]:
                print("File is valid.\n")
                filesfound += 1
                # find tabs included in file
                for line in lines:
                    if line.startswith("Processing") \
                            and not line.endswith("state\n"):
                        tabname = line.strip("Processing ").split('/')[0]
                        tablist.append(tabname)
                tablist = set(tablist)

                # compose title
                tabstring = ''
                for tab in tablist:
                    tabstring += '%s/' % tab

                # add entry for file: first element tabs, second error message
                filedict[fileid] = [tabstring, '']
                # open corresponding err file
                errfile = os.path.join(logdir, "gw_summary_pipe%s.err" %
                                       fileid)
                with open(errfile, 'r') as ferr:
                    filedict[fileid][1] = ferr.read()
            else:
                print("File not valid.\n")
else:
    print "Log directory not found (%r)." % logdir

# GET STATUS: 0, alive; 1, dead; 2, maintenance.
codestatus = 1
STATUSPATH = os.path.join(os.environ['TMPDIR'], 'summary/', 'status')
try:
    manualstatus = loadtxt(STATUSPATH)
    print "Manual status code is %r." % manualstatus
except IOError:
    manualstatus = 0
    print "Manual status file not found: %r." % STATUSPATH
    
if manualstatus == 0:
    # check condor queue
    USER = os.environ['USER']
    cmd = subprocess.Popen('condor_q %s' % USER, shell=True,
                           stdout=subprocess.PIPE)
    for line in cmd.stdout:
        if "gw_daily_summary" in line:
            if line.split()[5] != 'H':
                codestatus = 0
                print "Condor job OK."
else:
    codestatus = 2

# WRITE HTML
if codestatus == 0:
    contentlines = [
        '<h2>Code status: '
        '<font color="green">alive</font></h2>\n',
        '<p>The code is currently running.</p>\n',
        '<p> If some of the plots are not dislaying correctly, check the '
        'status of the individual configuration files below to see if there '
        'are syntax errors (click on the "err" link to see the error message, '
        'if one was produced).</p>\n',
        '<p>If you still think something else is wrong,'
        ' <a href="mailito:misi@ligo.caltech.edu" target="_blank">report an '
        'issue</a>.</p>\n'
    ]
elif codestatus == 2:
    contentlines = [
        '<h2>Code status: '
        '<font color="orange">testing</font></h2>\n',
        '<p>The code is currently undergoing maintenance.</p>\n',
        '<p>While fixes are being implemented functionality might be reduced. '
        'However, this should be temporary. If you still think something is '
        'wrong, <a href="mailito:misi@ligo.caltech.edu" target="_blank">'
        'report an issue</a>.</p>\n'
    ]
else:
    contentlines = [
        '<h2>Code status: '
        '<font color="red">dead</font></h2>\n',
        '<p>The code is not currently running.</p>\n',
        '<p>Please, <a href="mailito:misi@ligo.caltech.edu" target="_blank">'
        'report this</a>.</p>\n'
    ]

contentlines += [
    '<h2>Configuration file status:</h1>\n',
    '<ul>\n',
]

for fileid, contents in filedict.iteritems():
    name = contents[0].strip('/')
    if name == '':
        name = "Unknown name"
    logurl = "logs/gw_summary_pipe%s.out" % fileid
    errurl = "logs/gw_summary_pipe%s.err" % fileid
    if contents[1] == '':
        filestatus = '<font color="green">OK</font>'
    else:
        filestatus = '<font color="red">ERROR</font>'
        # in the future, we can also show error message directly rather than
        # just linking to the error file.

    statusline = '<li>%s (<a href="%s" target="_blank">log</a>, ' \
                 '<a href="%s" target="_blank">err</a>): %s.</li>\n' \
                 % (name, logurl, errurl, filestatus)
    contentlines.append(statusline)

if filesfound == 0:
    contentlines.append("<li>No logs found.</li>\n")

contentlines.append("</ul>\n")

now = datetime.datetime.utcnow().strftime('%Y-%m-%d %X')
contentlines.append("<p>Last updated: %s.</p>" % now)

headerlines = [
    '<!DOCTYPE html>\n',
    '<html lang="en">\n',
    '<head>\n',
    '<meta content="width=device-width, initial-scale=1.0" name="viewport" />\n',
    '<link media="all" href="html/bootstrap.min.css" type="text/css" rel="stylesheet" />\n',
    '<link media="all" href="html/datepicker.css" type="text/css" rel="stylesheet" />\n',
    '<link media="all" href="html/fancybox/source/jquery.fancybox.css?v=2.1.5" type="text/css" rel="stylesheet" />\n',
    '<link media="all" href="html/gwsummary2.css" type="text/css" rel="stylesheet" />\n',
    '<link media="all" href="html/gw_L1.css" type="text/css" rel="stylesheet" />\n',
    '<title>IFO summary</title>\n',
    '<script src="html/jquery-1.10.2.min.js" type="text/javascript"></script>\n', '<script src="html/moment.min.js" type="text/javascript"></script>\n',
    '<script src="html/js/bootstrap.min.js" type="text/javascript"></script>\n', '<script src="html/bootstrap-datepicker.js" type="text/javascript"></script>\n',
    '<script src="html/fancybox/source/jquery.fancybox.pack.js?v=2.1.5" type="text/javascript"></script>\n', '<script src="html/gwsummary.js" type="text/javascript"></script>\n',
    '<base href="." />\n', '</head>\n',
    '<body>\n',
    '<div id="wrap">\n',
    '<div class="container" id="header">\n',
    '<div class="row">\n',
    '<div class="col-sm-12">\n',
    '<h1 class="inline-block">LIGO Caltech 40m Observatory status</h1>\n',
    '</div>\n',
    '</div>\n',
    '</div>\n',
    '<div id="nav-wrapper">\n',
    '<nav class="navbar" role="navigation" id="nav">\n',
    '<div class="container">\n', '<div class="row">\n',
    '<div class="col-md-12">\n', '<div class="navbar-header">\n',
    '<div class="btn-group pull-left">\n',
    '<a class="navbar-brand dropdown-toggle" data-toggle="dropdown" href="#">\n',
    'C1\n',
    '<b class="caret"></b>\n',
    '</a>\n',
    '<ul class="dropdown-menu">\n',
    '<li>\n',
    '<a class="ifo-switch" data-new-base="https://ldas-jobs.ligo.caltech.edu/~max.isi/summary">C1</a>\n',
    '</li>\n',
    '<li>\n',
    '<a class="ifo-switch" data-new-base="https://ldas-jobs.ligo.caltech.edu/~detchar/summary">L1</a>\n',
    '</li>\n',
    '<li>\n',
    '<a class="ifo-switch" data-new-base="https://ldas-jobs.ligo-wa.caltech.edu/~detchar/summary">H1</a>\n',
    '</li>\n',
    '</ul>\n',
    '</div>\n',
    '<a id="calendar" data-viewmode="0" title="Show/hide calendar" data-date-format="dd-mm-yyyy" class="navbar-brand dropdown-toggle">\n',
    'Calendar\n',
    '<b class="caret"></b>\n',
    '</a>\n',
    '<div class="btn-group pull-left">\n',
    '<a class="navbar-brand dropdown-toggle" id="today" style="padding-left: 20px;">Today</a>\n',
    '<a class="navbar-brand" id="yesterday" style="padding-left: 20px;">Yesterday</a>\n', '</div>\n',
    '</div>\n',
    '</div>\n',
    '</div>\n',
    '</div>\n',
    '</nav>\n',
    '</div>\n',
    '<div id="main" class="container">\n',
    '    <div class="row">\n',
    '    <div class="col-md-12">\n',
]

footerlines = [
    '    </div>\n',
    '    </div>\n',
    '</div>\n',
    '<script>\n',
    '   var today = moment().local();\n',
    "   var tday = today.format('YYYYMMDD');\n",
    "   $('#today').attr('href', 'day/' + tday);\n",
    "   var yday = today.subtract('days', 1).format('YYYYMMDD');\n",
    "   $('#yesterday').attr('href', 'day/' + yday);\n",
    '</script>\n',
    '</div>\n',
    '<footer>\n',
    '<div class="container">\n',
    '<div class="row">\n',
    '<div class="col-md-12">\n',
    '<a href="mailito:misi@ligo.caltech.edu" target="_blank">Report an issue</a>\n',
    '</div>\n',
    '</div>\n',
    '</div>\n',
    '</footer>\n',
    '<script>\n',
    '    $(document).ready(function() {\n',
    '        window.setInterval(refreshImage, 5*60*1000);\n',
    '    });\n',
    '</script>\n',
    '</body>\n',
    '</html>\n'
]

htmllines = headerlines + contentlines + footerlines

htmlpath = 'status.html'
with open(htmlpath, 'w') as f:
    for line in htmllines:
        f.write(line)
    print "HTML written to %r" % htmlpath 
