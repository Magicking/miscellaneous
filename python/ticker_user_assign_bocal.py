#!/usr/bin/python
# coding=utf-8

import urllib2
import re
import time
import sys
import htmlentitydefs
import urllib
import hashlib

if len(sys.argv) != 2:
    print "ticket.py subject"
    sys.exit(-1)

body = ""
for line in sys.stdin:
    body += line

f = urllib2.Request("https://intra-bocal.epitech.net/")
f.add_header("User-Agent","PyPOST")
f.add_header("Accept","*/*")

login = "lauren_e"
mdp = "CHANGEME"
master_t = "0"

ret = urllib2.urlopen(f)
ret.read()
dict_cookies = ret.info()
phpsesid = 'PHPSESSID=' + re.search(r'PHPSESSID=(\w+);', dict_cookies['Set-Cookie']).group(1) + ';'

f = urllib2.Request("https://intra-bocal.epitech.net/index.php?pgid=homeprivate&m_menu_state=1")
f.add_header("User-Agent","PyPOST")
f.add_header("Accept","*/*")
f.add_header("Cookie", phpsesid);
f.add_data("login=%s&pass=%s" % (login, mdp));

ret = urllib2.urlopen(f)
ret.read()

f = urllib2.Request("https://intra-bocal.epitech.net/index.php?pgid=read&m_tickets_id=%s" % (master_t))
f.add_header("User-Agent","PyPOST")
f.add_header("Accept","*/*")
f.add_header("Cookie", phpsesid + "login=%s; pass=%s;" % (login, mdp))

ret = urllib2.urlopen(f)
buf = ret.read()

ts = re.search(r'm_tickets_ts_page" value=\'(\w+)\'', buf).group(1)

def postticket():
    f = urllib2.Request("https://intra-bocal.epitech.net/")
    f.add_header("User-Agent","PyPOST")
    f.add_header("Accept","*/*")
    f.add_header("Cookie", phpsesid + "login=%s; pass=%s;" % (login, mdp))
    buf = "m_tickets_id=%s&pgid=read&m_tickets_frame=print_ticket&m_tickets_ts_page=%s&m_tickets_userassign_%d=%s&m_tickets_subject=%s&m_tickets_content=%s&m_tickets_button_print_ticket_submit=Valider votre demande" % (master_t, ts, 26594, "lauren_e", urllib.quote(sys.argv[1]), urllib.quote(body))
#26594 lauren_e
    f.add_data(buf)
#    print buf
    print urllib2.urlopen(f).read()

postticket()
