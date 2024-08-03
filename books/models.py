from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    pdf = models.FileField(upload_to='pdfs/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='cover_images/', null=True, blank=True)  # Nuevo campo de imagen de portada
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
