from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Test(models.Model):
    #size=models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)