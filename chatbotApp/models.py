from django.db import models

# Create your models here.
class Past(models.Model):
    #we are going to save two fileds
    question = models.CharField(max_length=250)
    answer = models.TextField(max_length=5000)

    def __str__(self):
        #it gives string representation to the question  
        # It is used to display a human-readable version of the object in the Django admin interface.
        return self.question


