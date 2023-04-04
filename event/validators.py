from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class FileValidator:
    """
    Validator for file fields that checks the file format.
    """
    def __init__(self, allowed_formats):
        self.allowed_formats = allowed_formats

    def __call__(self, value):
        # Get the file extension
        ext = value.name.split('.')[-1]

        # Check if the file extension is in the allowed formats
        if ext not in self.allowed_formats:
            raise ValidationError(f'File format not supported. Allowed formats are: {", ".join(self.allowed_formats)}')

# Allowed file formats
ALLOWED_FORMATS = ['jpg', 'jpeg', 'png', 'gif']

