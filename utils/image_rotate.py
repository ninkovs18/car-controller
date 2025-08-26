from PIL import Image
from io import BytesIO

def rotate_img(image_bytes: BytesIO, rotation_degree: int) -> BytesIO:
        
        image = Image.open(image_bytes)
        
        if rotation_degree == 90:
            image_rotated = image.rotate(90, expand=True)
        elif rotation_degree == -90:
            image_rotated = image.rotate(-90, expand=True)
        elif rotation_degree == 180:
            image_rotated = image.rotate(180, expand=True)
        else:
            image_rotated = image

        image_bytes_new = BytesIO()
        image_rotated.save(image_bytes_new, format='JPEG')
        
        image_bytes_new.seek(0)
        
        return image_bytes_new
        