from PIL import Image, ImageFilter

im = Image.open('A.png', 'RGB')
im = im.filter(ImageFilter.FIND_EDGES)
im.save('edge.png')
