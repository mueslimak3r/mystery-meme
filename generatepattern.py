import random

from PIL import Image

from imageviewer import view_image_object


def generate_pattern(seed, width, height, datasize):

    image = Image.new("1", (width, height))

    mask = [0] * width * height

    random.seed(seed)
    for _ in range(datasize * 2):
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        image.putpixel((x, y), 1)
        mask[(y * width) + x] = 1

    '''
    for y in range(image.height):
        for x in range(image.width):
            image.putpixel((x, y), mask[(y * width) + x])
    '''

    image = image.convert('RGB')
    mode = image.mode
    size = image.size
    data = image.tobytes()

    view_image_object(data, size, mode)
    return mask

if __name__ == "__main__":
    generate_pattern(42, 500, 500, 1000)