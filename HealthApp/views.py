from django.shortcuts import render, redirect,  get_object_or_404
from HealthApp.models import ContactDB, RegisterDB, CommunityPost,Reply,PostVote,ExerciseLog,GratitudeEntry, Comment, ChallengeProgress, JournalEntry, Question,Response, Appointment, Booking
from AdminApp.models import ContentDB,MindfulnessExercise, Challenge, MeditationSession,Recipe, GratitudePrompt, AromatherapySuggestion, ExerciseRoutine, NutritionalTip
from DoctorApp.models import DoctorRegisterDB, Event
from django.contrib import messages
import uuid
import pytz
from django.db.models import Sum,Avg, Min
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth.models import User
from datetime import timedelta
from datetime import date
from django.utils import timezone
from collections import defaultdict
from django.http import Http404
from django.utils.timezone import now
from .decorators import login_required_custom

# Create your views here.

def homepage(request):
    return render(request, "Home.html")

def aboutus(request):
    return render(request, "AboutUs.html")

def services(request):
    return render(request, "Services.html")

def contact(request):
    return render(request, "Contact.html")


def contact_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        msg = request.POST.get('message')

        obj = ContactDB(Name=name, Email=email, Message=msg)
        obj.save()
        messages.success(request, "Message send successfully!")
        return redirect(contact)


def faqs(request):
    return render(request, "FAQs.html")


def user_register_page(request):
    return render(request, "User_Registration.html")


