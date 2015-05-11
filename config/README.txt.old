------------------------------------------------------------------------------
INFORMATION ABOUT THE CONFIG FILE TRANSFER SETUP FOR THE SUMMARY PAGES
------------------------------------------------------------------------------
Max Isi - misi@ligo.caltech.edu
Updated: Nov 17, 2014

Rana - May 10, 2015
------------------------------------------------------------------------------

The contents of this directory:
/cvs/cds/caltech/chans/GWsummaries/
are synced to LDAS so that they can be used to generate the 
detector summary pages using the gwsumm package (https://github.com/gwpy/gwsumm).

All files with the '.ini' extension will be uploaded, no matter what
subdirectory they are in. In fact, the code completely ignores subdirectory
structure. This means you can organize the files as you wish without altering
the output.

The code determines what IFO the config files corresponds to by looking at the
prefix of the file name. For example, 'c1-lsc.ini' will be used when creating
C1 summaries, but ignored otherwise. Files with the prefix 'all-' will be used
for all IFOs. A special case is the 'defaults.ini' file, which contains HTML
and other general information. Although this file is always loaded, its
settings can be overwritten by custom files (e.g. if the same property is
defined in 'defaults.ini' and 'c1-lsc.ini', the latter will take precedence).

The remote LDAS folder mirrors the local nodus one. Version control is
implemented in the remote folder by means of a Git repository. If you want to 
revert to a previous version of a config file, you can let me know or go to
https://github.com/maxisi/summary/tree/master/config and replace the file
yourself. Note that changes that have not been synced to LDAS will NOT be
backed up.

For information on the INI format itself see: 
https://ldas-jobs.ligo.caltech.edu/~duncan.macleod/gwsumm/latest/

Pages URLs:

OLD, obsolete location
C1 : https://ldas-jobs.ligo.caltech.edu/~max.isi/summary/day/20141117/

NEW (as of May 5)
https://nodus.ligo.caltech.edu:30889/detcharsummary/
