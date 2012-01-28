#!/usr/bin/python
"""Set KnowledgeTree admin password

Option:
    --pass=  unless provided, will ask interactively # Not working yet
"""

from sys import stderr, argv, exit
from getopt import gnu_getopt, GetoptError
from hashlib import md5

from dialog_wrapper import Dialog
from mysqlconf import MySQL

def usage(s=None):
    if s:
        print >> stderr, "Error:", s
    print >> stderr, "Syntax: %s [options]" % argv[0]
    print >> stderr, __doc__
    exit(1)

def main():
    try:
        opts, args = gnu_getopt(argv[1:], "h",
                                       ['help', 'pass='])
    except GetoptError, e:
        usage(e)

    password = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "KnowledgeTree Password",
            "Enter new password for the KnowledgeTree 'admin' account")

    hashpass = md5(password).hexdigest()

    m = MySQL()
    m.execute('UPDATE dms.users SET password=\"%s\"  WHERE username=\"admin\";' % hashpass)

if __name__ == "__main__":
    main()
