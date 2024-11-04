from django.shortcuts import render, redirect, get_object_or_404
from AdminApp.models import ContentDB, MindfulnessExercise,NutritionalTip,Recipe, MeditationSession,Challenge, AromatherapySuggestion, ExerciseRoutine, GratitudePrompt
from HealthApp.models import ContactDB, Question
from DoctorApp.models import DoctorRegisterDB, Event
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.utils import timezone

# Create your views here.

def index_page(request):
    return render(request, "Index.html")

def content_page(request):
    return render(request, "ContentManagement.html")

def add_content(request):
    if request.method == "POST":

        image = request.FILES['Image']
        title = request.POST.get('Title')
        content_type = request.POST.get('Content_Type')
        content = request.POST.get('Content')
        category = request.POST.get('Category')
        author = request.POST.get('Author')


        obj = ContentDB(Image=image, Title=title, ContentType=content_type, Content=content, Category=category, Author=author)
        obj.save()
        return redirect(content_page)

    else:
        return render(request, "ContentManagement.html")

def view_content(request):
    data = ContentDB.objects.all()
    return render(request, "View_Contents.html", {'data':data})

def edit_content(request,co_id):
    data = ContentDB.objects.get(id=co_id)
    return render(request,"Update_Contents.html", {'data':data})

def delete_content(request,co_id):
    x = ContentDB.objects.filter(id=co_id)
    x.delete()
    return redirect(view_content)

