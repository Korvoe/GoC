from django.db import models
from django.contrib.auth.models import AbstractUser
from Crypto.Cipher import AES
from django.conf import settings
from django.core.exceptions import FieldError, ImproperlyConfigured
from django.utils.functional import cached_property
import hashlib
import string


class EncryptedMixin(models.Field):
    def __init__(self, *args, **kwargs):
        if kwargs.get("primary_key"):
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} does not support primary_key=True."
            )
        if kwargs.get("unique"):
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} does not support unique=True."
            )
        if kwargs.get("db_index"):
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} does not support db_index=True."
            )
        self._internal_type = "BinaryField"
        super().__init__(*args, **kwargs)

    def keys(self):
        key_list = settings.FIELD_ENCRYPTION_KEYS
        if not isinstance(key_list, (list, tuple)):
            raise ImproperlyConfigured("FIELD_ENCRYPTION_KEYS should be a list.")
        return key_list

    def encrypt(self, data_to_encrypt):
        if not isinstance(data_to_encrypt, str):
            data_to_encrypt = str(data_to_encrypt)
        keys = self.keys()
        cipher = AES.new(bytes.fromhex(keys[0]), AES.MODE_GCM)
        nonce = cipher.nonce
        cypher_text, tag = cipher.encrypt_and_digest(data_to_encrypt.encode())
        return nonce + tag + cypher_text

    def decrypt(self, value):
        nonce = value[:16]
        tag = value[16:32]
        cypher_text = value[32:]
        counter = 0
        keys = self.keys()
        num_keys = len(keys[0])
        while counter < num_keys:
            cipher = AES.new(
                bytes.fromhex(keys[counter]), AES.MODE_GCM, nonce=nonce
            )
            try:
                plaintext = cipher.decrypt_and_verify(cypher_text, tag)
            except ValueError:
                counter += 1
                continue
            return plaintext.decode()
        raise ValueError("AES Key incorrect or message corrupted")

    def get_internal_type(self):
        return self._internal_type

    def get_db_prep_save(self, value, connection):
        value = super().get_db_prep_save(value, connection)
        if value is not None:
            encrypted_value = self.encrypt(value)
            return connection.Database.Binary(encrypted_value)

    def from_db_value(self, value, expression, connection):
        if value is not None:
            return self.to_python(self.decrypt(value))

    @cached_property
    def validators(self):
        # For IntegerField (and subclasses) we must pretend to be that
        # field type to get proper validators.
        self._internal_type = super().get_internal_type()
        try:
            return super().validators
        finally:
            self._internal_type = "BinaryField"

class EncryptedCharField(EncryptedMixin, models.CharField):
    pass

class EncryptedEmailField(EncryptedMixin, models.EmailField):
    pass



class CustomUser(AbstractUser):
    pass
    first_name = EncryptedCharField(max_length=50)
    last_name = EncryptedCharField(max_length=50)
    email =  EncryptedEmailField(max_length=50)
    last_active = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
