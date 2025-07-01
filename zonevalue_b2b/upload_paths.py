import os
from django.utils.text import slugify


def get_extension(filename):
    return os.path.splitext(filename)[1].lower()


def user_profile_image_path(instance, filename):
    email = getattr(instance, "email", None)
    username = slugify(email.split("@")[0]) if email else "user"
    ext = get_extension(filename)
    return f"users/{username}/profile{ext}"


def company_logo_path(instance, filename):
    email = getattr(instance, "email", None)
    username = slugify(email.split("@")[0]) if email else "user"
    company_name = getattr(instance, "company_name", None) or "company"
    company_slug = slugify(company_name)
    ext = get_extension(filename)
    return f"users/{username}/companies/{company_slug}/logo{ext}"
