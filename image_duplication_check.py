from PIL import Image

def dhash(image, hash_size):
    # Grayscale and shrink the image.
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),Image.Resampling.LANCZOS
    )
    differences = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))

            differences.append(pixel_left > pixel_right)

    hash_num = 0
    for value in differences:
        hash_num *= 2
        if value:
            hash_num += 1

    return hash_num

def get_image_hash(hash_size, img_path):
    image = Image.open(img_path)
    size = image.size[0] * image.size[1]
    img_hash = dhash(image, hash_size)
    return img_hash
    
