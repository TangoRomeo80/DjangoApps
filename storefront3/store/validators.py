from django.core.exceptions import ValidationError


# Method to validate file size
def validate_file_size(file):
    max_size_kb = 5 * 1024

    if file.size > max_size_kb * 1024:
        raise ValidationError('Max file size is %s KB.' % max_size_kb)
