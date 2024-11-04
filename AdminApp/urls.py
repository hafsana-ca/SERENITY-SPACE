from django.urls import path
from AdminApp import views

urlpatterns = [
    path("index_page/",views.index_page,name="index_page"),
    path("content_page/",views.content_page,name="content_page"),
    path("add_content/",views.add_content,name="add_content"),
    path("view_content/",views.view_content,name="view_content"),
    path("edit_content/<int:co_id>/",views.edit_content,name="edit_content"),
    path("delete_content/<int:co_id>/",views.delete_content,name="delete_content"),
    path("update_content/<int:data_id>/",views.update_content,name="update_content"),

    path("contact_pg/",views.contact_pg,name="contact_pg"),
    path("view_contact/",views.view_contact,name="view_contact"),
    path("delete_contact/<int:dr_id>/",views.delete_contact,name="delete_contact"),

    path("admin_login_page/",views.admin_login_page,name="admin_login_page"),
    path("admin_login/",views.admin_login,name="admin_login"),
    path("admin_logout/",views.admin_logout,name="admin_logout"),

    path("add_question/",views.add_question,name="add_question"),
    path("questions_list/",views.questions_list,name="questions_list"),
    path("delete_question/<int:dr_id>/",views.delete_question,name="delete_question"),

    path('manage_doctors/', views.manage_doctors, name='manage_doctors'),
    path('approve_doctor/<int:doctor_id>/', views.approve_doctor, name='approve_doctor'),
    path('reject_doctor/<int:doctor_id>/', views.reject_doctor, name='reject_doctor'),
    path("view_mental_health_pro/", views.view_mental_health_pro, name="view_mental_health_pro"),

    path("view_all_events/", views.view_all_events, name="view_all_events"),

    path('add_calm_music/', views.add_calm_music, name='add_calm_music'),
    path('view_music/', views.view_music, name='view_music'),
    path("delete_music/<int:dr_id>/",views.delete_music,name="delete_music"),
    path('add_mindfulness_exercise/', views.add_mindfulness_exercise, name='add_mindfulness_exercise'),
    path('view_visualization_exercises/', views.view_visualization_exercises, name='view_visualization_exercises'),
    path('delete_exercise/<int:dr_id>/', views.delete_exercise, name='delete_exercise'),

    path('add_meditation_session', views.add_meditation_session, name='add_meditation_session'),
    path('meditation_list', views.meditation_list, name='meditation_list'),
    path('delete_meditation/<int:dr_id>/', views.delete_meditation, name='delete_meditation'),
    path('edit_meditation_session/<int:co_id>/', views.edit_meditation_session, name='edit_meditation_session'),
    path('update_meditation_session/<int:co_id>/', views.update_meditation_session, name='update_meditation_session'),

    path('add_aromatherapy_suggestion', views.add_aromatherapy_suggestion, name='add_aromatherapy_suggestion'),
    path('list_aromatherapy_suggestions', views.list_aromatherapy_suggestions, name='list_aromatherapy_suggestions'),
    path('delete_therapy/<int:dr_id>/', views.delete_therapy, name='delete_therapy'),
    path('edit_therapy/<int:co_id>/', views.edit_therapy, name='edit_therapy'),
    path('update_therapy/<int:co_id>/', views.update_therapy, name='update_therapy'),

    path('add_exercise', views.add_exercise, name='add_exercise'),
    path('exercise_list', views.exercise_list, name='exercise_list'),
    path('delete_selfcare_exercise/<int:dr_id>/', views.delete_selfcare_exercise, name='delete_selfcare_exercise'),
    path('edit_exercise/<int:co_id>/', views.edit_exercise, name='edit_exercise'),
    path('update_exercise/<int:co_id>/', views.update_exercise, name='update_selfcare_exercise'),

    path('add_gratitude_prompt', views.add_gratitude_prompt, name='add_gratitude_prompt'),
    path('view_gratitude_prompts', views.view_gratitude_prompts, name='view_gratitude_prompts'),
    path('delete_gratitude_prompts/<int:dr_id>/', views.delete_gratitude_prompts, name='delete_gratitude_prompts'),
    path('edit_gratitude_prompt/<int:co_id>/', views.edit_gratitude_prompt, name='edit_gratitude_prompt'),
    path('update_gratitude_prompt/<int:dr_id>/', views.update_gratitude_prompt, name='update_gratitude_prompt'),

    path('add_challenge', views.add_challenge, name='add_challenge'),
    path('challenge_list', views.challenge_list, name='challenge_list'),
    path('delete_challenge/<int:dr_id>/', views.delete_challenge, name='delete_challenge'),
    path('edit_challenge/<int:co_id>/', views.edit_challenge, name='edit_challenge'),
    path('update_challenge/<int:dr_id>/', views.update_challenge, name='update_challenge'),

    path('add_nutritional_tip', views.add_nutritional_tip, name='add_nutritional_tip'),
    path('list_nutritional_tips', views.list_nutritional_tips, name='list_nutritional_tips'),
    path('delete_nutritional_tips/<int:dr_id>/', views.delete_nutritional_tips, name='delete_nutritional_tips'),
    path('edit_nutritional_tips/<int:co_id>/', views.edit_nutritional_tips, name='edit_nutritional_tips'),
    path('update_nutritional_tips/<int:data_id>/', views.update_nutritional_tips, name='update_nutritional_tips'),

    path('add_recipe', views.add_recipe, name='add_recipe'),
    path('recipe_list', views.recipe_list, name='recipe_list'),
    path('delete_recipe/<int:dr_id>/', views.delete_recipe, name='delete_recipe'),
    path('edit_recipe/<int:co_id>/', views.edit_recipe, name='edit_recipe'),
    path('update_recipe/<int:data_id>/', views.update_recipe, name='update_recipe'),

]

