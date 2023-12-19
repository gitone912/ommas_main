from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from .bot import call_bot
from django.http import HttpResponse, JsonResponse
from .models import *
from .gpt import *
from .ai_models.ocr import *
import csv
from .ai_models.cnn_model import *
import pandas as pd
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
    pav_length = request.GET.get('pav_length', '')
    print("pav_length",pav_length)
    if request.method == 'POST':
        try:
            lat1 = request.POST.get('lat', '')
            lng1 = request.POST.get('lng', '')
            lat2 = request.POST.get('lat2', '')
            lng2 = request.POST.get('lng2', '')
            pav_length = request.POST.get('pav_length')
            print("pav_length",pav_length)
            
            map_url = f'http://127.0.0.1:8000/map/?lat={lat1}&lng={lng1}&lat2={lat2}&lng2={lng2}&pav_length={pav_length}'

            # Redirect to the map URL
            return redirect(map_url)
        except Exception as e:
            # Handle exceptions if any
            print(e)

    # Render the get_coordinates.html template for initial page load
    return render(request, 'coordinate_map.html',{'pav_length':pav_length})


def map(request):
    # You can retrieve data from the URL or any other source
    # For now, let's assume you receive the data as a query parameter in the URL
    lat1 = request.GET.get('lat', '')
    lng1 = request.GET.get('lng', '')
    lat2 = request.GET.get('lat2', '')
    lng2 = request.GET.get('lng2', '')
    pav_length = request.GET.get('pav_length', '')
    print("pav_length",pav_length)
    
    # Convert the coordinates into a list of lists
    coordinates_list = [[float(lat1), float(lng1)], [float(lat2), float(lng2)]]

    data = coordinates_list
    print(data)
    print("hello")
    return render(request, 'map.html', {'data': data,'pav_length':pav_length})



def ocr_reader(request):
    return render(request, 'ocr.html')