def register_details(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        img = request.FILES.get('image')

        if password1 == password2:
            user = RegisterDB.objects.create(
                Username=username,
                Email=email,
                Password1=password1,
                Password2=password2,
                Image=img
            )
            messages.success(request, "Registered successfully!Now you can login")
            return redirect('user_login_page')
        else:
            messages.error(request, "Passwords do not match!")
    return render(request, "User_Registration.html")


def user_login_page(request):
    # Check if user is already logged in, redirect to homepage
    if 'username' in request.session:
        return redirect('homepage')  # Redirect to homepage if already logged in
    return render(request, "User_Login.html")


def UserLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Fetch user from RegisterDB using the correct field name (Username)
            user = RegisterDB.objects.get(Username=username)

            # Check if the password matches
            if user.Password1 == password:  # Assuming plain text password
                # Manually log the user in by setting a session variable
                request.session['username'] = user.Username  # Save user in session
                messages.success(request, "Login successful!")
                return redirect('dashboard_view')  # Redirect after successful login
            else:
                messages.warning(request, "Invalid password.")
        except RegisterDB.DoesNotExist:
            messages.warning(request, "User not found.")

    return render(request, 'User_Login.html')



def user_logout(request):
    if 'username' in request.session:
        del request.session['username']  # Remove the user from the session
    messages.success(request, "You have been logged out.")
    return redirect('UserLogin')



def dashboard_view(request):
    if 'username' in request.session:
        username = request.session['username']

        try:
            register = RegisterDB.objects.get(Username=username)
        except RegisterDB.DoesNotExist:
            register = None

        # Get the latest journal entry for the user
        latest_journal = JournalEntry.objects.filter(user=register).order_by('-date_created').first()

        # Aggregate responses to get average stress levels for each screening
        screenings = Response.objects.filter(user=register).values('screening_id').annotate(
            average_stress=Avg('stress_level')
        ).order_by('-screening_id')

        # Prepare data for the chart
        dates = []
        stress_levels = []
        ist = pytz.timezone('Asia/Kolkata')

        for screening in screenings:
            screening_id = screening['screening_id']
            average_stress = screening['average_stress']
            first_response = Response.objects.filter(user=register, screening_id=screening_id).order_by('created_at').first()
            if first_response:
                screening_date = first_response.created_at.astimezone(ist).strftime('%Y-%m-%d %H:%M:%S')
                dates.append(screening_date)
                stress_levels.append(average_stress)

        # Get the latest 3 appointments
        latest_appointments = Appointment.objects.filter(username=username).order_by('-date')[:3]

        # Get all event bookings made by the user
        event_bookings = Booking.objects.filter(username=username).select_related('event').order_by('-booking_date')

        # Prepare the context for rendering
        context = {
            'register': register,
            'latest_journal': latest_journal,
            'dates': dates,
            'stress_levels': stress_levels,
            'latest_appointments': latest_appointments,
            'event_bookings': event_bookings,
        }

        return render(request, 'Main_Home.html', context)
    else:
        return redirect('user_login_page')







def journal_page(request):
    return render(request, "Journal.html")



@login_required_custom
def save_journal(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        mood = request.POST.get('mood')
        image = request.FILES.get('image')

        if title and content and mood:
            username = request.session.get('username')
            if not username:
                messages.error(request, 'User not found in session.')
                return redirect('user_login_page')

            try:
                user = RegisterDB.objects.get(Username=username)
            except RegisterDB.DoesNotExist:
                messages.error(request, 'User not found.')
                return redirect('user_login_page')

            # Check if a journal entry already exists for the current date
            today = date.today()
            existing_journal = JournalEntry.objects.filter(user=user, date_created=today).first()

            if existing_journal:
                # If an entry already exists, display an alert message
                messages.warning(request, 'You have already submitted the journal for today. Please come back tomorrow.')
                return redirect('journal_page')
            else:
                # Create a new entry if none exists
                JournalEntry.objects.create(
                    user=user,
                    title=title,
                    content=content,
                    mood=mood,
                    image=image
                )
                messages.success(request, 'Your journal has been saved successfully!')

            return redirect('journal_page')
        else:
            messages.error(request, 'Please fill out all required fields.')

    return render(request, 'Journal.html')



def view_journal(request):
    username = request.session.get('username')

    if not username:
        return redirect('UserLogin')  # Redirect to login if not authenticated

    # Fetch user journals from the database
    journals = JournalEntry.objects.filter(user__Username=username).order_by('-date_created')

    return render(request, 'view_journal.html', {'journals': journals})


@login_required_custom
def delete_journal_entry(request, entry_id):
    username = request.session.get('username')

    if not username:
        return redirect('UserLogin')

    try:
        user = RegisterDB.objects.get(Username=username)
    except RegisterDB.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('view_journal')

    # Attempt to get the journal entry
    entry = get_object_or_404(JournalEntry, id=entry_id, user=user)

    entry.delete()
    messages.success(request, 'Journal entry deleted successfully!')
    return redirect('view_journal')  # Redirect to the journal view after deletion



@login_required_custom
def edit_profile(request):
    # Fetch the current user based on the session's username
    username = request.session.get('username')

    if not username:
        messages.error(request, "You need to log in to edit your profile.")
        return redirect('user_login_page')

    try:
        # Fetch the user's current details from the database
        user = RegisterDB.objects.get(Username=username)
    except RegisterDB.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('user_login_page')

    if request.method == "POST":
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_password1 = request.POST.get('password1')
        new_password2 = request.POST.get('password2')
        new_image = request.FILES.get('image')

        # Update user details if they are provided and valid
        if new_username and new_email:
            user.Username = new_username
            user.Email = new_email

            # If passwords are provided, update them; otherwise, keep the current password
            if new_password1 and new_password2:
                if new_password1 != new_password2:
                    messages.error(request, "Passwords do not match!")
                    return redirect('edit_profile')
                else:
                    user.Password1 = new_password1
                    user.Password2 = new_password2

            # Update profile image if a new image is uploaded
            if new_image:
                user.Image = new_image

            # Save the updated user profile
            user.save()

            # Update the session with the new username if it's changed
            request.session['username'] = user.Username

            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard_view')
        else:
            messages.error(request, "All fields except password are required")

    return render(request, 'Edit_profile.html', {'user': user})




def journal_detail(request, id):
    journal = get_object_or_404(JournalEntry, id=id)

    return render(request, 'journal_detail.html', {'journal': journal})


def stress_screening(request):
    return render(request, 'Stress_Screening.html')


def init_user_score(request):
    if 'user_score' not in request.session:
        request.session['user_score'] = 0
        request.session['current_question'] = 4  # Start from question ID 4
        request.session['screening_id'] = str(uuid.uuid4())  # Generate a unique screening_id
        request.session.modified = True



def start_screening(request):
    init_user_score(request)  # This will handle screening_id initialization
    return redirect('question_screening', question_id=request.session['current_question'])



def question_screening(request, question_id):
    # Get the question based on the primary key field 'id'
    question = get_object_or_404(Question, id=question_id)

    total_questions = 12
    current_question_number = question_id - 3  # Since your questions start from ID 4
    progress_percentage = (current_question_number / total_questions) * 100

    if request.method == 'POST':
        selected_option = request.POST.get('option')

        if selected_option:
            # Strip any leading or trailing spaces from the selected option
            selected_option = selected_option.strip()

            # Define the score for each option
            score = {
                'Not at all': 0,
                'Several days': 1,
                'More than half the days': 2,
                'Always': 3
            }

            # Update the user score based on the selected option
            user_score = score.get(selected_option, 0)
            request.session['user_score'] += user_score

            # Save the response to the database
            if 'username' in request.session:  # Ensure user is logged in
                username = request.session['username']
                user = RegisterDB.objects.get(Username=username)

                # Fetch the screening_id from the session (initialize at screening start)
                screening_id = request.session.get('screening_id', None)

                # Create and save the response with the screening_id
                response = Response(
                    question=question,
                    user_response=selected_option,
                    stress_level=user_score,  # Store the numeric value
                    user=user,
                    screening_id=screening_id  # Assign the screening_id
                )
                response.save()

            # Move to the next question
            next_question_id = question_id + 1

            if next_question_id <= 15:  # Assuming you have 15 questions in total
                request.session['current_question'] = next_question_id
                return redirect('question_screening', question_id=next_question_id)
            else:
                return redirect('screening_result')

    return render(request, 'Question.html', {'question': question, 'progress_percentage': progress_percentage})



def screening_result(request):
    total_score = request.session.get('user_score', 0)
    print(f'Total Score: {total_score}')

    # Logic to determine stress level based on total_score
    if total_score <= 10:
        stress_level = 'Low'
    elif total_score <= 22:
        stress_level = 'Moderate'
    else:
        stress_level = 'High'

    # Fetch the screening_id from the session
    screening_id = request.session.get('screening_id', None)

    # No need to update the responses again with the total score
    # They already have individual scores in the 'stress_level' field

    # Safely delete session keys
    if 'user_score' in request.session:
        del request.session['user_score']
    if 'current_question' in request.session:
        del request.session['current_question']
    if 'screening_id' in request.session:
        del request.session['screening_id']

    return render(request, 'Screening_Result.html', {
        'total_score': total_score,
        'stress_level': stress_level
    })



def resources_view(request):
    # Get the filter parameter from the request (e.g., Blog, Article, etc.)
    filter_type = request.GET.get('filter', 'All')

    # If 'All' is selected, show all resources, otherwise filter by ContentType
    if filter_type == 'All':
        resources = ContentDB.objects.all()
    else:
        resources = ContentDB.objects.filter(ContentType=filter_type)

    # Render the template with the filtered resources
    context = {
        'resources': resources,
        'filter_type': filter_type,
    }
    return render(request, 'Resources.html', context)

def blog_detail(request, id):
    blog = get_object_or_404(ContentDB, id=id)
    return render(request, 'Resource_Single.html', {'blog': blog})


def team_view(request):
    professionals = DoctorRegisterDB.objects.filter(is_approved=True)  # Only get approved doctors
    return render(request, 'Support_Circle.html', {'professionals': professionals})


def doctor_detail(request, id):
    doctor = get_object_or_404(DoctorRegisterDB, id=id)
    return render(request, 'Doctor_Detail.html', {'doctor': doctor})

def doctor_appointment(request):
    return render(request, "Doctor_Appointment.html")


def make_appointment(request, doctor_id):
    if request.method == 'POST':
        # Extract form data
        username = request.session.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        age = request.POST.get('age')
        date = request.POST.get('date')
        time = request.POST.get('time')
        message = request.POST.get('message')

        try:
            doctor = DoctorRegisterDB.objects.get(id=doctor_id)
            # Save the appointment
            appointment = Appointment(
                username=username,
                email=email,
                mobile=mobile,
                age=age,
                date=date,
                time=time,
                message=message,
                doctor=doctor
            )
            appointment.save()

            # Redirect to a success page
            return redirect('appointment_success')
        except DoctorRegisterDB.DoesNotExist:
            # Handle error if doctor doesn't exist
            return redirect('doctor_detail', id=doctor_id)  # Pass the doctor_id back to the detail view

    # Handle GET requests
    else:
        try:
            doctor = DoctorRegisterDB.objects.get(id=doctor_id)
            return render(request, 'Doctor_Appointment.html', {'doctor': doctor})  # Render the appointment form
        except DoctorRegisterDB.DoesNotExist:
            return redirect('doctor_detail', id=doctor_id)  # Redirect if doctor does not exist


def appointment_success(request):
    return render(request, 'Appointment_Success.html')


def event_list(request):
    events = Event.objects.all()  # Get all events from the database
    return render(request, 'Display_Events.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)  # Get the specific event
    return render(request, 'Event_Detail.html', {'event': event})


def book_seat(request, event_id):
    event = Event.objects.get(id=event_id)  # Fetch the event based on the ID

    if request.method == 'POST':
        # Extract form data manually from POST request
        username = request.session['username']  # Username from session
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')

        # Save the booking details
        booking = Booking(event=event, username=username, email=email, mobile=mobile)
        booking.save()

        # Redirect to a success page or confirmation page
        messages.success(request, "Successfully Registered..!")
        return redirect(event_list)
    # Render the booking form page
    return render(request, 'Book_a_Seat.html', {'event': event})


def mindfulness_intro(request):
    return render(request, 'Mindfulness_intro.html')


def calm_music_view(request):
    calm_musics = MindfulnessExercise.objects.filter(category='calm_music')
    return render(request, 'Calm_music_page.html', {'calm_musics': calm_musics})


def visual_mindfulness(request):
    visualization_exercises = MindfulnessExercise.objects.filter(category='visualization_exercise')
    return render(request, 'Visualization_exercises_page.html', {'visualization_exercises': visualization_exercises})


def view_visualization_video(request, exercise_id):
    # Fetch the specific exercise using the exercise_id
    exercise = get_object_or_404(MindfulnessExercise, id=exercise_id)

    # Render the video player page and pass the exercise object
    return render(request, 'view_visualization_video.html', {'exercise': exercise})


def community_home(request):
    username = request.session.get('username')
    user = RegisterDB.objects.get(Username=username)

    posts = CommunityPost.objects.all()
    user_votes = PostVote.objects.filter(user=user).values_list('post_id', flat=True)  # List of post IDs user has liked

    return render(request, 'Community_Home.html', {
        'posts': posts,
        'user_votes': user_votes,  # Pass this list to the template
    })



def create_post(request):
    if 'username' not in request.session:
        return redirect('user_login_page')

    if request.method == 'POST':
        user = RegisterDB.objects.get(Username=request.session['username'])  # Fetch user by username
        title = request.POST['title']  # Get the title from the form
        text = request.POST['text']
        image = request.FILES.get('image', None)  # Get image if uploaded

        # Validate that title and text are not empty
        if not title.strip() or not text.strip():
            return render(request, 'Create_Post.html', {
                'error_message': 'Both title and text are required.',
            })

        # Create a new post
        post = CommunityPost(author=user, title=title, text=text)  # Include title here
        if image:
            post.image = image
        post.save()

        return redirect('community_home')  # Redirect to the community page after saving the post

    return render(request, 'Create_Post.html')



def add_comment(request, post_id):
    if 'username' not in request.session:
        return redirect('user_login_page')

    post = get_object_or_404(CommunityPost, id=post_id)
    user = RegisterDB.objects.get(Username=request.session['username'])

    if request.method == 'POST':
        comment_text = request.POST['comment_text']
        Comment.objects.create(post=post, author=user, comment_text=comment_text)

    return redirect('community_home')  # Redirect to the community home after adding comment


def comment_detail(request, post_id):
    if 'username' not in request.session:
        return redirect('user_login_page')

    post = get_object_or_404(CommunityPost, id=post_id)
    comments = post.comments.all()  # Get all comments related to the post
    replies = post.replies.all()  # Get all replies related to the post (since replies are now tied to posts)

    reply_count = replies.count()  # Count the number of replies for the post

    if request.method == 'POST':
        user = RegisterDB.objects.get(Username=request.session['username'])
        reply_text = request.POST.get('reply_content')

        # Create a new reply for the post
        Reply.objects.create(post=post, author=user, reply_text=reply_text)

        return redirect('comment_detail', post_id=post.id)  # Use comment_detail, not post_detail

    return render(request, 'Comment.html', {
        'post': post,
        'comments': comments,
        'replies': replies,
        'reply_count': reply_count,  # Pass reply count to the template
    })


def add_reply(request, comment_id):
    if 'username' not in request.session:
        return redirect('user_login_page')

    comment = get_object_or_404(Comment, id=comment_id)
    user = RegisterDB.objects.get(Username=request.session['username'])

    if request.method == 'POST':
        reply_text = request.POST['reply_content']
        Reply.objects.create(comment=comment, author=user, reply_text=reply_text)

    return redirect('comment_detail', post_id=comment.post.id)


def vote_post(request, post_id):
    username = request.session.get('username')

    # Fetch the user from RegisterDB using the session username
    user = get_object_or_404(RegisterDB, Username=username)

    # Fetch the post the user is trying to like
    post = get_object_or_404(CommunityPost, id=post_id)

    # Check if the user has already voted on this post
    existing_vote = PostVote.objects.filter(user=user, post=post).exists()

    if not existing_vote:
        # If the user has not already liked the post, create a like and update the vote count
        PostVote.objects.create(user=user, post=post)
        post.votes += 1  # Increment the post's vote count
        post.save()
        return JsonResponse({'liked': True})

    # Return a response indicating the user already liked the post
    return JsonResponse({'liked': False})


def user_has_voted(request,post_id):
    if 'username' not in request.session:
        return False
    user = RegisterDB.objects.get(Username=request.session['username'])
    return PostVote.objects.filter(user=user, post_id=post_id).exists()


def delete_post(request, post_id):
    if 'username' not in request.session:
        return redirect('user_login_page')

    # Get the post and the logged-in user
    post = get_object_or_404(CommunityPost, id=post_id)
    user = RegisterDB.objects.get(Username=request.session['username'])

    # Only allow the author of the post to delete it
    if post.author == user:
        post.delete()  # Delete the post
        messages.success(request, "Successfully Deleted your Comment")
        return redirect('community_home')  # Redirect to the community home after deletion

    return redirect('community_home')


def self_care_intro(request):
    return render(request, "Self_care_intro.html")


def user_meditation_list(request):
    sessions = MeditationSession.objects.all()
    return render(request, 'User_Guided_Meditation.html', {'sessions': sessions})


def user_meditation_detail(request, session_id):
    session = MeditationSession.objects.get(id=session_id)

    return render(request, 'User_meditation_Detail.html', {'session': session})


def aromatherapy_suggestions(request):
    oils = AromatherapySuggestion.objects.all()
    return render(request, 'Aromatherapy_suggestions.html', {'oils': oils})


def aromatherapy_detail(request, oil_id):
    oil = get_object_or_404(AromatherapySuggestion, id=oil_id)

    # Split benefits and instructions into lists
    oil.benefits_list = [benefit.strip() for benefit in oil.benefits.split(',')]
    oil.usage_instructions_list = [instruction.strip() for instruction in oil.usage_instructions.split(',')]

    return render(request, 'Aromatherapy_Detail.html', {'oil': oil})


def list_exercise_routines(request):
    # Check if the user is logged in using their username stored in session
    if not request.session.get('username'):
        return redirect('login')  # Redirect to login if not logged in

    # Fetch the logged-in user from RegisterDB based on the username in session
    try:
        user = RegisterDB.objects.get(Username=request.session['username'])
    except RegisterDB.DoesNotExist:
        return redirect('login')  # Redirect if the user is not found

    # Fetch all exercises
    exercises = ExerciseRoutine.objects.all()

    # Iterate through exercises and calculate progress for each
    for exercise in exercises:
        completed_logs = ExerciseLog.objects.filter(
            user=user, exercise=exercise
        ).count()
        exercise.progress = min((completed_logs / 10) * 100, 100)  # Example progress calculation

    # Render the template with exercises
    return render(request, 'Exercise_Routine.html', {'exercises': exercises})


def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(ExerciseRoutine, id=exercise_id)
    return render(request, 'Exercise_Detail_User.html', {'exercise': exercise})


@csrf_exempt  # Disable CSRF just for this example
def log_exercise(request, exercise_id):
    if request.method == 'POST':
        # Check if the user is logged in using their username stored in session
        if not request.session.get('username'):
            return JsonResponse({'success': False, 'message': 'User not logged in'})

        # Fetch the logged-in user from RegisterDB based on the username in session
        try:
            user = RegisterDB.objects.get(Username=request.session['username'])
        except RegisterDB.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})

        try:
            exercise = ExerciseRoutine.objects.get(id=exercise_id)
            # Log the completed exercise for the user
            ExerciseLog.objects.create(user=user, exercise=exercise)
            print(f'Logged exercise: {exercise.name} for user: {user.Username}')  # Debug print
            return JsonResponse({'success': True})
        except ExerciseRoutine.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Exercise not found'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})



def workout_logs(request):
    # Check if the user is logged in using their username stored in session
    if not request.session.get('username'):
        return JsonResponse([], safe=False)  # Return empty if not logged in

    # Fetch the logged-in user from RegisterDB based on the username in session
    try:
        user = RegisterDB.objects.get(Username=request.session['username'])
    except RegisterDB.DoesNotExist:
        return JsonResponse([], safe=False)  # Return empty if user not found

    logs = ExerciseLog.objects.filter(user=user)  # Get all logs for the user

    events = []
    for log in logs:
        events.append({
            'title': log.exercise.name,  # Display the exercise name
            'start': log.date_completed.isoformat(),  # Use date completed for calendar
            'description': f'Logged {log.exercise.name}.',  # Add description for each exercise
        })

    return JsonResponse(events, safe=False)



def nutritional_tips_list(request):
    tips = NutritionalTip.objects.all().order_by('-date')  # Fetch all tips, latest first
    return render(request, 'User_Nutrition_List.html', {'tips': tips})


def nutritional_tip_detail(request, tip_id):
    tip = get_object_or_404(NutritionalTip, id=tip_id)
    return render(request, 'Nutritional_tip_Detail.html', {'tip': tip})


def user_recipe_list(request):
    recipes = Recipe.objects.all()  # Fetch all recipes from the database
    return render(request, 'Recipe_list_User.html', {'recipes': recipes})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    # Split ingredients and instructions into lists
    recipe.ingredients_list = [ingredient.strip() for ingredient in recipe.ingredients.split(',')]
    recipe.instructions_list = [instruction.strip() for instruction in recipe.instructions.split(',')]
    recipe.nutrition_info_list = [info.strip() for info in recipe.nutrition_info.split(',')]

    return render(request, 'Recipe_Detail_User.html', {'recipe': recipe})


def gratitude_practice_page(request):
    # Fetch the username from the session
    username = request.session.get('username')

    # Ensure the user exists
    user = RegisterDB.objects.filter(Username=username).first()
    if not user:
        messages.error(request, "User not found.")
        return redirect('login_page')  # Redirect to login or an appropriate page

    # Get the current week number
    current_week = timezone.now().isocalendar()[1]

    # Filter prompts for the current week
    prompts = GratitudePrompt.objects.filter(week_number=current_week)

    if request.method == "POST":
        prompt_id = request.POST.get('prompt')
        entry_text = request.POST.get('entry_text')

        # Check if the checkbox was ticked
        challenge_completed = 'challenge_completed' in request.POST

        # Validate if a valid prompt is selected
        if not prompt_id or prompt_id == 'Select':
            messages.error(request, "Please select a valid prompt.")
            return redirect('gratitude_practice_page')

        # Create and save the gratitude entry
        gratitude_entry = GratitudeEntry.objects.create(
            prompt_id=prompt_id,
            user=user,
            entry_text=entry_text,
            challenge_completed=challenge_completed  # Save the challenge status
        )
        messages.success(request, "Successfully Saved...")
        return redirect('gratitude_practice_page')

    return render(request, 'Gratitude_Practice_Page.html', {'prompts': prompts})






def gratitude_entries_page(request):
    username = request.session.get('username')
    user = RegisterDB.objects.get(Username=username)

    # Fetch all gratitude entries for the logged-in user
    entries = GratitudeEntry.objects.filter(user=user)

    return render(request, 'Gratitude_Entries_Page.html', {'entries': entries})



def gratitude_intro_page(request):
    return render(request,"Gratitude_Intro.html")

def challenges_page(request):
    # Get the current date
    current_date = timezone.now().date()

    Challenge.objects.filter(end_date__lt=current_date).delete()

    challenges = Challenge.objects.all().order_by('start_date')

    return render(request, 'Challenges_page.html', {'challenges': challenges})

def challenge_detail(request, challenge_id):
    user = RegisterDB.objects.get(Username=request.session['username'])
    challenge = get_object_or_404(Challenge, pk=challenge_id)

    # Calculate completed tasks and total tasks
    challenge_progress = ChallengeProgress.objects.filter(challenge=challenge, user=user)
    completed_tasks = challenge_progress.filter(completed=True).count()
    total_tasks = (challenge.end_date - challenge.start_date).days + 1
    completed_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    user_participating = ChallengeProgress.objects.filter(user=user, challenge=challenge).exists()

    return render(request, 'Challenge_Detail.html', {
        'challenge': challenge,
        'challenge_progress': challenge_progress,
        'completed_tasks': completed_tasks,
        'total_tasks': total_tasks,
        'completed_percentage': completed_percentage,
        'user_participating': user_participating,
    })

def toggle_challenge(request, challenge_id):
    user = RegisterDB.objects.get(Username=request.session['username'])
    challenge = get_object_or_404(Challenge, pk=challenge_id)

    # Check if user is already participating
    if ChallengeProgress.objects.filter(user=user, challenge=challenge).exists():
        ChallengeProgress.objects.filter(user=user, challenge=challenge).delete()  # Leave challenge
    else:
        # Join challenge (create progress entries for all days)
        start_date = challenge.start_date
        end_date = challenge.end_date

        # Make sure the start and end dates are valid
        if start_date and end_date:
            while start_date <= end_date:
                ChallengeProgress.objects.create(user=user, challenge=challenge, date=start_date)
                start_date += timedelta(days=1)

    return redirect('challenge_detail', challenge_id=challenge_id)

def mark_task_complete(request, challenge_id, progress_id):
    # Get the user from the session
    user = RegisterDB.objects.get(Username=request.session['username'])

    # Get the specific challenge progress entry
    challenge_progress = get_object_or_404(ChallengeProgress, pk=progress_id, user=user, challenge__id=challenge_id)

    # Get the current date
    current_date = timezone.now().date()

    # Check if the task date is today
    if challenge_progress.date == current_date:
        # Mark the task as complete if it's the correct day
        challenge_progress.completed = True
        challenge_progress.save()
    else:
        # If the user is trying to mark a task for a different day, show a warning message
        messages.error(request, "You can only mark the task as complete on the actual day.")

    return redirect('challenge_detail', challenge_id=challenge_id)
