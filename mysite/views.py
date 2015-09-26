from django.http          import HttpResponse
import datetime
from django.template               import Template, Context

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)


def custom_class_template(request):
    class Person(object):
        def __init__(self, first_name, last_name):
            self.first_name, self.last_name = first_name, last_name
    p = Person('John', 'Smith')
    tt = Template('Hello, {{person_dtl.first_name}} {{person_dtl.last_name}}')
    cc = Context({'person_dtl': p}) 
    return HttpResponse(tt.render(cc))

def template_example(request):
    person = {'name': 'John', 'age':'43'}
    t = Template('{{person_dtl.name}} is {{person_dtl.age}} years old')
    c = Context({'person_dtl': person})
    return HttpResponse(t.render(c))
