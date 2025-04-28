import math
from PIL import Image


def compare_images(image1, image2, tolerance=10):
    #check for sizes

    #DEBUG
    #print(image1.size)
    #print(image2.size)

    if not image1.size == image2.size:
        result = -1
        return result, "Images have different sizes.", None, None
    width, height = image1.size
    diff_image = Image.new('RGBA', (width, height), 'white')
    pixels1 = image1.load()
    pixels2 = image2.load()
    pixelsdiff = diff_image.load()
    result = 0
    wrong_pixels = 0
    for x in range(width):
        for y in range(height):
            #if not pixels1[x, y] == pixels2[x, y]:
            math_diff = map(lambda pix1, pix2: int(math.fabs(pix1-pix2)) > tolerance, pixels1[x, y], pixels2[x, y])
            if True in math_diff:
                result = 1
                wrong_pixels += 1
                pixelsdiff[x, y] = (255, 0, 0, 255)
    return result, "comparison done", diff_image, wrong_pixels


def compare_images_similarity(image1, image2, percentage):
    result, msg, diff_image, wrong_pixels = compare_images(image1, image2, tolerance=10)
    if result == -1:
        return result,  msg, None, None
    width, height = image1.size
    if float(width * height - wrong_pixels) / float(width * height) < float(percentage):
        result = 1
    else:
        result = 0
    return result, "comparison done", diff_image, wrong_pixels


def main():
    pass


if __name__ == "__main__":
    main()
