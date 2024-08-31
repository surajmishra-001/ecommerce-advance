from django.core.exceptions import ValidationError
from PIL import Image

def validate_thumbnail_size(image):
    img = Image.open(image)
    # Example validation: Limit to 2 MB
    max_size = 2 * 1024 * 1024  # 2 MB
    if image.size > max_size:
        raise ValidationError("The maximum file size allowed is 2 MB.")
