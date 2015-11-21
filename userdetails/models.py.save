from django.db                              import models
from django.contrib.auth.models             import User

class Event(models.Model):
    author = models.ForeignKey('auth.User')
    event_date = models.DateField()
    event_details = models.TextField()
    attendees = models.ManyToManyField(User, related_name="bookedin")
    def __str__(self):               
        return self.event_details




  
