import random

from PIL import Image

from imageviewer import view_image_object


def generate_pattern(seed, width, height, datasize):

    image = Image.new("1", (width, height))

    mask = [0] * width * height
    unique_pixel_counter = 0

    random.seed(seed)
    i = 0
    while i < datasize:
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        if mask[(y * width) + x] == 0:
            image.putpixel((x, y), 1)
            unique_pixel_counter += 1
            mask[(y * width) + x] = 1
            i += 1
            #print ("yielding at i: ", i, " x, y: ", x, y)
            yield x, y

    print("number of points in pattern: ", unique_pixel_counter)
    image = image.convert('RGB')
    mode = image.mode
    size = image.size
    data = image.tobytes()

    view_image_object(data, size, mode)
    image.close()
    return 0, 0