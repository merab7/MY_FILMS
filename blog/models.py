from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class FilmCard(models.Model):
    title = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.FloatField()
    ranking = models.CharField(max_length=100)
    review = models.TextField()
    img_url = models.ImageField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)  

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Post(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    post_text = models.TextField()
    film = models.ForeignKey(FilmCard, on_delete=models.CASCADE)
    author =  models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author.username} - {self.date_created}"

class MyT_10(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    rank = models.IntegerField(default=0)
    film = models.ForeignKey(FilmCard, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['rank', '-date_created'] 
