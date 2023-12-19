from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from .bot import call_bot
from django.http import HttpResponse, JsonResponse
from .models import *
from .gpt import *
from .ai_models.ocr import *
# Create your views here.

def bot(request):
    if request.method == 'POST':
        try:
            user_input = request.POST.get('user_input', '')
            response = generate_prompt(user_input)
            print(response)
            # Save the chat history
            Chat.objects.create(user_input=user_input, response=response)
            print("created")
            chat_history = Chat.objects.all().order_by('-timestamp')
            return render(request, 'bot.html', {'chat_history': chat_history})
        except Exception as e:
            print(e)
            print("error")
            return render(request, 'bot.html', {'error': str(e)})

    chat_history = Chat.objects.all().order_by('-timestamp')
    return render(request, 'bot.html', {'chat_history': chat_history})


def login_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            error_message = 'Invalid username or password.'

    return render(request, 'login.html', {'error_message': error_message})

def signup_view(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            error_message = 'Username already exists. Please choose a different one.'
        elif User.objects.filter(email=email).exists():
            error_message = 'Email already exists. Please use a different one.'
        else:
            User.objects.create_user(username=username, email=email, password=password)
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('login')  

    return render(request, 'signup.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')


def dashboard(request):
    return render(request,'index.html')

from django.shortcuts import render

def get_coordinates(request):
    if request.method == 'POST':
        try:
            lat1 = request.POST.get('lat', '')
            lng1 = request.POST.get('lng', '')
            lat2 = request.POST.get('lat2', '')
            lng2 = request.POST.get('lng2', '')
            
            # Assuming you have a Map model to store coordinates in the database
            # You can save the coordinates to the database or perform any other actions
            # Example: Map.objects.create(latitude=lat1, longitude=lng1)
            #          Map.objects.create(latitude=lat2, longitude=lng2)

            # Construct the map URL with the coordinates
            map_url = f'http://127.0.0.1:8000/map/?lat={lat1}&lng={lng1}&lat2={lat2}&lng2={lng2}'

            # Redirect to the map URL
            return redirect(map_url)
        except Exception as e:
            # Handle exceptions if any
            print(e)

    # Render the get_coordinates.html template for initial page load
    return render(request, 'coordinate_map.html')


def map(request):
    # You can retrieve data from the URL or any other source
    # For now, let's assume you receive the data as a query parameter in the URL
    lat1 = request.GET.get('lat', '')
    lng1 = request.GET.get('lng', '')
    lat2 = request.GET.get('lat2', '')
    lng2 = request.GET.get('lng2', '')

    # Convert the coordinates into a list of lists
    coordinates_list = [[float(lat1), float(lng1)], [float(lat2), float(lng2)]]

    data = coordinates_list
    print(data)
    print("hello")
    return render(request, 'map.html', {'data': data})



def ocr_reader(request):
    return render(request, 'ocr.html')