from django.shortcuts import render, redirect, get_object_or_404
from collections import Counter
from .models import User
from .forms import UserForm
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import requests
import jwt
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError
from datetime import datetime, timedelta
from login import settings 
from django.views.generic import TemplateView
from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.models import User as Users

class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({"message":f"welcome {user.username}"})

def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if not username or not password:
            return JsonResponse({'success':False,'message':'username or password invalid'})
        user = authenticate(request, username=username,password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            # Generate JWT Token
            token = generate_jwt_token(user)
            
            print("tokenHereereree",token)
            # return JsonResponse({'success': True,'token':token}, status=200)
            response = JsonResponse({'success': True,'token':token}, status=200)
            response.set_cookie(
                key='jwt_token',
                value=token,
                httponly=True,     # Prevent access from JavaScript (security)
                secure=False,      # Set to True in production (HTTPS)
                samesite='Lax'     # Or 'Strict' for tighter security
            )
            print('cookiee',request.COOKIES.get('jwt_token'))
            return response
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials or not superuser'}, status=401)

    return render(request, 'login.html')



def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('jwt_token')
        print("jwt verify")
        if not token:
            return redirect('login')

        try:
            decoded = jwt.decode(token, "r1@ke8n&=9(ds41q0k7q&yiz!(y96x2w-f4+zm(0+v0x@(%#js", algorithms=['HS256'])
            request.user = Users.objects.get(id=decoded['id'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'message': 'Invalid token'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)

        return view_func(request, *args, **kwargs)
    return wrapper
def generate_jwt_token(user):
    """
    Generate a JWT token for the given user.
    This token includes the user's email and other information as needed.
    """
    payload = {
        'username': user.username,
        'email': user.email,
        'id': user.id,
        'exp': datetime.utcnow() + timedelta(days=1),  # Expiration time of the token
        # 'exp': datetime.utcnow() + timedelta(seconds=30),  # expires in 30 seconds
        'iat': datetime.utcnow()  # Issued at time
    }
    
    # Secret key for encoding the JWT. You can set this in your Django settings.
    secret_key = "r1@ke8n&=9(ds41q0k7q&yiz!(y96x2w-f4+zm(0+v0x@(%#js"

    # Generate the JWT token
    token = jwt.encode(payload, secret_key, algorithm='HS256') 
    
    return token
@jwt_required 
def user_list(request):
    users = User.objects.all()
    return render(request, 'dashboard.html', {'users': users})

@jwt_required
def user_creates(request):
    form = UserForm()
    # if form.is_valid():
    #     form.save()
    #     return redirect('user_list')
    return render(request, 'form.html', {'form': form})
@jwt_required
@csrf_protect
def user_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = UserForm(data)
            if form.is_valid():
                form.save()
                return JsonResponse({'message': 'User created successfully!'}, status=201)
            else:
                return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def user_update_api(request, pk):
    try:
        print("update api hitted")
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if request.method == 'POST':
        print("update api hitted 2")
        data = json.loads(request.body)
        print(f"{data} data")
        for field, value in data:
            setattr(user, field, value)
        user.save()
        return JsonResponse({'message': 'User updated'})

@csrf_exempt
def user_delete_api(request, pk):
    try:
        user = User.objects.get(pk=pk)
        user.delete()
        return JsonResponse({'message': 'User deleted'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
        
def user_update(request, id):
    user = get_object_or_404(User, id = id)
    # account = User.objects.all()
    # users = User.objects.get(id=id)
    # form = UserForm(instance=users)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'update_form.html', {'form': form})

def logout_view(request):
    # Log the user out (clears the session)
    logout(request)

    # Optionally, clear the 'access_token' cookie (or any other cookies you want to remove)
    response = redirect('login')  # Redirect to login page after logout

    # Delete the 'access_token' cookie (adjust the cookie name and path as needed)
    response.delete_cookie('access_token', path='/')  # Ensure the path matches the cookie’s path

    # You can also delete other cookies here if needed
    # response.delete_cookie('other_cookie', path='/')

    return response

@jwt_required
def dashborard_view(request):
    users = User.objects.all()
    form = UserForm()

    role_counter = Counter()
    role_active_counter = Counter()
    dept_counter = Counter()
    dept_active_counter = Counter()

    for user in users:
        # Count roles
        role_counter[user.user_role] += 1
        if user.is_active:
            role_active_counter[user.user_role] += 1

        # Count departments
        dept_counter[user.department] += 1
        if user.is_active:
            dept_active_counter[user.department] += 1

    # Prepare the context
    context = {
        'user': users.count(),
        'deptcount': len(form['department']),

        # Roles
        'SME': role_counter['SME'],
        'sme_active': role_active_counter['SME'],
        'sme_deactive': role_counter['SME'] - role_active_counter['SME'],

        'Employee': role_counter['Employee'],
        'employee_active': role_active_counter['Employee'],
        'employee_deactive': role_counter['Employee'] - role_active_counter['Employee'],

        'Examiner': role_counter['Examiner'],
        'examiner_active': role_active_counter['Examiner'],
        'examiner_deactive': role_counter['Examiner'] - role_active_counter['Examiner'],

        'admin': role_counter['Admin'],
        'admin_active': role_active_counter['Admin'],
        'admin_deactive': role_counter['Admin'] - role_active_counter['Admin'],

        'candidate': role_counter['Candidate'],
        'candidate_active': role_active_counter['Candidate'],
        'candidate_deactive': role_counter['Candidate'] - role_active_counter['Candidate'],

        # Departments
        'tech_total': dept_counter['Tech'],
        'tech_active': dept_active_counter['Tech'],
        'tech_deactive': dept_counter['Tech'] - dept_active_counter['Tech'],

        'quality_total': dept_counter['Quality Check'],
        'quality_active': dept_active_counter['Quality Check'],
        'quality_deactive': dept_counter['Quality Check'] - dept_active_counter['Quality Check'],

        'media_total': dept_counter['Media'],
        'media_active': dept_active_counter['Media'],
        'media_deactive': dept_counter['Media'] - dept_active_counter['Media'],

        'b_dev_total': dept_counter['Business Development'],
        'b_dev_active': dept_active_counter['Business Development'],
        'b_dev_deactive': dept_counter['Business Development'] - dept_active_counter['Business Development'],
    }

    return render(request, 'dashboard-graph.html', context)

'''
@jwt_required
def dashborard_view(request):
    user = User.objects.all()
    form = UserForm()
    SME = 0
    examiner = 0
    employee = 0
    candidate = 0
    candidate_active = 0
    candiate_deactive = 0
    admin = 0
    admin_active = 0
    admin_deactive = 0
    SME_active = 0
    SME_deactive = 0
    examiner_active = 0
    examiner_deactive = 0
    employee_active = 0
    employee_deactive = 0
    tech_total = 0
    tech_active = 0
    tech_deactive = 0
    quality_total = 0
    quality_active = 0
    quality_deactive = 0
    media_total = 0
    media_active = 0
    media_deactive = 0
    b_dev_total = 0
    b_dev_active = 0
    b_dev_deactive = 0
    #user role
    for i in user:
        if i.user_role == 'SME':
            SME +=1
            if i.is_active == True:
                SME_active += 1
            elif i.is_active == False:
                SME_deactive += 1
        elif i .user_role == "Examiner":
            examiner +=1
            if i.is_active == True:
                examiner_active += 1
            elif i.is_active == False:
                examiner_deactive += 1
        elif i.user_role == 'Employee':
            employee += 1
            if i.is_active == True:
                employee_active += 1
            elif i.is_active == False:
                employee_deactive += 1
        elif i.user_role == 'Candidate':
            candidate+=1
            if i.is_active == True:
                candidate_active += 1
            elif i.is_active == False:
                candiate_deactive += 1
        elif i.user_role == 'Admin':
            admin +=1
            if i.is_active == True:
                admin_active += 1
            elif i.is_active == False:
                admin_deactive += 1
    for i in user:
        if i.department == 'Tech':
            tech_total+=1
            if i.is_active == True:
                tech_active +=1
            elif i.is_active == False:
                tech_deactive +=1
        elif i.department == 'Quality Check':
            quality_total+=1
            if i.is_active == True:
                quality_active +=1
            elif i.is_active == False:
                quality_deactive +=1
        elif i.department == 'Media':
            media_total+=1
            if i.is_active == True:
                media_active +=1
            elif i.is_active == False:
                media_deactive +=1
        elif i.department == "Business Development":
            b_dev_total+=1
            if i.is_active == True:
                b_dev_active +=1
            elif i.is_active == False:
                b_dev_deactive +=1
    return render(request,'dashboard-graph.html',
                  { 'user':user.count(),'deptcount':len(form['department']),
                   'SME':SME,'Examiner':examiner,'Employee':employee,'sme_active':SME_active,'sme_deactive':SME_deactive,'employee_active':employee_active,'employee_deactive':employee_deactive,
                   'examiner_active':examiner_active,'examiner_deactive':examiner_deactive,'candidate':candidate,'candidate_active':candidate_active,'candidate_deactive':candiate_deactive
                   ,'admin':admin,'admin_active':admin_active,'admin_deactive':admin_deactive,'tech_total':tech_total,'tech_active':tech_active,'tech_deactive':tech_deactive,'media_total':media_total,
                   'media_active':media_active,'media_deactive':media_deactive,'quality_total':quality_total,'quality_active':quality_active,
                   'quality_deactive':quality_deactive,
                   'b_dev_total':b_dev_total,'b_dev_active':b_dev_active,'b_dev_deactive':b_dev_deactive})'''
#sending email 
'''
send_mail(
    'contact form', # subject
    'you have logged in form ', #message content
    settings.EMAIL_HOST_USER,
    [email_id],
    fail_silently = False
)
'''
'''def user_delete(request, id):
    user = get_object_or_404(User, id = id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'delete.html', {'user': user})'''

'''def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('jwt_token', path='/')  # Correct cookie name
    return response'''

'''function logoutUser() {
  localStorage.clear();  // If you're still using it
  fetch("/logout/").then(() => {
    window.location.href = "/login";
  });
}
'''

"""class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Access the user directly from the request object
        user = request.user
        return Response({"message": f"Welcome {user.username}!"})

# Login view with error handling
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'success': False, 'message': 'Username and password are required'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return JsonResponse({'success': True}, status=200)
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials or not superuser'}, status=401)

    return render(request, 'login.html')
"""