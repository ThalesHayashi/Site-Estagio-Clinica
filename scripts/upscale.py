from PIL import Image
import os
src = os.path.join('public','1718225436654_Easy-Resize.com.jpg')
if not os.path.exists(src):
    print('SOURCE_MISSING', src)
else:
    img = Image.open(src)
    w,h = img.size
    target = 1200
    # Make square by padding if necessary
    size = max(w,h)
    # create white background
    square = Image.new('RGB',(size,size),(255,255,255))
    square.paste(img, ((size-w)//2, (size-h)//2))
    # resize to target
    up = square.resize((target,target), Image.LANCZOS)
    out_jpg = os.path.join('public','470218448_474803038963147_8631634616631528250_n_2x.jpg')
    up.save(out_jpg, quality=90)
    out_webp = os.path.join('public','470218448_474803038963147_8631634616631528250_n_2x.webp')
    up.save(out_webp, format='WEBP', quality=90)
    print('SAVED', out_jpg, out_webp)
