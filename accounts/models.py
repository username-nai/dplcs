from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    member_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True)
    is_admin_role = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.member_id and self.pk is None:
            # We need to save first to get an ID if we want to base it on ID
            # Or we can generate based on the last user's ID
            super().save(*args, **kwargs)
            self.member_id = f"LIB{self.pk:06d}"
            # Need to save again to update the member_id
            kwargs['force_insert'] = False
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member_id} - {self.username}"
