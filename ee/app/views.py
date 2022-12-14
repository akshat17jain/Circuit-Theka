
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .models import *
from .forms import *
import base64
import json
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.serializers.json import DjangoJSONEncoder


class MyJsonEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, InMemoryUploadedFile):
           return o.read()
        return str(o)

def HomePageView(request):
    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST , request.FILES )
        if form.is_valid():
            uimg = form.cleaned_data.get('image')
            img = json.dumps(uimg, cls=MyJsonEncoder)
            request.session['image_object'] = img
            return redirect('ResultView')
    else:
        form = ImageForm()

    params = {'form': form}
    return render(request, 'home.html', params)

class AboutProjectPageView(TemplateView):
    template_name = 'about_project.html'


class DevelopersPageView(TemplateView):
    template_name = 'developers.html'

def ResultView(request):
    image_object = request.session.get('image_object')
    b64_img = base64.b64encode(image_object)

    context = {'img':b64_img}
    return render(request, 'result.html', context)






