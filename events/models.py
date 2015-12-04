import datetime
from django.db                              import models
from django.utils                           import timezone
from django.contrib.auth.models             import User
from userdetails.models                     import Z

class E(models.Model):
  author                  = models.ForeignKey('auth.User', related_name="author")
  e_date                  = models.DateField('Date of the event, in the format "yyyy-mm-dd", e.g. for 31st December 2015, enter "2015-12-31"', default=timezone.now, blank=True,null=True)
  detail_public           = models.TextField('Details to be shown publicly', blank=True,null=True)
  detail_private          = models.TextField('Details to be shown only to logged in users', blank=True,null=True)
  notes                   = models.TextField(blank=True,null=True)
  attendees               = models.ManyToManyField(User, related_name="bookedin")
  created_date            = models.DateTimeField(default=timezone.now)
  is_live                 = models.BooleanField(default=True)
  def __str__(self):
    return self.detail_public





