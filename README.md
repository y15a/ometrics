ometrics
========

Quantify how much you code.

ometrics has been started with a simple goal of monitoring how much you code - regardless of what project you are working on right now. Its core operations are:

1. Scan pre-defined directories for git repositories
2. Looks for recent commits
3. Compiles stats
4. Send report via Email


Usage
--------

    $ # do all the settings, then,
    $ python main.py


Settings
--------------
Note that settings.py contained in the repository is merely a template. When ometrics is first run on your system, .ometrics directory is created under $HOME where settings.py is copied into. ometrics will refer to settings.py in that directory.

Current options are:

* _GIT_DIRS_ - Tuple containing paths to directories, under which git repos are scanned for.
* _GIT_AUTHOR_EMAILS_ - Tuple containig email address of the authors. Set this to your own emails to filter out all commits made by your teammates.
* _INTERVAL_DAYS_ - Number of dates ometrics goes back to collect the statistics. Default value is 14 (two weeks).
* _REPORT_EMAIL_TO_ - String containing email address where report is sent to.
* _USE_HTML_ - Boolean value denoting whether HTML email is used or not. HTML version is styled using Twitter Bootstrap. Default is True.
* _EMAIL_SETUP_ - A dict containing connection & authentication details for the SMTP server of your choice.


Requirements
---------------
GitPython, Jinja2, Unipath, requests. For version info see requirements.txt