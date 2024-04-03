from django.db import models
import os

# Create your models here.
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    # def filename(self):
    #     return os.path.basename(self.file.name)