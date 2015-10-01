from django.shortcuts               import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User

from .models                        import Event

def event_list(request):
    all_events = Event.objects.order_by('event_date')
    return render(request, 'events_app_b/event_list.html', {'all_events_dtl': all_events})

@login_required
def event_booking(request, pk, attendance):
    event = get_object_or_404(Event, pk=pk)
    updated_attendee = User.objects.get(username = request.user)
    if attendance == 'bookinto':
        event.attendees.add(updated_attendee)
    else:
        event.attendees.remove(updated_attendee)
    event.author = request.user
    event.save()
    return redirect('events_app_b.views.event_list')

