from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from django.core.validators import RegexValidator
from zonevalue_b2b.upload_paths import user_profile_image_path, company_logo_path
from zonevalue_b2b.storage import s3_storage


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        if not password:
            raise ValueError("Password is required")

        role_id = extra_fields.pop("role", None)

        if role_id:
            try:
                role = Role.objects.get(id=role_id)
                extra_fields["role"] = role
            except Role.DoesNotExist:
                raise ValueError("Invalid role ID")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser (Owner) must have is_staff=True")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    alternate_email = models.EmailField(unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        validators=[RegexValidator(r"^\d{10}$", message="Enter 10 digit phone number")],
    )
    profile_image = models.ImageField(
        upload_to=user_profile_image_path, storage=s3_storage, blank=True, null=True
    )
    gst_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    company_logo = models.ImageField(
        upload_to=company_logo_path, storage=s3_storage, blank=True, null=True
    )
    company_size = models.CharField(
        max_length=50,
        choices=[
            ("1-10", "1-10"),
            ("11-50", "11-50"),
            ("51-200", "51-200"),
            ("201-500", "201-500"),
            ("500+", "500+"),
        ],
        blank=True,
        null=True,
    )
    industry = models.CharField(
        max_length=100,
        choices=[
            ("real_estate", "Real Estate"),
            ("construction", "Construction"),
            ("interior", "Interior Designing"),
            ("legal", "Legal Advisory"),
            ("finance", "Finance/Mortgage"),
        ],
        blank=True,
        null=True,
    )
    company_name = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    is_email_subscribed = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "phone_number", "company_name", "role"]

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["-date_joined"]
