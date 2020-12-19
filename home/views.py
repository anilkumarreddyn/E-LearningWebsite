from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from accounts.models import *
from django.contrib import messages
import ast
from datetime import datetime
import random
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal


# Create your views here.
def home(request):
    iconList = ["fas fa-exclamation-triangle", "fas fa-flag-checkered", "fas fa-exclamation-circle"]
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        message = request.POST.get('message')

        contact = Contacts(fname=fname, lname=lname, contact=contact, email=email, message=message)
        contact.save()
        messages.success(request, 'We have recieved your message successfully. We may contact you back if needed.')

    notices = noticeBoard.objects.all()
    params = {'notices': notices, 'icons': iconList}

    return render(request, 'index.html', params)

def courses(request):
    subsall = AllSubjects.objects.all()
    chap = ChapterList.objects.all()
    params = {'subjects': subsall, 'chapters': chap}
    return render(request, 'study-materials.html', params)

def subject_courses(request, subject):
    subsall = AllSubjects.objects.all()
    subs = AllSubjects.objects.get(slug=subject)
    chap = ChapterList.objects.filter(subj=subs.name)
    params = { 'subjects': subsall, 'chapters': chap, 'name': subs.name}
    return render(request, 'study-materials-subs.html', params)
    # print(chap)
    # return HttpResponse(chap)


def studyMaterials(request, course, chapter):
    subs = AllSubjects.objects.get(slug=course)
    content = allContent.objects.filter(subj=subs.name, chapSlug=chapter)   
    params = {'content':content}
    video = content.values_list('videoID', flat=True)[0]
    
    return redirect('/courses/'+str(course)+'/'+str(chapter)+'/'+str(video))
    # return HttpResponse(content.values_list('videoID', flat=True)[0])


def searchStudyMaterialsSubs(request):
    subsall = AllSubjects.objects.all()
    content = ChapterList.objects.all()
    if request.method == 'GET':
        searchInput = request.GET['search']
        results = ChapterList.objects.filter(name__icontains=searchInput)
        results2 = ChapterList.objects.filter(subj__icontains=searchInput)
        resultsFinal = results.values('name', 'no', 'subj', 'subjSlug', 'slug')
        results2Final = results2.values('name', 'no', 'subj', 'subjSlug', 'slug')

        if results.exists():
            params = {'subjects': subsall, 'chapters': resultsFinal}
            return render(request, 'searchStudyMaterials.html', params)
        if results2.exists():
            params = {'subjects': subsall, 'chapters': results2Final}
            return render(request, 'searchStudyMaterials.html', params)
        else:
            messages.success(request,'No search results found :-(')
            return redirect('/')

def searchQuizzes(request):
    quizzes = QuizChapterList.objects.all()
    # QuizChapterList.objects.get()
    subsall = AllSubjects.objects.all()
    if request.method == 'GET':
        searchInput = request.GET['search']
        results = QuizChapterList.objects.filter(name__icontains=searchInput)
        results2 = QuizChapterList.objects.filter(subj__icontains=searchInput)
        resultsFinal = results.values('name', 'no', 'subj', 'subjSlug', 'slug')
        results2Final = results2.values('name', 'no', 'subj', 'subjSlug', 'slug')

        if results.exists():
            params = {'subjects': subsall, 'chapters': resultsFinal}
            return render(request, 'searchQuizzes.html', params)
        if results2.exists():
            params = {'subjects': subsall, 'chapters': results2Final}
            return render(request, 'searchQuizzes.html', params)
        else:
            messages.success(request,'No search results found :-(')
            return redirect('/')



def studyMaterialsWithVideos(request, course, chapter, video):
    comments = Comments.objects.filter(subject=course, chapter=chapter, video=video)
    # replies = comments.values_list('replies', flat=True) #Not in need currently
    # replies = Replies.objects.filter(subject=course, video=video, chapter=chapter, comment_id=comments.comment_id)     
    subs = AllSubjects.objects.get(slug=course)
    content1 =allContent.objects.filter(subj=subs.name, chapSlug=chapter) 
    content = allContent.objects.filter(subj=subs.name, chapSlug=chapter, videoID=video)   
    params = {'content':content, 'content1': content1, 'comments': comments}
             
    return render(request, 'study-materials-w-vids.html', params)
    

def quizIntro(request, typee, course, slug, uname):
    rand = random.randint(11111111, 999999999)
    return render(request, 'quizIntro.html', {'type': typee, 'course':course, 'uname':uname, 'course_elong': AllSubjects.objects.get(slug=course), 'slug':slug, 'chap': QuizChapterList.objects.get(slug=slug), 'rand':rand})


