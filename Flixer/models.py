from django.db import models


# Create your models here.
class Movie(models.Model):
    movie_id = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    link = models.URLField()
    year = models.IntegerField()

    def __str__(self):
        return '{0} : {1} : {2} : {3}'.format(self.movie_id, self.name, self.link, str(self.year))


class User(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=20)
    gender = models.CharField(max_length=2,
                              choices=[('M', 'Male'),
                                       ('F', 'Female')])
    email = models.EmailField()

    def __str__(self):
        return '{0} : {1} : {2} : {3}'.format(self.user_id, self.name, self.password, self.email)
