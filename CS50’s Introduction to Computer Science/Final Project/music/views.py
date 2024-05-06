from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.
def top_artists():
    url = "https://spotify-scraper.p.rapidapi.com/v1/chart/artists/top"
    headers = {
        "X-RapidAPI-Key": "6903eee1d0msh6462ca846c711fap16a743jsne5656e3c2bfe",
        "X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    response_data = response.json()

    artists_info = []

    if 'artists' in response_data:

        for artist in response_data['artists']:
            name = artist.get('name', 'No name')
            avatar_url = artist.get('visuals', {}).get('avatar', [{}])[0].get('url', 'No URL')
            artist_id = artist.get('id', 'No ID')
            artists_info.append((name, avatar_url, artist_id))

    return artists_info


@login_required(login_url='login')
def index(request):
    artists_info = top_artists()
    context = {
        'artists_info' : artists_info,
    }
    return render(request, 'index.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
        
    return render(request, 'login.html')

def singup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('singup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('singup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('/')
        else:
            messages.info(request, 'Password Did Not Matched')
            return redirect('singup')
    else:
        return render(request, 'singup.html', {'messages': messages.get_messages(request)})

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')
