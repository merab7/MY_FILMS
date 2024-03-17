from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def save(self, *args, **kwargs):
            super().save(*args, **kwargs)

            if self.image.name != 'default.jpg':
                try:
                    img = Image.open(self.image.path)

                    if img.height > 300 or img.width > 300:
                        output_size = (300, 300)
                        img.thumbnail(output_size)
                        img.save(self.image.path)

                except Exception as e:
                    # Handle errors (e.g., IOError, FileNotFoundError) appropriately
                    print(f"Error processing image for {self.user.username}: {e}")



     
