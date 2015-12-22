import datetime
from django.db                              import models
from django.utils                           import timezone
from django.contrib.auth.models             import User

class Z(models.Model):
  user                    = models.OneToOneField('auth.User')
  may_post_event          = models.BooleanField(default=False)
  may_edit_any_event      = models.BooleanField(default=False)
  #may_add_user            = models.BooleanField(default=False)
  notes                   = models.TextField(blank=True,null=True)
  created_date            = models.DateTimeField(default=timezone.now)
  def __str__(self):
    return str(self.user)





