from imageretrival.imageprocessing.utils import to_json
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Descriptor, Image
from .imageprocessing.featureextraction import ORBExtractor
from django.contrib.auth import logout as do_logout
from django.contrib import messages
from .imageprocessing.utils import to_json
# Create your views here.


def index(request):
    return render(request, 'imageretrival/index.html')

def images(request):
    print(request.user)
    if(request.user.is_authenticated):
        images = Image.objects.filter(user=request.user).order_by('-created_at')
        context = {
            'images': images
        }
        return render(request, 'imageretrival/images.html', context)
    return redirect('/login')

def upload(request):
    if request.method == 'POST' and request.FILES['photo']:
        try:
            file = request.FILES['photo']
            orb = ORBExtractor(file)
            orb_result = orb.compute()
            image = Image()
            image.title = request.POST['title']
            image.width = orb.image.shape[0]
            image.height = orb.image.shape[1]
            image.file = file
            image.user = request.user
            image.save()
            descriptor = Descriptor()
            descriptor.rows = orb_result.shape[0]
            descriptor.cols = orb_result.shape[1]
            descriptor.content = str(to_json(orb_result)).replace(' ', '')
            descriptor.image = image
            descriptor.save()
            messages.success(request, 'La imagen se ha cargado correctamente')
        except:
            messages.error(request, 'Errpr al cargar la imagen, intente nuevamente')
        return redirect('/subir-imagen')
    return render(request, 'imageretrival/upload.html')

def detail(request, image_id):
    image = Image.objects.get(pk=image_id)
    context = {
        'image': image
    }
    return render(request, 'imageretrival/detail.html', context)

def duplicates(request):
    return HttpResponse(request, 'Hola mundo')

def login(request):
    return render(request, 'imageretrival/login.html')

def register(request):
    return render(request, 'imageretrival/register.html')

def logout(request):
    do_logout(request)
    return redirect('/')

