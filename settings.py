#! coding=utf-8

# tuple of directories where git repos are scanned for.
# all subdirectories will be examined as well.
GIT_DIRS = ('~', )

# tuple of emails
# Any git commits whose author is not listed here
# will be excluded from the generated report
GIT_AUTHOR_EMAILS = ('', )

# Stats will be generated for all commits
# backdating this many days
INTERVAL_DAYS = 14

# email address to send report to
REPORT_EMAIL_TO = ''

# True if HTML mail is to be used.
# Set it to false if you want plain-text email.
USE_HTML = True

# Use your email provider of choice
EMAIL_SETUP = {
    'smtp': 'smtp.gmail.com',
    'port': 587,
    'username': 'your username',
    'password': 'your password'
}
