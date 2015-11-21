from django.shortcuts               import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models     import User

from .models                        import Z

def userdetail_list(request):
    all_userdetails = Z.objects.order_by('user')
    return render(request, 'userdetails/userdetail_list.html', {'all_userdetails': all_userdetails})

