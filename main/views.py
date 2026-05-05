from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .models import BloodStock, BloodRequest, Donor


# HOME
def home(request):
    return render(request, 'home.html')


# LOGIN (ADMIN USE)
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/admin/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect('/')


# SEARCH
def search_blood(request):
    results = []
    searched = False

    if request.GET.get('blood_group') and request.GET.get('city'):
        blood_group = request.GET.get('blood_group')
        city = request.GET.get('city')

        results = BloodStock.objects.filter(
            blood_group__iexact=blood_group,
            city__iexact=city
        )

        searched = True

    return render(request, 'search.html', {
        'results': results,
        'searched': searched
    })


# REQUEST BLOOD (WITH VALIDATION ✅)
def request_blood(request):
    if request.method == "POST":
        blood_group = request.POST.get('blood_group')
        quantity = request.POST.get('quantity')
        city = request.POST.get('city')
        contact = request.POST.get('contact')

        
        if int(quantity) <= 0:
            return render(request, 'request.html', {
                'error': 'Quantity must be greater than 0'
            })

        if len(contact) != 10:
            return render(request, 'request.html', {
                'error': 'Contact number must be 10 digits'
            })

        # ✅ SAVE
        BloodRequest.objects.create(
            blood_group=blood_group,
            quantity=quantity,
            city=city,
            contact=contact
        )

        return render(request, 'request.html', {
            'success': True
        })

    return render(request, 'request.html')


# DONATE BLOOD (WITH VALIDATION ✅)
def donate_blood(request):
    if request.method == "POST":
        name = request.POST.get('name')
        blood_group = request.POST.get('blood_group')
        phone = request.POST.get('phone')
        age = request.POST.get('age')

        # 🔥 VALIDATION
        if int(age) < 18:
            return render(request, 'donate.html', {
                'error': 'You must be at least 18 years old'
            })

        if len(phone) != 10:
            return render(request, 'donate.html', {
                'error': 'Phone number must be 10 digits'
            })

        Donor.objects.create(
            name=name,
            blood_group=blood_group,
            phone=phone,
            age=age,
            last_donation_date="2024-01-01"
        )

        return render(request, 'donate.html', {
            'success': True
        })

    return render(request, 'donate.html')