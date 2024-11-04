from django.shortcuts import render,redirect, get_object_or_404
from DoctorApp.models import DoctorRegisterDB, Event
from HealthApp.models import Booking,Appointment
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from datetime import datetime


def doctor_home(request):
    events = Event.objects.all()
    # Check if the user is logged in based on session
    if 'username' in request.session:
        try:
            doctor = DoctorRegisterDB.objects.get(username=request.session['username'])
            return render(request, 'Doctor_Home.html', {'doctor': doctor,'events':events})
        except DoctorRegisterDB.DoesNotExist:
            return redirect('doctor_register')
    else:
        return redirect('dr_login')



def dr_register_page(request):
    return render(request, "Doctor_Registration.html")

def doctor_register(request):
    if request.method == 'POST':
        # Capture the form data
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        location = request.POST.get('location')
        gender = request.POST.get('gender')
        img = request.FILES.get('image')
        specialization = request.POST.get('specialization')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        license_no = request.POST.get('license_no')
        pwd1 = request.POST.get('password1')
        pwd2 = request.POST.get('password2')
        institution = request.POST.get('institution')
        availability = request.POST.get('availability')
        bio = request.POST.get('bio')

        # Save the form data
        new_doctor = DoctorRegisterDB(
            name=name,
            username=username,
            email=email,
            location=location,
            gender=gender,
            profile_picture=img,
            specialization=specialization,
            qualification=qualification,
            experience=experience,
            license_number=license_no,
            institution=institution,
            password1=pwd1,
            password2=pwd2,
            availability=availability,
            bio=bio,
            is_approved=False  # Set approval to false initially
        )
        new_doctor.save()

        messages.success(request, 'Registration Successful. Awaiting Admin Approval.')
        return redirect(doctor_home)

    return render(request, 'Doctor_Registration.html')


def dr_login_page(request):
    # # Check if user is already logged in, redirect to homepage
    if 'username' in request.session:
        return redirect(doctor_home)  # Redirect to homepage if already logged in
    return render(request, "Doctor_Login.html")


def dr_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Fetch doctor from DoctorRegisterDB using the correct field name (username)
            doctor = DoctorRegisterDB.objects.get(username=username)

            # Check if the password matches using password1
            if doctor.password1 == password:  # Assuming plain text password
                # Manually log the user in by setting a session variable
                request.session['username'] = doctor.username  # Save username in session
                request.session['doctor_id'] = doctor.id  # Store doctor_id in session
                messages.success(request, "Login successful!")
                return redirect('doctor_home')  # Redirect to doctor's home or dashboard
            else:
                messages.warning(request, "Invalid password.")
        except DoctorRegisterDB.DoesNotExist:
            messages.warning(request, "Doctor not found.")

    return render(request, 'Doctor_Login.html')




def dr_logout(request):
    if 'username' in request.session:
        del request.session['username']  # Remove the user from the session
    messages.success(request, "You have been logged out.")
    return redirect('dr_login')


def doctor_profile(request, doctor_id):
    doctor = get_object_or_404(DoctorRegisterDB, id=doctor_id)
    return render(request, 'Doctor_Profile.html', {'doctor': doctor})




def add_event(request):
    username = request.session.get('username')
    if not username:
        messages.error(request, 'You must be logged in to add an event.')
        return redirect('dr_login')  # Redirect to login if session is not found

    doctor = DoctorRegisterDB.objects.get(username=username)  # Get the doctor from session

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
        organizer = request.POST.get('organizer')
        organizer_info = request.POST.get('organizer_info')
        contact_email = request.POST.get('contact_email')
        cover_image = request.FILES.get('cover_image')

        # Create and save the event instance, organizer is set as the doctor
        event = Event(
            title=title,
            description=description,
            category=category,
            date=date,
            time=time,
            location=location,
            organizer=organizer,  # Use doctor's name as organizer
            organizer_info=organizer_info,
            contact_email=contact_email,
            cover_image=cover_image
        )
        print(cover_image)  # To check if it's correctly getting the image

        event.save()

        messages.success(request, 'Event added successfully!')
        return redirect(add_event)  # Redirect to doctor's events list after saving

    return render(request, 'Add_Events.html')


