import datetime
from django.db                              import models
from django.utils                           import timezone
from django.contrib.auth.models             import User

class Z(models.Model):
  author                  = models.ForeignKey('auth.User', related_name="author")
  e_date                  = models.DateField()
  detail_public           = models.TextField(blank=True,null=True)
  detail_private          = models.TextField(blank=True,null=True)
  notes                   = models.TextField(blank=True,null=True)
  attendees               = models.ManyToManyField(User, related_name="bookedin")
  created_date            = models.DateTimeField(default=timezone.now)
  is_live                 = models.BooleanField(default=True)
  def __str__(self):
    return self.detail_public





