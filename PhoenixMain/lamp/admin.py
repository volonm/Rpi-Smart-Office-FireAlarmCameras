from django.contrib import admin
from lamp.models import Lamps

# Register your models here.

admin.site.register(Lamps)

# class Book(models.Model):
#     GENRE = (
#         ('F', 'Fiction'),
#         ('NF', 'Non-Fiction'),
#     )
#     book_title = models.CharField(max_length=200)
#     book_published = models.DateTimeField("date published", default=datetime.now())
#     book_author = models.CharField(max_length=200)
#     book_genre = models.CharField(max_length=1, choices=GENRE, default='NF')