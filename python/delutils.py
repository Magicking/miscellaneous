#!/usr/bin/python

import os
import functools

PATH = '/mnt/crypted/transmission/downloads'
percent     = 50

svfs = os.statvfs(PATH)
threshold     = (svfs.f_blocks * percent) // 100.
actual        = svfs.f_blocks - svfs.f_bavail

l  = []
for v in os.walk(PATH):
  for w in v[2]:
    s = "%s/%s" % (v[0], w)
    st = os.stat(s)
    l.append((st.st_mtime, s))

l.sort(key=functools.cmp_to_key(lambda x,y: x[0] - y[0]))

for i in l:
  if threshold <= actual:
    svfs = os.statvfs(PATH)
    actual = svfs.f_blocks - svfs.f_bavail
    if i[1][0] == '.':
      continue
    print("Deleting %s. %d / %d" % (i[1], threshold / svfs.f_blocks * 100, actual / svfs.f_blocks * 100))
    os.remove(i[1])
  else:
    break

os.system("touch %s/.notempty" % PATH)
os.system("find %s -empty -delete" % PATH)