def quizIndiv(request, typee, course, slug, uname):
    userall = AllUsers.objects.get(username=uname)
    if request.user.is_authenticated and request.user.username == uname and userall.accounts_type == 'Student':
        student = Student.objects.get(username=uname)
        status = ''
        point = 0
        n = 0
        if typee == 'miniQuiz':
            n = 10
        elif typee == 'megaQuiz':
            n = 35
        elif typee == 'ultraQuiz':
            n = 50
        questBank = QuestionBank.objects.filter(subject=course, chapSlug=slug)
        listt = []
        listt2 = []
        for i in questBank:
            
            listt.append(str(i).split(' || '))
        for l in listt:
            l[4] = ast.literal_eval(str(l[4]))
            listt2.append(l)
        listt3 = random.shuffle(listt2)
        print(listt2)

        student = Student.objects.get(username=request.user.username)
        
        if request.method == 'POST':
            backend = request.POST.get('backend')
            answer = ast.literal_eval(backend)
            for key, value in answer.items():
                ques = QuestionBank.objects.get(quesID=int(key))
                if ques.answer == value:
                    point = point + 1
                else:
                    pass
            
            if (point/n*100) >= 35:
                status = 'Pass'
            elif (point/n*100) < 35:
                status == 'Fail'
            
            if student.points == '':
                student.points = point
                student.save()
            else:
                student.points = int(student.points) + point
                student.save()

            
            if student.quizAttended == '':
                student.quizAttended = 1
                student.save()
            else :
                student.quizAttended = int(student.quizAttended) + 1
                student.save()
            

            resultList = ast.literal_eval(str(student.results))
            resultList.append(point/n*100)
            student.results = resultList
            student.save()
            successRate = sum(resultList)/len(resultList)
            # successRate = average/len(resultList)*100
            student.successRate = successRate
            student.save()
            return render(request, 'result.html', {'point':point, 'point_percentage': point/n*100, 'status':status, 'n': len(listt2[0:n]), 'total_points': student.points, 'successRate': successRate})
            # return HttpResponse(rand)

        params = {'questions': questBank, 'questions2': listt2[0:n], 'n': len(listt2[0:n]), 'course':course, 'slug':slug}
        return render(request, 'quizMain.html', params)
    else:
        messages.error(request, 'Please log in as a student first!')
        return redirect('/accounts/login')

def quizAll(request, typee, uname):
    subsall = AllSubjects.objects.all()
    chap = QuizChapterList.objects.all()
    params = {'subjects': subsall, 'chapters': chap}
    return render(request, 'quizAll.html', params)

def enroll_anonymous(request):
    messages.error(request, 'Please log in as a student first.')
    return redirect('/accounts/login')

def quiznotLogged(request, typee):
    messages.error(request, 'Please log in as a student to continue.')
    return redirect("/accounts/login")

def enrollment(request, username):
    userall = AllUsers.objects.get(username=username)
    if request.user.is_authenticated and request.user.username == username and userall.accounts_type == 'Student':
                    
        subjects = Courses.objects.all()
        students = Student.objects.get(username=username)
        
        if request.method == 'POST':
            version = request.POST.get('version')
            subject = request.POST.get('subject')

            desiredCourse = Courses.objects.get(slug=subject)

            if Enrollment.objects.filter(uname=username, subject=desiredCourse.slug).exists():
                messages.info(request,'You are already enrolled in this course')
                return redirect('/enrollment/'+str(username))
            else:

                # integration part
                mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id='naser5f87eff1ddede', sslc_store_pass='naser5f87eff1ddede@ssl')
                mypayment.set_urls(
                    success_url='http://'+str(request.META['HTTP_HOST'])+'/enrollmentCheckout/'+str(version)+'/'+str(subject)+'/2000/'+str(username), 
                    fail_url='http://'+str(request.META['HTTP_HOST'])+'/enrollmentCheckoutFail',
                    cancel_url='http;://'+str(request.META['HTTP_HOST'])+'/enrollmentCancel', 
                    ipn_url=str(request.META['HTTP_HOST'])+'/enrollmentConfirmation'
                    ) 
                mypayment.set_product_integration(total_amount=Decimal(desiredCourse.price), currency='BDT', product_category='Course', product_name=subject, num_of_item=1, shipping_method='YES', product_profile='None')
                mypayment.set_customer_info(name=students.fname + ' ' + students.lname, email=students.email, address1='Address', address2='Address', city='Dhaka', postcode='2231', country='Bangladesh', phone=students.contact)
                mypayment.set_shipping_info(shipping_to=students.fname + ' ' + students.lname, address='Address', city='Dhaka', postcode='1209', country='Bangladesh')
                response_data = mypayment.init_payment()
                print(response_data)

                return redirect(response_data['GatewayPageURL'])
                # return HttpResponse(desiredCourse)

    else:
        messages.success(request, 'Please log in as a student')
        return redirect('/accounts/login')
        # return HttpResponse(students.enrolled)
    params = {'subjects': subjects}
    return render(request, 'course-admission.html', params)
    # return HttpResponse(request.META['HTTP_HOST']+request.path)

@csrf_exempt
def enrollmentConfirmation(request):
    print('CONFIRMEDDDDDDD!!!!!')
    return HttpResponse('Confirmation')

