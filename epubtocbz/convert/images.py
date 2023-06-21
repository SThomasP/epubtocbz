from io import BytesIO
from PIL import Image


def scale(right_image, left_image):
    rw, rh = right_image.size
    lw, lh = left_image.size
    if lh > rh:
        return right_image, left_image.resize((int(lw / lh * rh), rh))
    elif rh > lh:
        return right_image.resize((int(rw / rh * lh), lh)), left_image
    else:
        return right_image, left_image


def create_spread(right, left):
    right_image = open_image(right)
    left_image = open_image(left)
    r_scaled, l_scaled = scale(right_image, left_image)
    rw, rh = r_scaled.size
    lw, lh = l_scaled.size
    spread_width = rw + lw
    spread_height = max(lh, rh)
    spread_image = Image.new('RGB', (spread_width, spread_height))
    spread_image.paste(r_scaled, (lw, 0))
    spread_image.paste(l_scaled, (0, 0))
    image_io = BytesIO()
    spread_image.save(image_io, format='JPEG', quality=95)
    left_image.close()
    right_image.close()
    spread_image.close()
    return image_io.getvalue()


def open_image(imageb):
    return Image.open(BytesIO(imageb))
