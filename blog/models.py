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
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    #here we are choosing how to be displayed posts when we are mapping throw them
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})
    

      #user.post_set is amazing i can see all the pots connected to the user and alo\
    #created posts like this user.post_set(.....her goes post) and i do not need to set user because i am creating from this user using post_set
    





