@csrf_exempt
def enrollmentCheckout(request, version, course, price, username):
    userall = AllUsers.objects.get(username=username)
    if userall.accounts_type == 'Student':
        subjects = Courses.objects.all()
        students = Student.objects.get(username=username)

        subj = Courses.objects.get(slug=course)
        link = subj.link
        enroll = Enrollment(
            name=str(students.fname)+' '+str(students.lname),
            contact=students.contact, 
            uname=username,
            version=version, 
            time=datetime.now().strftime('%m/%d/%Y, %H:%M:%S'), 
            subject=course,
            link=link
            )
        enroll.save()

        course = Courses.objects.get(slug=course)
        if course.totStudents == '':
            course.totStudents = 1
            course.save()
        else:
            course.totStudents = int(course.totStudents) + 1
            course.save()

        students.enrolled = int(students.enrolled) + 1
        students.save()

        messages.success(request, 'You have successfully enrolled in this program!')
        params = {'version':'You have successfully enrolled in ' + course.name + '. Your version is '+version + ' and price is '+str(price) + ' BDT. You can view the course details in your dashboard.', 'status': 'Congratulations!'}
        return render(request, 'enrollmentNews.html', params)

@csrf_exempt
def enrollmentCheckoustFail(request):
    params = {'version':'Transanction failed for some reason. Please check your balance or try again later, If it still does not work, contact us.', 'status':'Sorry!'}
    return render(request, 'enrollmentNews.html', params)


@csrf_exempt
def enrollmentCheckoutCancelled(request):
    return render(request, 'enrollmentNews.html')


def comment(request, course, chapter, video, uname):
    if request.method == 'GET':
        content = allContent.objects.get(videoID=video)
        comments = Comments.objects.all()
        if content.comments == '':
            commentDict = {}
        elif content.comments == 'None':
            commentDict = {}
        else:
            commentDict = ast.literal_eval(content.comments)

        commentt = request.GET.get('comment')
        commentDict[str(uname) + ' at ' + datetime.now().strftime('%m/%d/%Y, %H:%M:%S')] = commentt
        content.comments = commentDict
        content.save()

        commentdata = Comments(subject=course, username=uname, comment=commentt, chapter=chapter, video=video, datetime=datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))
        commentdata.save()


    return redirect('/courses/'+str(course)+'/'+str(chapter)+'/'+str(video))
    # return HttpResponse([values for key, values in commentDict.items()])


def replyComment(request, course, chapter, video, uname, comment_id):
    commentt = Comments.objects.get(id=comment_id)
    if commentt.replies == '' or commentt.replies == 'None' or commentt.replies is None:
        replyDict = {}
    else:
        replyDict = ast.literal_eval(commentt.replies)
    
    if request.method == 'GET':
        reply = request.GET.get('reply')
        replyData = Replies(subject=course, username=uname, video=video, chapter=chapter, datetime=datetime.now().strftime('%m/%d/%Y, %H:%M:%S'), comment_id=comment_id, reply=reply)
        replyData.save()

        replyDict[uname + '; ' + datetime.now().strftime('%m/%d/%Y, %H:%M:%S') + '; ' + comment_id] = reply
        commentt.replies = str(replyDict)
        commentt.save()

    return redirect('/courses/'+str(course)+'/'+str(chapter)+'/'+str(video))


def newsletter(request):
    if request.method == 'GET':
        email = request.GET['email']
        submit = Newsletter(email=email)
        submit.save()
    messages.success(request, 'You have successfully subscribed to our newsletter. We will keep you updated.')
    return redirect('/')


def cvIntro(request):
    return render(request, 'cv-intro.html')


def cvBuilder(request):
    CV.objects.all().delete()
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        birthdate = request.POST.get('bday')
        address = request.POST.get('address')
        p_address = request.POST.get('p-address')
        fname = request.POST.get('fname')
        mname = request.POST.get('mname')
        nationality = request.POST.get('nationality')
        religion = request.POST.get('religion')
        bloodgroup = request.POST.get('bloodgroup')
        job_obj = request.POST.get('job-obj')
        skillsbackend = request.POST.get('skillsbackend')
        skills = skillsbackend.split(',')
        expbackend = request.POST.get('expbackend')
        exp = expbackend.split(',')
        edubackend = request.POST.get('edubackend')
        edu2 = '['+edubackend+']'
        edus = ast.literal_eval(edu2)
        imgg = request.FILES['img']

        cv = CV(email=email, img=imgg)
        cv.save()
        temp = CV.objects.get(email=email)

        params = {
            'name': name,
            'contact': contact,
            'email': email,
            'birthdate': birthdate,
            'address': address,
            'p_address': p_address,
            'fname': fname,
            'mname': mname,
            'nationality': nationality,
            'religion': religion,
            'bloodgroup': bloodgroup,
            'job_obj': job_obj,
            'skills': skills,
            'exp': exp,
            'edus': edus,
            'img': temp.img
        }
        messages.success(request, 'Please print the webpage pressing Ctrl+P an save as a PDF.')
        return render(request, 'cvBuilder.html', params)
        
    messages.success(request, 'Please Fill up the foloowing form')
    return render(request, 'cv-Form.html')



def cvBuilderEnd(request):
        return render(request, 'cvBuilder.html')
