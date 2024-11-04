from django.urls import path
from HealthApp import views

urlpatterns = [
    path("",views.homepage,name="homepage"),
    path("aboutus/",views.aboutus,name="aboutus"),
    path("services/",views.services,name="services"),
    path("contact/",views.contact,name="contact"),
    path("contact_form/",views.contact_form,name="contact_form"),
    path("faqs/",views.faqs,name="faqs"),

    path("user_register_page/",views.user_register_page,name="user_register_page"),
    path("UserLogin/",views.UserLogin,name="UserLogin"),
    path("register_details/",views.register_details,name="register_details"),
    path("user_login_page/",views.user_login_page,name="user_login_page"),
    path("user_logout/",views.user_logout,name="user_logout"),

    path("dashboard_view/",views.dashboard_view,name="dashboard_view"),
    path("edit_profile/",views.edit_profile,name="edit_profile"),
    path("journal_detail/<int:id>/",views.journal_detail,name="journal_detail"),

    path("journal_page/",views.journal_page,name="journal_page"),
    path("save_journal/",views.save_journal,name="save_journal"),
    path("view_journal/",views.view_journal,name="view_journal"),
    path('delete_journal/<int:entry_id>/', views.delete_journal_entry, name='delete_journal_entry'),

    path('stress_screening/', views.stress_screening, name='stress_screening'),
    path('start_screening/', views.start_screening, name='start_screening'),
    path('question_screening/<int:question_id>/', views.question_screening, name='question_screening'),
    path('screening_result/', views.screening_result, name='screening_result'),

    path('resources_view/', views.resources_view, name='resources_view'),
    path('blog_detail/<int:id>/', views.blog_detail, name='blog_detail'),

    path('team_view/', views.team_view, name='team_view'),
    path('doctor_detail/<int:id>/', views.doctor_detail, name='doctor_detail'),
    path('doctor_appointment', views.doctor_appointment, name='doctor_appointment'),
    path('make_appointment/<int:doctor_id>/', views.make_appointment, name='make_appointment'),
    path('appointment_success', views.appointment_success, name='appointment_success'),

    path('event_list', views.event_list, name='event_list'),
    path('event_detail/<int:event_id>/', views.event_detail, name='event_detail'),
    path('book_seat/<int:event_id>/', views.book_seat, name='book_seat'),

    path('mindfulness_intro/', views.mindfulness_intro, name='mindfulness_intro'),
    path('calm_music_view/', views.calm_music_view, name='calm_music_view'),
    path('visual_mindfulness/', views.visual_mindfulness, name='visual_mindfulness'),
    path('view-visualization-video/<int:exercise_id>/', views.view_visualization_video, name='view_visualization_video'),

    path('community_home/', views.community_home, name='community_home'),
    path('create_post', views.create_post, name='create_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment_detail/<int:post_id>/', views.comment_detail, name='comment_detail'),
    path('vote_post/<int:post_id>/', views.vote_post, name='vote_post'),
    path('user_has_voted/<int:post_id>/', views.user_has_voted, name='user_has_voted'),
    path('add_reply/<int:comment_id>/', views.add_reply, name='add_reply'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),  # URL for deleting a post

    path('self_care_intro/', views.self_care_intro, name='self_care_intro'),

    path('user_meditation_list/', views.user_meditation_list, name='user_meditation_list'),
    path('user_meditation_detail/<int:session_id>/', views.user_meditation_detail, name='user_meditation_detail'),

    path('aromatherapy/', views.aromatherapy_suggestions, name='aromatherapy_suggestions'),
    path('aromatherapy/<int:oil_id>/', views.aromatherapy_detail, name='aromatherapy_detail'),

    path('list_exercise_routines/', views.list_exercise_routines, name='list_exercise_routines'),
    path('exercise_detail/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('log_exercise/<int:exercise_id>/', views.log_exercise, name='log_exercise'),
    path('workout_logs/', views.workout_logs, name='workout_logs'),

    path('nutritional_tips_list/', views.nutritional_tips_list, name='nutritional_tips_list'),
    path('nutritional_tip_detail/<int:tip_id>/', views.nutritional_tip_detail, name='nutritional_tip_detail'),

    path('user_recipe_list/', views.user_recipe_list, name='user_recipe_list'),
    path('recipe_detail/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),

    path('gratitude_practice_page', views.gratitude_practice_page, name='gratitude_practice_page'),
    path('gratitude_intro_page', views.gratitude_intro_page, name='gratitude_intro_page'),
    path('gratitude-entries_page/', views.gratitude_entries_page, name='gratitude_entries_page'),

    path('challenges/', views.challenges_page, name='challenges_page'),
    path('challenge_detail/<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
    path('toggle_challenge/<int:challenge_id>/', views.toggle_challenge, name='toggle_challenge'),
    path('mark_task_complete/<int:challenge_id>/<int:progress_id>/', views.mark_task_complete, name='mark_task_complete'),

]