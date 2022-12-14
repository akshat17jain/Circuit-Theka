
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from .forms import *
import base64




def HomePageView(request):
    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST , request.FILES )
        if form.is_valid():
            request.session['image_object'] = form.cleaned_data.get('image')
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
    b64_img = base64.b64encode(image_object.file.read()).decode('latin-1')

    context = {'img':b64_img}
    return render(request, 'result.html', context)






