from imageretrival.imageprocessing.matcher import AutomaticDuplicateFinder, ManualDuplicateFinder
from imageretrival.models import Image
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.hashers import make_password


def do_login(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        print('logeado')
        return redirect('/imagenes')
    else:
        messages.error(request, 'Nombre de usuario o contraseña incorrecta')
        return redirect('/login')


def do_register(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']

    user = User()
    user.username = username
    user.password = make_password(password)
    user.email = email
    user.save()

    login(request, user)

    return redirect('/imagenes')


def find_duplicates(request):
    context = {}
    if request.method == 'POST':
        image = request.FILES['photo']
        df = ManualDuplicateFinder(
            Image.objects.filter(user_id=request.user), image)
        res = df.find_duplicates()
        context = {
            'result': res
        }
        if(len(res) == 0):
            messages.info(
                request, 'No se han encontrado duplicados para esta imagen')
    return render(request, 'imageretrival/duplicates.html', context)


def delete(request, image_id):
    image = Image.objects.get(pk=image_id)
    image.delete()
    return redirect('/imagenes')


def find_automatic_duplicates(request):
    df = AutomaticDuplicateFinder(Image.objects.filter(user_id=request.user))
    res = df.find_duplicates()
    context = {
        'result': res
    }
    if(len(res) == 0):
        messages.info(
            request, 'No se han encontrado duplicados en su colección')
    return render(request, 'imageretrival/duplicates.html', context)
