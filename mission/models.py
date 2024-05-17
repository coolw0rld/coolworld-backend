from django.db import models

from django.db import models

class Mission(models.Model):
    content = models.CharField(max_length=1000)  
    date = models.DateField()  
    is_successful = models.BooleanField(default=False) 
    image = models.ImageField(blank=True, upload_to='mission_images/') 
    category = models.CharField(max_length=100) 

    def __str__(self):
        return self.content