def csv_to_dict(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def quality_monitor_data(request):
    csv_file_path = 'static/data/ariyalur.csv'  

    csv_data = csv_to_dict(csv_file_path)

    return render(request, 'quality_monitor_data.html', {'csv_data': csv_data})

def upload_data(request):
    if request.method == 'POST':
        try:
            file = request.FILES['file']
            print(file)
            return render(request, 'upload_data.html', {'success': 'File uploaded successfully.'})
        except Exception as e:
            return render(request, 'upload_data.html', {'error': str(e)})
    return render(request, 'upload.html')

def joint_inspection_cnn(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        prediction = predict_image(image.temporary_file_path())  # Update with your actual prediction function
        return render(request, 'cnn.html', {'prediction': prediction})

    return render(request, 'cnn.html')

def usfg(request):
    # Read data from CSV file
    with open('static/data/unsatisfactory_work_grade/sqm/indiasqm.csv', 'r') as file:
        india_data = list(csv.DictReader(file))

    with open('static/data/unsatisfactory_work_grade/sqm/jharkhand.csv', 'r') as file:
        jharkhand_data = list(csv.DictReader(file))

    with open('static/data/unsatisfactory_work_grade/sqm/bokaro.csv', 'r') as file:
        bokaro_data = list(csv.DictReader(file))

    return render(request, 'chart.html', {'india_data': india_data, 'jharkhand_data': jharkhand_data, 'bokaro_data': bokaro_data})


def mga(request):
    return render(request,'monitorwise_grading_abstract.html')


# views.py
from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse

def chart_data(request):
    # Load your CSV data into a DataFrame
    df = pd.read_csv('static/data/monitor/sqm_monitors_jh.csv')


    # Example 1: Bar Chart - Total Counts of C, P, M, L Grades
    total_counts = df.groupby(['MONITOR_NAME', 'ADMIN_IM_YEAR', 'ADMIN_IM_MONTH1']).agg({
        'C_GRADE_COUNT_T': 'sum',
        'P_GRADE_COUNT_T': 'sum',
        'M_GRADE_COUNT_T': 'sum',
        'L_GRADE_COUNT_T': 'sum',
    }).reset_index()

    # Example 2: Line Chart - Ongoing and Maint counts
    ongoing_maint_counts = df.groupby(['MONITOR_NAME', 'ADMIN_IM_YEAR', 'ADMIN_IM_MONTH1']).agg({
        'ONGOING_S': 'sum',
        'MAINT_S': 'sum',
    }).reset_index()

    # Example 3: Doughnut Chart - Total Counts of COMP_S, ONGOING_S, MAINT_S, LSB_S
    doughnut_counts = df.groupby(['MONITOR_NAME']).agg({
        'COMP_S': 'sum',
        'ONGOING_S': 'sum',
        'MAINT_S': 'sum',
        'LSB_S': 'sum',
    }).reset_index()

    # Example 4: Radar Chart - Total Counts of C_GRADE_COUNT_T, P_GRADE_COUNT_T, M_GRADE_COUNT_T, L_GRADE_COUNT_T
    radar_counts = df.groupby(['MONITOR_NAME']).agg({
        'C_GRADE_COUNT_T': 'sum',
        'P_GRADE_COUNT_T': 'sum',
        'M_GRADE_COUNT_T': 'sum',
        'L_GRADE_COUNT_T': 'sum',
    }).reset_index()

    chart_data = {
        'bar_chart': {
            'labels': total_counts.apply(lambda x: f"{x['ADMIN_IM_MONTH1']} {x['ADMIN_IM_YEAR']} - {x['MONITOR_NAME']}", axis=1).tolist(),
            'datasets': [
                {
                    'label': 'C Grade',
                    'data': total_counts['C_GRADE_COUNT_T'].tolist(),
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'borderColor': 'rgba(75, 192, 192, 1)',
                    'borderWidth': 1,
                },
                # ... Repeat for P, M, L Grades
            ],
        },
        'line_chart': {
            'labels': ongoing_maint_counts.apply(lambda x: f"{x['ADMIN_IM_MONTH1']} {x['ADMIN_IM_YEAR']} - {x['MONITOR_NAME']}", axis=1).tolist(),
            'datasets': [
                {
                    'label': 'Ongoing',
                    'data': ongoing_maint_counts['ONGOING_S'].tolist(),
                    'borderColor': 'rgba(255, 99, 132, 1)',
                    'borderWidth': 1,
                    
                },
                {
                    'label': 'Maint',
                    'data': ongoing_maint_counts['MAINT_S'].tolist(),
                    'borderColor': 'rgba(255, 255, 0, 1)',
                    'borderWidth': 1                    
                },
            ],
        },
        'doughnut_chart': {
            'labels': doughnut_counts['MONITOR_NAME'].tolist(),
            'datasets': [
                {
                    'data': doughnut_counts['COMP_S'].tolist(),
                    'backgroundColor': ['rgba(75, 192, 192, 0.2)', 'rgba(255, 99, 132, 0.2)', 'rgba(255, 255, 0, 0.2)'],
                },
                # ... Repeat for Ongoing, Maint, LSB
                {
                    'data': doughnut_counts['ONGOING_S'].tolist(),
                    'backgroundColor': ['rgba(75, 192, 192, 0.2)', 'rgba(255, 99, 132, 0.2)', 'rgba(255, 255, 0, 0.2)'],
                },
                {
                    'data': doughnut_counts['MAINT_S'].tolist(),
                    'backgroundColor': ['rgba(75, 192, 192, 0.2)', 'rgba(255, 99, 132, 0.2)', 'rgba(255, 255, 0, 0.2)'],
                },
                {
                    'data': doughnut_counts['LSB_S'].tolist(),
                    'backgroundColor': ['rgba(75, 192, 192, 0.2)', 'rgba(255, 99, 132, 0.2)', 'rgba(255, 255, 0, 0.2)'],
                }
            ],
        },
        'radar_chart': {
            'labels': radar_counts['MONITOR_NAME'].tolist(),
            'datasets': [
                {
                    'label': 'C Grade',
                    'data': radar_counts['C_GRADE_COUNT_T'].tolist(),
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'borderColor': 'rgba(75, 192, 192, 1)',
                    'borderWidth': 1,
                    
                },
                # ... Repeat for P, M, L Grades
            ],
        },
    }

    return JsonResponse(chart_data)
