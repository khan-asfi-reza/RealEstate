import re
from rest_framework import serializers


def password_validator(value):
    if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', value):
        raise serializers.ValidationError(
            "Password must be minimum 8 characters long and contain digit ,capital letter and special character")

    elif re.compile('[A-Z]').search(value) is None:
        raise serializers.ValidationError("Password must have minimum one capital letter")

    elif re.compile('[0-9]').search(value) is None:
        raise serializers.ValidationError('Password must have digits')

