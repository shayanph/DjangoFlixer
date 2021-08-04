from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=30)

    def __str__(self):
        return '{0} : {1}'.format(self.category_id, self.cat_name)


class Movie(models.Model):
    movie_id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    link = models.URLField()
    year = models.IntegerField()
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} : {1} : {2} : {3} : {4}'.format(self.movie_id, self.name,
                                                    self.link, str(self.year),
                                                    self.category.category_id)


class Rating(models.Model):
    rating_id = models.CharField(max_length=30, primary_key=True)
    user_id = models.CharField(max_length=30)
    movie_id = models.CharField(max_length=30)
    rating_value = models.CharField(max_length=1)


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, name, gender, password, **other_fields):
        other_fields.setdefault('is_admin', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)

        return self.createUser(email, name, gender, password, **other_fields)

    def createUser(self, email, name, gender, password, **other_fields):
        email = self.normalize_email(email)
        user = UserMovie(email=email, name=name, gender=gender, **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserMovie(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=2,
                              choices=[('M', 'Male'),
                                       ('F', 'Female')])
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'gender']

    def __str__(self):
        return '{0} : {1} : {2} : {3}'.format(self.id, self.name, self.is_staff, self.email)
