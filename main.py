#! coding=utf-8

import datetime, smtplib, imp, os
from email.mime.text import MIMEText

import requests
from git import Repo
from git.errors import *
from unipath import Path
from jinja2 import Template

# Local settings are stored in $HOME/.ometrics/settings.py
# Find and load module there, creating files/dirs where appropriate
om = Path( os.environ['HOME'] ).absolute().child('.ometrics')
om.mkdir()
module_path = om.absolute()
if not om.child('settings.py').exists():
    print('Copying setitngs.py into %s' % str(om.child('settings.py')))
    Path(__file__).parent.child('settings.py').copy(om.child('settings.py'))
imp.load_source('settings', module_path.child('settings.py'))

from settings import *

from template import HTML_MAIL



now = datetime.datetime.utcnow()
gap = datetime.timedelta(days=INTERVAL_DAYS)
begins = now - gap

BT_CSS = requests.get('http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css').text

def contains_git(fs_path):
    return fs_path.child('.git').exists()


class Data:
    pass

def gen_change_str(change_dict):
        if USE_HTML:
            tpl_obj = []
            for repo in change_dict:
                commits = change_dict[repo]
                obj = Data()
                obj.repo = str(repo).split('"')[1]
                obj.n_commits = len(commits)
                obj.n_inserts = sum([commits[c]['inserts'] for c in commits])
                obj.n_deletes = sum([commits[c]['dels'] for c in commits])
                tpl_obj.append(obj)
            t = Template(unicode(HTML_MAIL))
            return t.render(
                bt_css=BT_CSS,
                title = 'SUMMARY OF GIT ACTIVITIES FROM %s to %s' % (str(begins.date()), str(now.date())),
                tpl_obj = tpl_obj
            )
        else:
            s = []
            for repo in change_dict:
                s.append('--')
                s.append(str(repo))
                commits = change_dict[repo]
                s.append('%i commits' % len(commits))
                s.append('%i inserts total' % sum([commits[c]['inserts'] for c in commits]))
                s.append('%i deletions total' % sum([commits[c]['dels'] for c in commits]))
            return '\n'.join(s)


def send_mail(title, body):
    type = 'html' if USE_HTML else 'plain'
    msg = MIMEText(body, type)
    msg['Subject'] = title
    msg['From'] = EMAIL_SETUP['username']
    msg['To'] = REPORT_EMAIL_TO
    s = smtplib.SMTP(EMAIL_SETUP['smtp'], EMAIL_SETUP['port'])
    s.ehlo()
    s.starttls()
    s.login(EMAIL_SETUP['username'], EMAIL_SETUP['password'])
    s.sendmail(EMAIL_SETUP['username'], [REPORT_EMAIL_TO], msg.as_string())
    s.close()
    print('Report successfully sent to %s' % REPORT_EMAIL_TO)


def gen_commit_dict(commit):
    files = commit.stats.files
    changes = 0
    inserts = 0
    dels = 0
    for f in files:
        changes += files[f]['lines']
        inserts += files[f]['insertions']
        dels += files[f]['deletions']
    if changes:
        return dict(
            changes=changes,
            inserts=inserts,
            dels=dels
        )
    else:
        return {}


# ----- Main script begins here -----------

for root in GIT_DIRS:
    p = Path(root)
    change_dict = {}
    for gitdir in p.walk(filter=contains_git):
        repo = Repo(str(gitdir.absolute()))
        try:
            s = '%i-%i-%i' % (begins.year, begins.month, begins.day)
            for commit in repo.commits_since(since=s):
                if commit.author.email.lower() not in GIT_AUTHOR_EMAILS:
                    continue
                cd = gen_commit_dict(commit)
                if cd:
                    if repo not in change_dict:
                        change_dict[repo] = {}
                    change_dict[repo][commit] = cd
        except (GitCommandError, AttributeError) as e:
            pass
    if change_dict:
        title = 'SUMMARY OF GIT ACTIVITIES FROM %s to %s' % (str(begins.date()), str(now.date()))
        body = gen_change_str(change_dict)
        send_mail(title, body)
            


