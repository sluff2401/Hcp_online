from django.shortcuts               import render, get_object_or_404, redirect
from django.utils                   import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User

from .models                        import E
from .forms                         import EForm
#from userdetails.models             import U
#from userdetails.forms              import UForm

def list(request):
    all_events = E.objects.filter(is_live=True).order_by('e_date')
    all_events_with_attendees = []
    for event in all_events:
        attendees_as_full_names = []
        for attendee in event.attendees.all():
            attendees_as_full_names.append(attendee.first_name)
        attendees_as_full_names_as_string = ', '.join(attendees_as_full_names)
        event_with_attendees_as_full_names = {"event":event, "attendees":attendees_as_full_names_as_string}
        all_events_with_attendees.append(event_with_attendees_as_full_names)
    return render(request, 'events/list.html', {'all_events_dtl': all_events_with_attendees})


@login_required
def booking(request, pk, attendance):
    event = get_object_or_404(E, pk=pk)
    updated_attendee = User.objects.get(username = request.user)
    if attendance == 'bookinto':
        event.attendees.add(updated_attendee)
    else:
        event.attendees.remove(updated_attendee)
    event.author = request.user
    event.save()
    return redirect('events.views.list')

@login_required
def insert(request):
  if request.method                           == "POST":
    form                                      = EForm(request.POST)
    if form.is_valid():
      event                                   = form.save(commit=False)
      if event.e_date                         < timezone.localtime(timezone.now()).date():
        return render(request, 'events/insert_update.html', {'form': form})
      user                                    = User.objects.get(id=request.user.id)

      if user.is_superuser                    == True:
        pass
      elif user.userdetail.may_edit_eny_event == True:
        pass
      elif event.author                       == user:
        pass
      else:
        return render(request, 'events/insert_update.html', {'form': form})

      event.author_name                       = user.username
      event.author                            = user
      event.save()

      return redirect('events.views.list')
  else:
    form = EForm()
  return render(request, 'events/insert_update.html', {'form': form})


@login_required
def update(request, pk):
  event                          = get_object_or_404(E, pk=pk)
  if request.method                      == "POST":
    form = EForm(request.POST, instance=event)
    if form.is_valid():
      event                                   = form.save(commit=False)

      user                                    = User.objects.get(id=request.user.id)

      if user.is_superuser                    == True:
        pass
      elif user.userdetail.may_edit_eny_event == True:
        pass
      elif event.author                       == user:
        pass
      else:
        return render(request, 'events/insert_update.html', {'form': form})

      event.author_name                       = user.username
      event.author                            = user
      event.save()

      if event.e_date                         < timezone.localtime(timezone.now()).date():
        return redirect('events.views.list_past')
      else:
        return redirect('events.views.list')
  else:
    form = EForm(instance=event)
  return render(request, 'events/insert_update.html', {'form': form})

@login_required
def remove(request, pk):
  event = get_object_or_404(E, pk=pk, period='1')

  user                               = User.objects.get(id=request.user.id)

  if user.is_superuser               == True:
    pass
  elif user.userdetail.may_edit_eny_event == True:
    pass
  elif event.author                  == user:
    pass
  else:
    if event.e_date                         < timezone.localtime(timezone.now()).date():
      return redirect('events.views.list_past')
    else:
      return redirect('events.views.list')

  event.author_name                       = user.username
  event.author                            = user
  event.is_live                           = False
  event.save()
  #event.delete()
  if event.e_date                         < timezone.localtime(timezone.now()).date():
    return redirect('events.views.list_past')
  else:
    return redirect('events.views.list')