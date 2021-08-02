from django.db import models


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


class User(models.Model):
    user_id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=20)
    gender = models.CharField(max_length=2,
                              choices=[('M', 'Male'),
                                       ('F', 'Female')])
    email = models.EmailField()

    def __str__(self):
        return '{0} : {1} : {2} : {3}'.format(self.user_id, self.name, self.password, self.email)
