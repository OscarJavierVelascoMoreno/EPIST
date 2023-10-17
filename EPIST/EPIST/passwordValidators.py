from django.core.exceptions import ValidationError
import re

class ComplexPasswordValidator:
    """
    Validate whether the password contains minimum one uppercase, one digit and one symbol.
    """
    def validate(self, password, user=None):
        if re.search('[A-Z]', password)==None or re.search('[0-9]', password)==None or re.search('[^A-Za-z0-9]', password)==None:
            raise ValidationError(
                "Esta contraseña es débil. La contraseña debe contener al menos 1 número, 1 mayúscula y 1 símbolo no alfanumérico.",
                code='password_is_weak',
            )
