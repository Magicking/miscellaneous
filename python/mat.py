from PIL import Image
from multiprocessing import Pool
from io import BytesIO

img1p = '1.jpg'
img2p = '2.jpg'
imgo  = 'out.png'

kn1 = [[0.13, 0.13, 0.13],
       [0.13, 1.0, 0.13],
       [0.13, 0.13, 0.13]]

kn2 = [[0.09, 0.09, 0.09],
       [0.09, 0.09, 0.09],
       [0.00, 0.00, 0.00]]
img1 = open(img1p)
im1 = BytesIO(img1.read())
img1.close()
im1.seek(0)
img2 = open(img2p)
im2 = BytesIO(img2.read())
img2.close()
im2.seek(0)
im1 = Image.open(im1)
im2 = Image.open(im2)

if im1.size != im2.size and im1.mode != im2.mode and im1.mode != 'RGB':
   exit()

imo = Image.new(im1.mode, im1.size)
xe, ye = im1.size

def kn_apply((x, y)):
  R, G, B = (0, 0, 0)
  for xi in range(3):
    for yi in range(3):
      if   0 <= x + xi - 1 and x + xi - 1 < im1.size[0]:
        if 0 <= y + yi - 1 and y + yi - 1 < im1.size[1]:
          pix1 = im1.getpixel((x + xi - 1, y + yi - 1))
          pix2 = im2.getpixel((x + xi - 1, y + yi - 1))
          R += pix1[0] * kn1[xi][yi] + pix2[0] * kn2[xi][yi] 
          G += pix1[1] * kn1[xi][yi] + pix2[1] * kn2[xi][yi]
          B += pix1[2] * kn1[xi][yi] + pix2[2] * kn2[xi][yi]
  R /= 2
  G /= 2
  B /= 2
  return ((x, y), (int(R), int(G), int(B)))

pool = Pool()

last_perc = 0
for x in range(xe):
  pix_list = pool.map(kn_apply, [(x, y) for y in range(ye)])
  for coord, pix  in pix_list:
    imo.putpixel(coord, pix)
    perc = int(x * 100 / xe)
    if perc != last_perc:
      print("%02d%%" % last_perc)
      last_perc = perc
imo.save(imgo, 'PNG')
