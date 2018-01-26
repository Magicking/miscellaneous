#!/usr/bin/python
# coding=utf-8

import httplib
import sys

if len(sys.argv) != 2:
  print 'Usage: ./postit.py PHPSESSID'
  exit(1)

phpsesid = 'PHPSESSID=%s;' % sys.argv[1]

def encode_multipart_formdata(fields, files):
  BOUNDARY = '----------cacaboundchevalchien!!'
  CRLF = '\r\n'
  L = []
  for (key, value) in fields.items():
    L.append('--' + BOUNDARY)
    L.append('Content-Disposition: form-data; name="%s"' % key)
    L.append('')
    L.append(value)
  for (filename, value) in files.items():
    L.append('--' + BOUNDARY)
    L.append('Content-Disposition: form-data; name="m_tickets_file_up"; filename="%s"' % filename)
    L.append('Content-Type: application/octet-stream')
    L.append('')
    L.append(value)
  L.append('--' + BOUNDARY + '--')
  L.append('')
  body = CRLF.join(L)
  content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
  return content_type, body

def post_multipart(fields, files):
  content_type, body = encode_multipart_formdata(fields, files)
  h = httplib.HTTPSConnection('intra-bocal.epitech.net')
  h.putrequest('POST', '/', False, True)
  h.putheader('User-Agent','PyPOST')
  h.putheader('Accept','*/*')
  h.putheader("Cookie", phpsesid)
  h.putheader('Content-Type', content_type)
  h.putheader('Content-Length', str(len(body)))
  h.endheaders()
  h.send(body)
  return h.getresponse().getheaders()

post_multipart({'m_tickets_id': '0', 'pgid': 'read',
                'm_tickets_frame': 'attachment', 'reopen': '1',
                'm_tickets_upload_file': 'Ajouter'},
               {'test.txt': 'x' * (1) })
#               {'test.txt': 'x' * (59*1024*1024) })