def update_content(request,data_id):
    if request.method == "POST":
        try:
            img = request.FILES['Image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = ContentDB.objects.get(id=data_id).Image
        title = request.POST.get('Title')
        content_type = request.POST.get('Content_Type')
        content = request.POST.get('Content')
        category = request.POST.get('Category')
        author = request.POST.get('Author')

        ContentDB.objects.filter(id=data_id).update(Image=file, Title=title, ContentType=content_type, Content=content, Category=category, Author=author)
        return redirect(view_content)

def contact_pg(request):
    return render(request, "Contact_Details.html")

def view_contact(request):
    print("View is being called!")  # Debugging print statement
    data = ContactDB.objects.all()
    print("Contact Data: ", data)  # Debugging to see if data is fetched
    return render(request, "Contact_Details.html", {'data': data})


def delete_contact(request,dr_id):
    x = ContactDB.objects.filter(id=dr_id)
    x.delete()
    return redirect(view_contact)

def admin_login_page(request):
    return render(request, "Admin_Login.html")

def admin_login(request):
    if request.method == "POST":
        un = request.POST.get('username')
        pwd = request.POST.get('password')

        user = authenticate(request, username=un, password=pwd)

        if user is not None and user.is_staff:  # Check if the user is a staff/admin
            login(request, user)  # Django's built-in login function
            request.session['username'] = user.username  # Store username in session
            messages.success(request, "Login Successful!")
            return redirect('index_page')  # Redirect after successful login
        else:
            messages.warning(request, "Invalid username or password")
            return redirect('admin_login_page')  # Redirect back to login on failure

    return render(request, 'Admin_Login.html')


def admin_logout(request):
    request.session.flush()  # Clears all session data
    logout(request)
    return redirect('admin_login_page')

def questions_list(request):
    questions = Question.objects.all()
    return render(request, 'Question_List.html', {'questions': questions})


def add_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question')
        options_text = request.POST.get('options')

        # Split options by comma
        options = options_text.split(',')

        # Create the Question object
        new_question = Question.objects.create(text=question_text, options=options)
        new_question.save()

        return redirect('add_question')  # Redirect to a list of questions or wherever appropriate

    return render(request, 'Add_Question.html')

def delete_question(request,dr_id):
    x = Question.objects.filter(id=dr_id)
    x.delete()
    return redirect(questions_list)

def manage_doctors(request):
    doctors = DoctorRegisterDB.objects.all()  # Fetch all doctors
    return render(request, 'Pending_Doctors.html', {'doctors': doctors})

def approve_doctor(request, doctor_id):
    doctor = DoctorRegisterDB.objects.get(id=doctor_id)
    doctor.is_approved = True
    doctor.save()
    return redirect(view_mental_health_pro)

def reject_doctor(request, doctor_id):
    doctor = DoctorRegisterDB.objects.get(id=doctor_id)
    doctor.delete()  # Or mark them as rejected
    return redirect(view_mental_health_pro)


def view_mental_health_pro(request):
    data = DoctorRegisterDB.objects.all()
    return render(request, "Pending_Doctors.html", {'data':data})


def view_all_events(request):
    events = Event.objects.all()
    return render(request, 'Admin_View_Events.html', {'events': events})


def add_calm_music(request):
    if request.method == 'POST':
        # Retrieve form data
        title = request.POST.get('title')
        description = request.POST.get('description')

        # Retrieve files
        cover_image = request.FILES.get('cover_image')
        media_file = request.FILES.get('media_file')  # Can be audio or video file

        # Ensure the title is not empty
        if not title:
            return HttpResponse("Title is required", status=400)

        # Ensure at least one media file (cover or music file) is provided
        if not cover_image and not media_file:
            return HttpResponse("At least one file (cover image or media file) is required", status=400)

        # Create and save the object to the MindfulnessExercise model
        MindfulnessExercise.objects.create(
            title=title,
            cover_image=cover_image,
            media_file=media_file,
            description=description,
            category='calm_music'
        )

        # Redirect after successful submission
        return redirect('add_calm_music')

    # Render the form template if it's a GET request
    return render(request, 'Add_calm_music.html')


def view_music(request):
    data = MindfulnessExercise.objects.all()
    return render(request, "View_Music.html", {'data':data})


def delete_music(request,dr_id):
    x = MindfulnessExercise.objects.filter(id=dr_id)
    x.delete()
    return redirect(view_music)


def add_mindfulness_exercise(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        cover_image = request.FILES.get('cover_image')
        media_file = request.FILES.get('media_file')
        description = request.POST.get('description')

        # Save to MindfulnessExercise model with category 'visualization_exercise'
        MindfulnessExercise.objects.create(
            title=title,
            cover_image=cover_image,
            media_file=media_file,
            description=description,
            category='visualization_exercise'  # Hardcode the category for this form
        )
        return redirect('add_mindfulness_exercise')  # Redirect after successful submission

    return render(request, 'Add_visualization_exercise.html')


def view_visualization_exercises(request):
    # Fetch all exercises categorized as 'visualization_exercise'
    exercises = MindfulnessExercise.objects.filter(category='visualization_exercise')

    context = {
        'exercises': exercises
    }
    return render(request, 'view_visualization_exercises.html', context)


def delete_exercise(request,dr_id):
    x = MindfulnessExercise.objects.filter(id=dr_id)
    x.delete()
    return redirect(view_visualization_exercises)


def add_meditation_session(request):
    if request.method == "POST":
        # Retrieve form data
        title = request.POST['title']
        description = request.POST['description']
        duration = request.POST['duration']
        media_type = request.POST['media_type']
        media_url = request.POST['media_url']
        image = request.FILES.get('image')


        # Create and save the new meditation session
        MeditationSession.objects.create(
            title=title,
            description=description,
            duration=duration,
            media_type=media_type,
            media_url=media_url,
            image=image
        )
        return redirect('add_meditation_session')  # Redirect to the list view after submission

    return render(request, 'Add_Meditation_Session.html')


def meditation_list(request):
    sessions = MeditationSession.objects.all()
    return render(request, 'View_Meditation.html', {'sessions': sessions})


def edit_meditation_session(request, co_id):
    data = get_object_or_404(MeditationSession, id=co_id)
    return render(request, "Update_Guided_Meditation_Session.html", {'data': data})


def update_meditation_session(request, co_id):
    if request.method == "POST":
        data = AromatherapySuggestion.objects.get(id=co_id)


        # Get the updated fields from the form
        title = request.POST['title']
        description = request.POST['description']
        duration = request.POST['duration']
        media_type = request.POST['media_type']
        media_url = request.POST['media_url']
        try:
            img = request.FILES['image']  # Check if a new image is uploaded
            fs = FileSystemStorage()
            file = fs.save(img.name, img)  # Save the uploaded image
        except MultiValueDictKeyError:
            file = data.image  # If no new image, use the existing one

        # Update the exercise in the database
        MeditationSession.objects.filter(id=co_id).update(
            title=title,
            description=description,
            duration=duration,
            media_type=media_type,
            media_url=media_url,
            image=file
        )

        return redirect('meditation_list')


def delete_meditation(request,dr_id):
    x = MeditationSession.objects.filter(id=dr_id)
    x.delete()
    return redirect(meditation_list)




def add_aromatherapy_suggestion(request):
    if request.method == 'POST':
        oil_name = request.POST.get('oil_name')
        description = request.POST.get('description')
        benefits = request.POST.get('benefits')
        usage_instructions = request.POST.get('usage_instructions')
        recommended_time = request.POST.get('recommended_time')
        stress_level = request.POST.get('stress_level')
        image = request.FILES.get('image')  # Handle image upload

        # Create a new aromatherapy suggestion
        new_suggestion = AromatherapySuggestion(
            oil_name=oil_name,
            description=description,
            benefits=benefits,
            usage_instructions=usage_instructions,
            recommended_time=recommended_time,
            stress_level=stress_level,
            image=image
        )
        new_suggestion.save()

        return redirect('add_aromatherapy_suggestion')  # Redirect after saving

    return render(request, 'Add_aromatherapy.html')


def list_aromatherapy_suggestions(request):
    suggestions = AromatherapySuggestion.objects.all()
    return render(request, 'View_aromatherapy.html', {'suggestions': suggestions})

def delete_therapy(request,dr_id):
    x = AromatherapySuggestion.objects.filter(id=dr_id)
    x.delete()
    return redirect(list_aromatherapy_suggestions)



def edit_therapy(request, co_id):
    data = get_object_or_404(AromatherapySuggestion, id=co_id)
    return render(request, "Update_therapy_Form.html", {'data': data})


# Handle the POST request for updating the exercise details
def update_therapy(request, co_id):
    if request.method == "POST":
        data = AromatherapySuggestion.objects.get(id=co_id)


        # Get the updated fields from the form
        oil_name = request.POST.get('oil_name')
        description = request.POST.get('description')
        benefits = request.POST.get('benefits')
        usage_instructions = request.POST.get('usage_instructions')
        recommended_time = request.POST.get('recommended_time')
        stress_level = request.POST.get('stress_level')
        try:
            img = request.FILES['image']  # Check if a new image is uploaded
            fs = FileSystemStorage()
            file = fs.save(img.name, img)  # Save the uploaded image
        except MultiValueDictKeyError:
            file = data.image  # If no new image, use the existing one


        # Update the exercise in the database
        AromatherapySuggestion.objects.filter(id=co_id).update(
            oil_name=oil_name,
            description=description,
            benefits=benefits,
            usage_instructions=usage_instructions,
            recommended_time=recommended_time,
            stress_level=stress_level,
            image=file

        )

        return redirect('list_aromatherapy_suggestions')




def add_exercise(request):
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        target_areas = request.POST['target_areas']
        recommended_time = request.POST['recommended_time']
        equipment = request.POST['equipment']
        duration = request.POST['duration']
        difficulty = request.POST['difficulty']
        instructions = request.POST['instructions']
        video_url = request.POST.get('video_url', '')
        image = request.FILES.get('image')

        # Save the new exercise routine to the database
        exercise = ExerciseRoutine(
            name=name,
            category=category,
            target_areas=target_areas,
            recommended_time=recommended_time,
            equipment=equipment,
            duration=duration,
            difficulty=difficulty,
            instructions=instructions,
            video_url=video_url,
            image=image
        )
        exercise.save()

        return redirect('add_exercise')  # Redirect to the exercise list after submission

    return render(request, 'Exercise_Form.html')


def exercise_list(request):
    exercises = ExerciseRoutine.objects.all()
    return render(request, 'View_Exercise.html', {'exercises': exercises})

def delete_selfcare_exercise(request,dr_id):
    x = ExerciseRoutine.objects.filter(id=dr_id)
    x.delete()
    return redirect(exercise_list)


def edit_exercise(request, co_id):
    data = get_object_or_404(ExerciseRoutine, id=co_id)
    return render(request, "Update_Exercise_Form.html", {'data': data})


# Handle the POST request for updating the exercise details
def update_exercise(request, co_id):
    if request.method == "POST":
        data = ExerciseRoutine.objects.get(id=co_id)

        try:
            img = request.FILES['image']  # Check if a new image is uploaded
            fs = FileSystemStorage()
            file = fs.save(img.name, img)  # Save the uploaded image
        except MultiValueDictKeyError:
            file = data.image  # If no new image, use the existing one

        # Get the updated fields from the form
        name = request.POST.get('name')
        category = request.POST.get('category')
        target_areas = request.POST.get('target_areas')
        recommended_time = request.POST.get('recommended_time')
        equipment = request.POST.get('equipment')
        duration = request.POST.get('duration')
        difficulty = request.POST.get('difficulty')
        instructions = request.POST.get('instructions')
        video_url = request.POST.get('video_url')

        # Update the exercise in the database
        ExerciseRoutine.objects.filter(id=co_id).update(
            image=file,
            name=name,
            category=category,
            target_areas=target_areas,
            recommended_time=recommended_time,
            equipment=equipment,
            duration=duration,
            difficulty=difficulty,
            instructions=instructions,
            video_url=video_url
        )

        return redirect('exercise_list')


def gratitude_practice_page(request):
    current_week = timezone.now().isocalendar()[1]  # Get the current week number
    prompts = GratitudePrompt.objects.filter(week_number=current_week)  # Filter by current week
    return render(request, "Add_Gratitude_prompt.html", {'prompts': prompts, 'current_week': current_week})


def add_gratitude_prompt(request):
    current_week = timezone.now().isocalendar()[1]  # Get current week number
    if request.method == "POST":
        prompt = request.POST.get('prompt')
        challenge = request.POST.get('challenge')
        week_number = request.POST.get('week_number') or current_week

        # Create and save the new GratitudePrompt
        new_prompt = GratitudePrompt(prompt=prompt, challenge=challenge, week_number=week_number)
        new_prompt.save()

        return redirect('view_gratitude_prompts')  # Redirect after adding
    return render(request, "Add_Gratitude_prompt.html", {'current_week': current_week})


def view_gratitude_prompts(request):
    prompts = GratitudePrompt.objects.all()  # Fetch all gratitude prompts
    return render(request, "View_Gratitude_Prompts.html", {'prompts': prompts})


def delete_gratitude_prompts(request,dr_id):
    x = GratitudePrompt.objects.filter(id=dr_id)
    x.delete()
    return redirect(view_gratitude_prompts)


def edit_gratitude_prompt(request,co_id):
    data = GratitudePrompt.objects.get(id=co_id)
    return render(request,"Updating_Prompt.html", {'data':data})


def update_gratitude_prompt(request, dr_id):
    if request.method == "POST":
        prompt = request.POST.get('prompt')
        challenge = request.POST.get('challenge')
        week_number = request.POST.get('week_number')  # Capture the week number from the form

        # Update the prompt, challenge, and week_number fields
        GratitudePrompt.objects.filter(id=dr_id).update(prompt=prompt, challenge=challenge, week_number=week_number)
        return redirect(view_gratitude_prompts)  # Redirect to view the updated prompts
    else:
        data = GratitudePrompt.objects.get(id=dr_id)  # Fetch the prompt data to pre-fill the form
        return render(request, "Updating_Prompt.html", {'data': data})



def add_challenge(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        total_tasks = request.POST.get('total_tasks')

        # Create new Challenge
        Challenge.objects.create(
            name=name,
            description=description,
            duration=duration,
            start_date=start_date,
            end_date=end_date,
            total_tasks=total_tasks
        )
        return redirect('add_challenge')  # Redirect to the list of challenges
    return render(request, 'Challenge_Form.html')


def challenge_list(request):
    challenges = Challenge.objects.all()
    return render(request, 'View_Challenges.html', {'challenges': challenges})


def delete_challenge(request,dr_id):
    x = Challenge.objects.filter(id=dr_id)
    x.delete()
    return redirect(challenge_list)


def edit_challenge(request,co_id):
    data = Challenge.objects.get(id=co_id)
    return render(request,"Update_Challenges.html", {'data':data})


def update_challenge(request,dr_id):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        duration = request.POST.get('duration')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        total_tasks = request.POST.get('total_tasks')

        Challenge.objects.filter(id=dr_id).update(name=name, description=description,duration=duration,start_date=start_date,
                                                        end_date=end_date, total_tasks=total_tasks)
        return redirect(challenge_list)


def add_nutritional_tip(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        source = request.POST.get('source')
        source_url = request.POST.get('source_url')

        # Save the nutritional tip
        NutritionalTip.objects.create(
            title=title,
            description=description,
            category=category,
            image=image,
            source=source,
            source_url=source_url
        )
        return redirect('add_nutritional_tip')
    return render(request, 'Nutritional_Tip.html')


def list_nutritional_tips(request):
    tips = NutritionalTip.objects.all()
    return render(request, 'View_nutritional_tips.html', {'tips': tips})


def delete_nutritional_tips(request,dr_id):
    x = NutritionalTip.objects.filter(id=dr_id)
    x.delete()
    return redirect(list_nutritional_tips)


def edit_nutritional_tips(request,co_id):
    data = NutritionalTip.objects.get(id=co_id)
    return render(request,"Update_Nutrition.html", {'data':data})


def update_nutritional_tips(request,data_id):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = NutritionalTip.objects.get(id=data_id).image
        source = request.POST.get('source')
        source_url = request.POST.get('source_url')

        NutritionalTip.objects.filter(id=data_id).update(
            title=title,
            description=description,
            category=category,
            image=file,
            source=source,
            source_url=source_url)
        return redirect(list_nutritional_tips)


def add_recipe(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')
        nutrition_info = request.POST.get('nutrition_info')
        category = request.POST.get('category')
        preparation_time = request.POST.get('preparation_time')
        health_benefit = request.POST.get('health_benefit')
        image = request.FILES.get('image')

        # Save the recipe to the database
        Recipe.objects.create(
            title=title,
            ingredients=ingredients,
            instructions=instructions,
            nutrition_info=nutrition_info,
            category=category,
            preparation_time=preparation_time,
            health_benefit=health_benefit,
            image=image
        )
        return redirect('add_recipe')  # Redirect to a list of recipes or another page after saving

    return render(request, 'Add_Recipe.html')


def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'View_Recipe.html', {'recipes': recipes})


def delete_recipe(request,dr_id):
    x = Recipe.objects.filter(id=dr_id)
    x.delete()
    return redirect(recipe_list)


def edit_recipe(request,co_id):
    data = Recipe.objects.get(id=co_id)
    return render(request,"Update_Recipe_Admin.html", {'data':data})

def update_recipe(request,data_id):
    if request.method == "POST":
        title = request.POST.get('title')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')
        nutrition_info = request.POST.get('nutrition_info')
        category = request.POST.get('category')
        preparation_time = request.POST.get('preparation_time')
        health_benefit = request.POST.get('health_benefit')
        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = Recipe.objects.get(id=data_id).image

        Recipe.objects.filter(id=data_id).update(
            title=title,
            ingredients=ingredients,
            instructions=instructions,
            nutrition_info=nutrition_info,
            category=category,
            preparation_time=preparation_time,
            health_benefit=health_benefit,
            image=file
        )
        return redirect(recipe_list)
