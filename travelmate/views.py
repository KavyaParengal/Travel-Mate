from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *

###### Register the user ########

def register(request):

    # User already logged in
    if request.user.is_authenticated:

        if request.user.is_superuser:
            return redirect('admin_dashboard')
        else:
            return redirect('user_dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        print("Registration Successful")
        return redirect('login')

    return render(request, 'register.html')

###### Login the user ########

def login_user(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('admin_dashboard')

            else:
                return redirect('user_dashboard')

        
        messages.error(request, "Invalid Username or Password")

    return render(request, 'login.html')

###### Logout the user ########

def logout_user(request):
    logout(request)
    return redirect('login')

########################################### ADMIN MODULE ###########################################

##### Dashboards for Admin ######

@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        return redirect('user_dashboard')

    return render(request, 'adminPage/admin_dashboard.html')

def view_destination(request):
    if not request.user.is_superuser:
        return redirect('user_dashboard')

    destinations = Destination.objects.all()
    return render(request, 'adminPage/view_destination.html', {'destinations': destinations})

def delete_destination(request, id):

    destination = get_object_or_404(Destination,id=id)
    destination.delete()
    messages.success(request,"Destination deleted successfully.")

    return redirect('view_destination')

def add_destination(request):

    if request.method == "POST":

        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        Destination.objects.create(
            name=name,
            description=description,
            image=image
        )

        messages.success(request,"Destination added successfully.")

        return redirect('view_destination')

    return render(request,'adminPage/add_destination.html')

def edit_destination(request, id):

    destination = get_object_or_404( Destination,id=id)

    if request.method == "POST":

        destination.name = request.POST.get('name')
        destination.description = request.POST.get('description')

        if request.FILES.get('image'):
            destination.image = request.FILES.get('image')

        destination.save()

        messages.success(request,"Destination updated successfully.")

        return redirect('view_destination')

    return render(request,'adminPage/edit_destination.html',{'destination': destination})

def view_contact_messages(request):

    contacts = Contact.objects.all().order_by('-created_at')

    return render(
        request,'adminPage/view_contact.html',{'contacts': contacts})

def view_bookings(request):

    bookings = Booking.objects.all().order_by('-booking_date')

    return render(request,'adminPage/view_booking.html',{'bookings': bookings})

def view_users(request):
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')

    return render(request, 'adminPage/view_users.html', {'users': users})

def admin_view_packages(request):
    packages = Package.objects.all()

    return render(request, 'adminPage/view_packages.html', {'packages': packages})

def add_package(request):

    if request.method == "POST":

        title = request.POST.get('title')
        location = request.POST.get('location')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        travel_date = request.POST.get('travel_date')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        is_recommended = (request.POST.get('is_recommended') == 'on')

        Package.objects.create(
            title=title,
            location=location,
            description=description,
            image=image,
            duration=duration,
            travel_date=travel_date,
            price=price,
            is_recommended=is_recommended
        )

        messages.success(request,"Package added successfully.")

        return redirect('admin_view_packages')

    return render(request,'adminPage/add_package.html')

def delete_package(request, id):

    package = get_object_or_404(Package,id=id)
    package.delete()
    messages.success(request,"Package deleted successfully.")

    return redirect('admin_view_packages')

def edit_package(request, id):

    package = get_object_or_404(Package,id=id)

    if request.method == "POST":

        package.title = request.POST.get('title')
        package.location = request.POST.get('location')
        package.description = request.POST.get('description')
        package.duration = request.POST.get('duration')
        package.travel_date = request.POST.get('travel_date')
        package.price = request.POST.get('price')

        package.is_recommended = (request.POST.get('is_recommended') == 'on')

        if request.FILES.get('image'):
            package.image = request.FILES.get('image')

        package.save()

        messages.success(request,"Package updated successfully.")

        return redirect('admin_view_packages')

    return render(request,'adminPage/edit_package.html',{'package': package})


def admin_view_touristplace(request):
    destinations = Destination.objects.all()

    destination_id = request.GET.get('destination')

    tourist_places = TouristPlace.objects.select_related('destination')

    if destination_id:
        tourist_places = tourist_places.filter(destination_id=destination_id)

    context = {
        'tourist_places': tourist_places,
        'destinations': destinations,
        'selected_destination': destination_id
    }

    return render(request, 'adminPage/view_touristplace.html', context)


def admin_add_touristplace(request):

    destinations = Destination.objects.all()

    if request.method == "POST":

        destination_id = request.POST.get('destination')

        destination = Destination.objects.get(id=destination_id)

        TouristPlace.objects.create(
            destination=destination,
            name=request.POST.get('name'),
            image=request.FILES.get('image'),
            description=request.POST.get('description'),
            location=request.POST.get('location'),
            google_map_link=request.POST.get('google_map_link'),
            rating=request.POST.get('rating'),
            rating_count=request.POST.get('rating_count')
        )

        messages.success(
            request,
            "Tourist Place added successfully."
        )

        return redirect('admin_view_touristplace')

    return render(request,'adminPage/add_touristplace.html',{ 'destinations': destinations})

def admin_delete_touristplace(request, id):

    place = get_object_or_404(TouristPlace, id=id)
    place.delete()
    messages.success(request, "Tourist Place deleted successfully.")

    return redirect('admin_view_touristplace')

def admin_edit_touristplace(request, id):

    place = get_object_or_404(TouristPlace,id=id)

    destinations = Destination.objects.all()

    if request.method == "POST":

        place.destination = Destination.objects.get(id=request.POST.get('destination'))

        place.name = request.POST.get('name')
        place.description = request.POST.get('description')
        place.location = request.POST.get('location')
        place.google_map_link = request.POST.get('google_map_link')
        place.rating = request.POST.get('rating')
        place.rating_count = request.POST.get('rating_count')

        if request.FILES.get('image'):
            place.image = request.FILES.get('image')

        place.save()

        messages.success(request,"Tourist Place updated successfully.")

        return redirect('admin_view_touristplace')

    return render(request,'adminPage/edit_touristplace.html',{'place': place,'destinations': destinations})

def admin_view_hotels(request):
    places = TouristPlace.objects.all()

    place_id = request.GET.get('place')

    hotels = Hotel.objects.select_related('touristplace')

    if place_id:
        hotels = hotels.filter(touristplace_id=place_id)

    context = {
        'hotels': hotels,
        'places': places,
        'selected_place': place_id
    }

    return render(request, 'adminPage/view_hotel.html', context)


def admin_delete_hotel(request, id):

    hotel = get_object_or_404(Hotel, id=id)
    hotel.delete()

    messages.success(request, "Hotel deleted successfully.")

    return redirect('admin_view_hotels')

def add_hotel(request):

    places = TouristPlace.objects.all()

    if request.method == "POST":

        touristplace = TouristPlace.objects.get(id=request.POST.get('touristplace'))

        Hotel.objects.create(
            touristplace=touristplace,
            name=request.POST.get('name'),
            image=request.FILES.get('image'),
            rating=request.POST.get('rating'),
            rating_count=request.POST.get('rating_count'),
            price_per_night=request.POST.get('price_per_night'),
            location=request.POST.get('location'),
            adults=request.POST.get('adults'),
            children=request.POST.get('children'),
            available_rooms=request.POST.get('available_rooms'),
            check_in=request.POST.get('check_in'),
            check_out=request.POST.get('check_out'),
            google_map_link=request.POST.get('google_map_link')
        )

        return redirect('admin_view_hotels')

    return render(request,'adminPage/add_hotel.html',{'places': places})

def edit_hotel(request, id):

    hotel = get_object_or_404(Hotel, id=id)
    places = TouristPlace.objects.all()

    if request.method == "POST":

        hotel.touristplace = TouristPlace.objects.get(id=request.POST.get('touristplace'))

        hotel.name = request.POST.get('name')

        if request.FILES.get('image'):
            hotel.image = request.FILES.get('image')

        hotel.rating = request.POST.get('rating')
        hotel.rating_count = request.POST.get('rating_count')
        hotel.price_per_night = request.POST.get('price_per_night')
        hotel.location = request.POST.get('location')
        hotel.adults = request.POST.get('adults')
        hotel.children = request.POST.get('children')
        hotel.available_rooms = request.POST.get('available_rooms')
        hotel.check_in = request.POST.get('check_in')
        hotel.check_out = request.POST.get('check_out')
        hotel.google_map_link = request.POST.get('google_map_link')

        hotel.save()

        return redirect('admin_view_hotels')

    context = {
        'hotel': hotel,
        'places': places
    }

    return render(request,'adminPage/edit_hotel.html',context)

def admin_view_restuarant(request):

    places = TouristPlace.objects.all()
    place_id = request.GET.get('place')
    restaurant = Restaurant.objects.select_related('touristplace')

    if place_id:
        restaurant = restaurant.filter(touristplace_id=place_id)

    context = {
        'restaurant': restaurant,
        'places': places,
        'selected_place': place_id
    }

    return render(request, 'adminPage/view_restuarant.html', context)

def admin_delete_restuarant(request, id):

    restuarant = get_object_or_404(Restaurant, id=id)
    restuarant.delete()

    messages.success(request, "Restuarant deleted successfully.")

    return redirect('admin_view_restuarant')

def add_restaurant(request):

    places = TouristPlace.objects.all()

    if request.method == "POST":

        touristplace = TouristPlace.objects.get(
            id=request.POST.get('touristplace')
        )

        Restaurant.objects.create(
            touristplace=touristplace,
            name=request.POST.get('name'),
            image=request.FILES.get('image'),
            rating=request.POST.get('rating'),
            rating_count=request.POST.get('rating_count'),
            price_range=request.POST.get('price_range'),
            location=request.POST.get('location'),
            google_map_link=request.POST.get('google_map_link'),
            is_open=request.POST.get('is_open') == 'on',
            closing_time=request.POST.get('closing_time')
        )

        return redirect('admin_view_restuarant')

    return render(request,'adminPage/add_restuarant.html',{'places': places})

def edit_restaurant(request, id):

    restaurant = get_object_or_404(Restaurant, id=id)
    places = TouristPlace.objects.all()

    if request.method == "POST":

        restaurant.touristplace = TouristPlace.objects.get(id=request.POST.get('touristplace'))

        restaurant.name = request.POST.get('name')

        if request.FILES.get('image'):
            restaurant.image = request.FILES.get('image')

        restaurant.rating = request.POST.get('rating')
        restaurant.rating_count = request.POST.get('rating_count')
        restaurant.price_range = request.POST.get('price_range')
        restaurant.location = request.POST.get('location')
        restaurant.google_map_link = request.POST.get('google_map_link')
        restaurant.is_open = request.POST.get('is_open') == 'on'
        restaurant.closing_time = request.POST.get('closing_time')

        restaurant.save()

        return redirect('admin_view_restuarant')

    context = {
        'restaurant': restaurant,
        'places': places
    }

    return render(request,'adminPage/edit_restuarant.html',context)


########################################### USER MODULE ###########################################

##### Dashboards for User ######

@login_required
def user_dashboard(request):
    destinations = Destination.objects.all()

    if request.method == "POST":
        search = request.POST.get("search")
        if search:
            destinations = Destination.objects.filter(name__icontains=search)

    return render(request, 'user/user_dashboard.html', {'destinations': destinations})

##### Destination Detail View ######

def destination_detail(request, id):
    destination = get_object_or_404(Destination, id=id)

    tourist_places = destination.places.all()

    return render(request, 'user/destination_detail.html', {'destination': destination, 'tourist_places': tourist_places})

##### Tourist Place Detail View ######

def place_detail(request, id):
    place = get_object_or_404(TouristPlace, id=id)

    # Dummy data (you can replace with API later)
    restaurants = place.restaurants.all()
    hotels = place.hotels.all()

    return render(request, 'user/tourplace_details.html', {'place': place,'restaurants': restaurants,'hotels': hotels})

####  About and Contact Views #####

def about(request):
    return render(request, 'user/about.html')

def contact(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(
            request,
            "Your message has been sent successfully."
        )

        return redirect('contact')

    return render(request, 'user/contact.html')

##### Packages View #####

def packages(request):
    packages = Package.objects.all()
    return render(request, 'user/packages.html', {'packages': packages})

##### Package Booking #####

def package_booking(request, id):

    package = get_object_or_404(Package, id=id)

    if request.method == "POST":

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        adults = int(request.POST.get('adults',1))
        children = int(request.POST.get('children',0))
        total_amount = request.POST.get('total_amount')

        Booking.objects.create(
            user=request.user,
            package=package,
            full_name=full_name,
            email=email,
            phone=phone,
            adults=adults,
            children=children,
            total_amount=total_amount
        )

        messages.success(request, "Package booked successfully")

    return render(
        request, 'user/package_booking.html', { 'package': package})
