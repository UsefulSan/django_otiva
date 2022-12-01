from django.core.exceptions import ValidationError
from django.db import models

from users.models import Users


def check_non_negative_number(value):
    if int(value) < 0:
        raise ValidationError('This number can not be negative')

# def check_min_len10(value):
#     if len(value) < 10:
#         raise ValidationError('The number of symbols is less than 10')

class Categories(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.CharField(min_length=5, max_length=10, unique=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Ads(models.Model):
    name = models.CharField(min_length=10, max_length=255)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    price = models.IntegerField(validators=[check_non_negative_number])
    description = models.CharField(max_length=500, null=True)
    is_published = models.BooleanField()
    image = models.ImageField(upload_to="images/")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class Selection(models.Model):
    items = models.ManyToManyField(Ads)
    name = models.CharField(max_length=40)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
