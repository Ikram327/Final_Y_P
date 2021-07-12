from django.core.exceptions import ValidationError


def validate_fname(value):
    a=True
    for i in value:
        if (i>='a' and i<='z') or (i>='A' and i<='Z'):
            continue
        else:
            a=False
            raise ValidationError("Name must be Characters")
            break
    if a:
        return value
