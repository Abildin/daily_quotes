from django.db import models

class Quote(models.Model):
    quote = models.TextField()
    source = models.CharField(max_length=100)
    date = models.DateField()

    def __unicode__(self):
        return self.date
