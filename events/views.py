from django.shortcuts               import render, get_object_or_404, redirect
from django.utils                   import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User

from .models                        import E
from .forms                         import EForm
from userdetails.models             import Z

def event_list(request, periodsought='current'):
    if periodsought == 'current':
        events = E.objects.filter(is_live=True, e_date__gte=timezone.now()).order_by('e_date')
    else:
        events = E.objects.exclude(is_live=True, e_date__gte=timezone.now()).order_by('-e_date')

    if request.user.is_authenticated():
        user                                     =  User.objects.get(id=request.user.id)
        is_authenticated                         =  True
        if user.z.may_post_event                 == True:
            user_can_post_events                 =  True
        else:
            user_can_post_events                 =  False  
        if user.z.may_edit_any_event             == True:
            user_can_edit_any_event              =  True
        else:
            user_can_edit_any_event              =  False  
        if user.z.may_add_user                   == True:
            user_can_add_users                   =  True
        else:
            user_can_add_users                   =  False
    else:
        is_authenticated                         =  False
        user_can_post_events                     =  False
        user_can_edit_any_event                  =  False  
        user_can_add_users                       =  False
       
    events_augmented = []
    for event in events:
        attendees_list = []
        for attendee in event.attendees.all():
            attendees_list.append(attendee.first_name)
        attendees_string   = ', '.join(attendees_list)

        if is_authenticated                      ==  False:
            user_can_edit_this_event             =   False
        else:
            if user_can_edit_any_event           ==  True:
                user_can_edit_this_event         =   True
            elif event.author                    ==  user:
                user_can_edit_this_event         =   True
            else:
                user_can_edit_this_event         =   False
             
        if event.e_date                          <  timezone.localtime(timezone.now()).date():
          event_status_now                       =  'past'
        elif event.is_live                       == True:
          event_status_now                       =  'live'
        else:
          event_status_now                       = 'deletednonpast'


        event_augmented = {"event":event, "attendees":attendees_string, 'user_can_edit_this_event':user_can_edit_this_event,                   'event_status_now': event_status_now}
        events_augmented.append(event_augmented)


    return render(request, 'events/list.html', {'events': events_augmented, 'periodsought':periodsought, 'user_can_post_events': user_can_post_events, 'is_authenticated':is_authenticated, 'user_can_add_users': user_can_add_users, 'user_can_edit_any_event': user_can_edit_any_event})
   



@login_required
def insertuser(request):
  if request.method                           == "POST":
    form                                      = EForm(request.POST)
    if form.is_valid():
      event                                   = form.save(commit=False)
      if event.e_date                         < timezone.localtime(timezone.now()).date():
        return render(request, 'events/insert_update.html', {'form': form})
      user                                    = User.objects.get(id=request.user.id)

      if user.is_superuser                    == True:
        pass
      elif user.z.may_add_user == True:
        pass
      else:
        return render(request, 'events/insert_update_user.html', {'form': form})

      event.author_name                       = user.username
      event.author                            = user
      event.save()

      return redirect('events.views.event_list')
  else:
    form = EForm()
  return render(request, 'events/insert_update_user.html', {'form': form})

@login_required
def event_process(request, pk='0', function="update"):
  if function                                 == 'insert':
    pass
  else:
    event                                     = get_object_or_404(E, pk=pk)                                         
                                              # i.e. function in ['detail', 'update', 'repeat', 
                                              #'restore', 'bookinto', 'leave', 'delete', 'deleteperm']
    
  if request.method                           == "POST":                       # i.e. have arrived here from 'events/insert_update.html'
    if function                               == 'insert':
      form                                    = EForm(request.POST)
    elif function                             == 'repeat':
      form                                    = EForm(request.POST)
      form_original                           = EForm(request.POST, instance=event)
      if form_original.is_valid():
        event_original                        = form_original.save(commit=False)
    else:   
      form                                    = EForm(request.POST, instance=event)
                                                 # i.e. function == 'update'
                                                 # function in ['detail', 'restore','bookinto', 'leave', 'delete', 'deleteperm'] don't go here
   
    
    if form.is_valid():
      event                                   = form.save(commit=False)
      if event.e_date                         < timezone.localtime(timezone.now()).date():
        error_message                         = 'event date cannot be in the past, please enter a valid date'
        return render(request, 'events/insert_update.html', {'form': form, 'error_message': error_message}) 
                                              # events cannot be posted for dates in past
      else:
        periodsought                          = 'current'

      user                                    = User.objects.get(id=request.user.id)

      if function                             == 'insert':
        event.author_name                     = user.username
        event.author                          = user
        if user.z.may_post_event              == True:
          pass
        else:                                                                 # user is not authorized to insert event                      
          return render(request, 'events/insert_update.html', {'form': form})
      elif function                           == 'update':
        if user.z.may_edit_any_event          == True:
          pass
        elif event.author                     == user:
          pass
        else:   
          return render(request, 'events/insert_update.html', {'form': form})
      else:                                                                      # i.e. function == 'repeat'
        event.author_name                     = user.username
        event.author                          = user                                                           
        if user.z.may_edit_any_event          == True:
          pass
        elif event_original.author            == user:
          pass
        else:                                                                              # user is not authorized to edit this event
          return render(request, 'events/insert_update.html', {'form': form_original})

      event.save()

      return redirect('events.views.event_list', periodsought)

    else:                                                                                  # i.e. form is not valid, ask user to resubmit it
      return render(request, 'events/insert_update.html', {'form': form})   

  else:                                                                                                       # i.e. request.method == "GET":
    if function                               in ['delete', 'deleteperm', 'bookinto', 'leave', 'restore', ]:  
      if event.e_date                         < timezone.localtime(timezone.now()).date():
        # decide which period of events to display afterwards
        periodsought                          = 'notcurrent'
      else:
        periodsought                          = 'current'
      if function                             == 'delete':
        event.is_live                         = False
        event.save()
        return redirect('events.views.event_list', periodsought)
      elif function                           == 'deleteperm':
        event.delete()
        return redirect('events.views.event_list', periodsought)
      elif function                           == 'bookinto':
        updated_attendee = User.objects.get(username = request.user)
        event.attendees.add(updated_attendee)
        event.save()
        return redirect('events.views.event_list', periodsought)
      elif function                           == 'leave':
        updated_attendee = User.objects.get(username = request.user)
        event.attendees.remove(updated_attendee)
        event.save()
        return redirect('events.views.event_list', periodsought)
      else:                                                                                 # i.e. function == 'restore'
        event.is_live                         = True
        event.save()
        return redirect('events.views.event_list', periodsought)
    elif function                             == 'detail':
        return render(request, 'diaryandcontacts/event_detail.html', {'event': item})       # no data input, just buttons
    elif function                             == 'insert':
      form = EForm()
      return render(request, 'events/insert_update.html', {'form': form})                   # ask user for event details
    else:                                                                                   # i.e. function in ['update','repeat']             
      form = EForm(instance=event)
      return render(request, 'events/insert_update.html', {'form': form})                   # ask user for event details