def doctor_events(request):
    if 'username' not in request.session:
        return redirect('dr_login')

    username = request.session['username']
    print(f"Current username: {username}")  # Debug print

    try:
        doctor = DoctorRegisterDB.objects.get(username=username)
    except DoctorRegisterDB.DoesNotExist:
        messages.warning(request, "Doctor not found.")
        return redirect('dr_login')

    # Fetch all events for this doctor, including past events
    events = Event.objects.filter(organizer=username)
    print(f"Number of events found: {events.count()}")  # Debug print

    # Fetch only future events
    future_events = events.filter(date__gte=datetime.now().date())
    print(f"Number of future events: {future_events.count()}")  # Debug print

    # Print details of each event
    for event in events:
        print(f"Event: {event.title}, Organizer: {event.organizer}")  # Debug print

    context = {
        'events': events,
        'future_events': future_events,
    }

    if not events.exists():
        messages.warning(request, "No events found for this doctor.")

    return render(request, 'View_Events.html', context)


def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, "Edit_Event.html", {'event': event})


def update_event(request, event_id):
    if request.method == "POST":
        # Handling file upload for cover image
        try:
            img = request.FILES['cover_image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = Event.objects.get(id=event_id).cover_image

        # Capture other fields
        title = request.POST.get('title')
        print("Title received from form: ", title)  # Debugging

        if not title:
            # You can add a message for empty title to debug further
            print("Title is empty or None")
            messages.error(request, "Title cannot be empty.")
            return redirect('edit_event', event_id=event_id)  # Redirect back to edit page if title is empty

        description = request.POST.get('description')
        category = request.POST.get('category')
        date = request.POST.get('date')
        time = request.POST.get('time')
        location = request.POST.get('location')
        organizer = request.POST.get('organizer')
        organizer_info = request.POST.get('organizer_info')
        contact_email = request.POST.get('contact_email')

        # Update the event in the database
        Event.objects.filter(id=event_id).update(
            title=title,
            description=description,
            category=category,
            date=date,
            time=time,
            location=location,
            organizer=organizer,
            organizer_info=organizer_info,
            contact_email=contact_email,
            cover_image=file
        )

        messages.success(request, 'Event updated successfully!')
        return redirect('doctor_events')  # Redirect to the event list after updating

    # Add error handling for GET requests or improper methods
    messages.error(request, "Invalid request method.")
    return redirect('doctor_events')


def delete_event(request, event_id):
    # Get the username from the session
    logged_in_username = request.session.get('username', None)

    # Check if the user is logged in
    if logged_in_username is None:
        messages.error(request, "You must be logged in to delete an event.")
        return redirect('login')  # Redirect to login if not logged in

    # Get the event by ID and ensure the organizer matches the session username
    event = get_object_or_404(Event, id=event_id, organizer=logged_in_username)

    # Delete the event
    event.delete()
    messages.success(request, "Event successfully deleted!")
    return redirect('doctor_events')  # Redirect back to the event list


def view_registered_users(request, event_id):
    # Get the event
    event = get_object_or_404(Event, id=event_id)

    # Get all bookings for the event
    bookings = Booking.objects.filter(event=event)

    # Render the registered users
    return render(request, 'View_event_registrations.html', {
        'event': event,
        'bookings': bookings
    })


def doctor_appointment(request):
    doctor_id = request.GET.get('doctor_id')  # Retrieve the doctor ID from the URL
    if doctor_id:
        try:
            doctor = DoctorRegisterDB.objects.get(id=doctor_id)  # Fetch the doctor instance
            context = {
                'doctor': doctor,  # Pass the doctor object to the template
            }
            return render(request, 'User_Appointments.html', context)  # Ensure correct template name
        except DoctorRegisterDB.DoesNotExist:
            # Handle the case where the doctor with the provided ID does not exist
            return redirect('doctor_home')
    else:
        # Handle the case where doctor_id is not provided
        return redirect('doctor_home')

def view_appointments(request):
    # Fetch the doctor from session or query based on logged-in doctor's info
    doctor_id = request.session.get('doctor_id')  # Assuming you store doctor_id in session
    if not doctor_id:
        return redirect('doctor_login')  # Redirect if the doctor is not logged in

    doctor = DoctorRegisterDB.objects.get(id=doctor_id)
    appointments = Appointment.objects.filter(doctor=doctor)  # Filter appointments for this doctor

    context = {
        'doctor': doctor,
        'appointments': appointments
    }

    return render(request, 'User_Appointments.html', context)


