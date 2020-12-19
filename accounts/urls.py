from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('confirmRegistration/<str:uname>', views.confirmRegistration, name='confirmRegistration'),
    path('teacher-reg', views.teacherReg, name='teacherReg'),
    path('logout', views.logout, name='logout'),
    path('user-dashboard/<str:uname>', views.userDashboard, name='user-dashboard'),
    path('user-edit-info/<str:uname>', views.userEditInfo, name='user-edit-info'),
    path('security-settings/<str:uname>', views.securitySettings, name='security-settings'),
    path('change-password/<str:uname>', views.changePassword, name='changePassword'),
    path('delete-user/<str:uname>', views.deleteUser, name='deleteAccount'),
    path('adminPanel', views.adminPanel, name='adminPanel'),
    path('confirmTeacher/<str:username>', views.confirmTeacher, name='confirmTeacher'),
    path('deleteApplicant/<str:username>', views.deleteApplicant, name='deleteApplicant'),
    path('deleteTeacher/<str:username>', views.deleteTeacher, name='deleteTeacher'),
    path('deleteStudent/<str:username>', views.deleteStudent, name='deleteStudent'),
    path('fileComplaint/<str:uname>', views.fileComplaint, name='fileComplaint'),
    path('addContent/<str:subj>/<str:uname>', views.addContent, name='addContent'),
    path('addQuestion/<str:subj>/<str:uname>', views.addQuestion, name='addQuestion'),
    path('addCourse', views.addCourse, name='addCourse'),
    path('send_mail_newsletter', views.send_mail_newsletter, name='send_mail_newsletter'),
] 
