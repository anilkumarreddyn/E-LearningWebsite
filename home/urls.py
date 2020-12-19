from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('about-us', views.home, name='about'),
    # path('contact-us', views.contact, name='contact'),
    # path('search', views.search, name='search'),
    path('courses', views.courses, name='courses'),
    path('courses/<str:subject>', views.subject_courses, name='subjectcourses'),
    path('courses/<str:course>/<str:chapter>', views.studyMaterials, name='study-materials'),
    path('courses/<str:course>/<str:chapter>/<str:video>', views.studyMaterialsWithVideos, name='study-materials-w-videos'),
    path('enrollment/', views.enroll_anonymous, name='enroll_anonymous'),
    path('enrollment/<str:username>', views.enrollment, name='enrollment'),
    path('enrollmentCheckout/<str:version>/<str:course>/<str:price>/<str:username>', views.enrollmentCheckout, name='enrollmentCheckout'),
    path('enrollmentCheckoutFail', views.enrollmentCheckoustFail, name='enrollmentCheckoutFail'),
    path('enrollmentConfirmation', views.enrollmentConfirmation, name='enrollmentConfirmation'),
    path('enrollmentCancel', views.enrollmentCheckoutCancelled, name='enrollmentCancelled'),
    path('quiz/<str:typee>/<str:course>/<str:slug>/<str:uname>', views.quizIndiv, name='quizIndiv'),
    path('quizIntro/<str:typee>/<str:course>/<str:slug>/<str:uname>', views.quizIntro, name='quizIndiv'),
    path('quiz/<str:typee>/<str:uname>', views.quizAll, name='quiz'),
    path('quiz/<str:typee>/', views.quiznotLogged, name='quizNotLogged'),
    path('answer-validate', views.quizAll, name='quiz'),
    path('comment/<str:course>/<str:chapter>/<str:video>/<str:uname>', views.comment, name='comment'),
    path('newsletter', views.newsletter, name='newsletter'),
    path('other-services/cvBuilder', views.cvBuilder, name='cvBuilder'),
    path('other-services/cvBuilderIntro', views.cvIntro, name='cvBuilderIntro'),
    path('search/study-materials-subs', views.searchStudyMaterialsSubs, name='searchStudyMaterialsSubs'),
    path('search/quizzes', views.searchQuizzes, name='searchQuizzes'),

    # path('search/study-materials', views.searchStudyMaterials, name='searchStudyMaterials'),
    # path('reply-comment/<str:course>/<str:chapter>/<str:video>/<str:uname>/<str:comment_id>', views.replyComment, name='comment')

    

    # path('administrative', views.search, name='administrative'),
    # path('admission', views.search, name='admission'),
    # path('instructors', views.search, name='instructors'),
    # path('exam', views.search, name='exam'),

]
