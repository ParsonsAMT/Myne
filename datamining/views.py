from django.conf import settings
from django import http
from django.template import Context, loader

def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context:
        MEDIA_URL
            Path of static media (e.g. "media.example.org")
    """
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return http.HttpResponseServerError(t.render(Context({
        'MEDIA_URL': settings.MEDIA_URL
    })))           
   

def resource_error(request, template_name='404.html'):
    """
    400 error handler.

    Templates: `400.html`
    Context:
        MEDIA_URL
            Path of static media (e.g. "media.example.org")
    """
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return http.HttpResponseServerError(t.render(Context({
        'MEDIA_URL': settings.MEDIA_URL
    })))   
    

def maintenance_error(request, template_name='503.html'):
   """
   503 maintenance page handler.

   Templates: `503.html`
   Context:
       MEDIA_URL
           Path of static media (e.g. "media.example.org")
   """
   t = loader.get_template(template_name) # You need to create a 500.html template.
   return http.HttpResponseServerError(t.render(Context({
       'MEDIA_URL': settings.MEDIA_URL
   })))     