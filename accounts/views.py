from django.shortcuts import render, redirect, HttpResponse
from home.models import *
from .models import *
from django.conf import settings
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
import random
from django.core.mail import send_mail
import smtplib, ast
from datetime import datetime


# Create your views here.

def register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipp = request.POST.get('zip')

        if (password == cpassword):
            if AllUsers.objects.filter(username=username).exists():
                messages.error(request, 'Username or Email already exists. Please select a different username or Email.')
                return redirect('/accounts/register')
            elif StudentsWithoutOTP.objects.filter(username=username).exists():
                messages.error(request, 'Username or Email already exists. Please select a different username or Email.')
                return redirect('/accounts/register')

            else:
                otp = random.randint(100000, 999999)
                studentsotp = StudentsWithoutOTP(
                                    fname=fname, lname=lname, contact=contact, 
                                    email=email, username=username, password=password, 
                                    address=str(city)+', '+str(state)+' - '+str(zipp),
                                    otp=otp
                                    )
                studentsotp.save()

                subject = 'Account Confirmation from Imperia Education'
                body = 'Your code for the email confirmation is ' + str(otp) + '. Enter the code in the verification page to verify your ID and activate your account.'
                message = subject + '\n' + body
                email_to = [email]
                
                obj = smtplib.SMTP('smtp.gmail.com', 587)
                obj.starttls()
                obj.login('abiralmahdi@gmail.com', 'Doors.290')
                obj.sendmail('abiralmahdi@gmail.com', email_to, message)
                params = {'username':username}
                return render(request, 'otp.html', params)

        else:
            messages.error(request, 'Your passwords does not match.')


    return render(request, 'signup.html')

def confirmRegistration(request, uname):
    if request.method == 'POST':
        code = request.POST.get('otp')

        studentsotp = StudentsWithoutOTP.objects.get(username=uname)
        if code == studentsotp.otp:

            user = User.objects.create_user(studentsotp.username, studentsotp.email, studentsotp.password)
            user.first_name = studentsotp.fname
            user.last_name = studentsotp.lname
            user.save()

            user2 = Student(
                            fname=studentsotp.fname, lname=studentsotp.lname, contact=studentsotp.contact, 
                            email=studentsotp.email, username=studentsotp.username, password=studentsotp.password, 
                            address=str(studentsotp.address),    
                            )
            user2.save()

            userall = AllUsers(
                fname=studentsotp.fname, lname=studentsotp.lname, contact=studentsotp.contact, 
                email=studentsotp.email, username=studentsotp.username, password=studentsotp.password, 
                accounts_type='Student'
            )
            userall.save()
            

            messages.success(request, 'You have created your account successfully!')
            
            user = auth.authenticate(username=studentsotp.username, password=studentsotp.password)
            auth.login(request, user)
            studentsotp.delete()
            messages.success(request, 'You have created your account successfully')
            return redirect('/')
        else:
            studentsotp.delete()
            messages.error(request, 'The code does not match your OTP. Please fill up the registration form and submit again.')
            return redirect('/accounts/register')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Successfully logged in, ' + str(user.username) + '!')
            return redirect('/')
        else:
            messages.error(request, 'Incorrect credentials')
            return redirect('/accounts/login')
    else:    
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('/accounts/login')


def teacherReg(request):
    subs = AllSubjects.objects.all()
    params = {'subjects': subs}
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        contact1 = request.POST.get('MobileNumber1')
        contact2 = request.POST.get('MobileNumber2')
        email = request.POST.get('EmailAddress')
        facebook = request.POST.get('FacebookId')
        institute = request.POST.get('Institute')
        dept = request.POST.get('Department')
        hscPass = request.POST.get('HscPassingYear')
        religion = request.POST.get('Religion')
        gender = request.POST.get('Gender')
        link = request.POST.get('classlink')
        subject1 = request.POST.get('Subject1')
        subject2 = request.POST.get('Subject2')
        subject3 = request.POST.get('Subject3')
        vers1 = request.POST.get('VersionPriority1')
        vers2 = request.POST.get('VersionPriority2')
        appointment = request.POST.get('AppointmentRemarks')

        teacher = TeachersApplied(
            fname=fname, lname=lname, contact1=contact1, contact2=contact2, 
            email=email, facebook=facebook, institute=institute, dept=dept, 
            hscPass=hscPass, religion=religion, gender=gender, subject1=subject1, 
            subject2=subject2, subject3=subject3, vers1=vers1, vers2=vers2, 
            appointment=appointment, date_of_apply=datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
            classLink=link
            )
        teacher.save()
        messages.success(request, 'Your application has been submitted. We will contact you soon for an interview.')

    return render(request, 'teacher-reg.html', params)


def userDashboard(request, uname):
    if request.user.is_authenticated and request.user.username == uname:
        user = User.objects.get(username=uname)
        userModel = Student.objects.filter(username=user.username)
        userall = AllUsers.objects.get(username=uname)
        if userall.accounts_type == 'Student':
            userModel2= Student.objects.get(username=user.username)
            enrollments = Enrollment.objects.filter(uname=uname)
            params = {
                'enrolled':userModel2.enrolled, 'enrollments':enrollments, 
                'successRate': round(float(userModel2.successRate), 2), 'points': int(userModel2.points),
                'quizzes': userModel2.quizAttended
                    }
            return render(request, 'student-dashboard.html', params)
        else:
            teacherModel = RegisteredTeachers.objects.get(username=user.username)
            all_subjects = AllSubjects.objects.all()
            courses = Courses.objects.filter(teacher=uname)

            if teacherModel.account_type == 'Teacher':
                subs = ast.literal_eval(teacherModel.subject)
                sub1 = subs[0]
                sub2 = subs[1]
                sub3 = subs[2]
                subject1 = AllSubjects.objects.get(slug=sub1)
                subject2 = AllSubjects.objects.get(slug=sub2)
                subject3 = AllSubjects.objects.get(slug=sub3)
                subList = [subject1, subject2, subject3]
                lectures1 = allContent.objects.filter(subjSlug=sub1)
                lectures2 = allContent.objects.filter(subjSlug=sub2)
                lectures3 = allContent.objects.filter(subjSlug=sub3)
                length1 = len(lectures1)
                length2 = len(lectures2)
                length3 = len(lectures3)
                totalLength = length1+length2+length3
                params = {'subs': subs, 'subList':subList, 'courses':courses, 'total_courses':len(courses), 'total_lectures': int(totalLength)}

                return render(request, 'teacher-dashboard.html', params)
            else:
                return render(request, 'student-dashboard.html')
            # params = {'enrolled':userModel2.enrolled}

    else:
        messages.error(request, 'You must login first to access the dashboard.')
        return redirect('/accounts/login')


def userEditInfo(request, uname):
    if request.user.is_authenticated and request.user.username == uname:
        userall = AllUsers.objects.get(username=uname)
        if userall.accounts_type == 'Student':
            user2 = Student.objects.get(username=uname)
            user = User.objects.get(username=uname)
            contactF = user2.contact
            addressF = user2.address
            if request.method == 'POST':
                Ffname = request.POST.get('fname')
                Flname = request.POST.get('lname')
                Fcontact = request.POST.get('contact')
                Femail = request.POST.get('email')
                Faddress = request.POST.get('address')

                user2.address = Faddress
                user2.fname = Ffname
                user2.lname = Flname
                user2.contact = Fcontact
                user2.email = Femail

                user.first_name = Ffname
                user.last_name = Flname
                user.email = Femail

                user.save()
                user2.save()
            else:
                params={'contact': contactF, 'address': addressF}
                return render(request, 'user-edit-info-s.html', params)

        else:
            user2 = RegisteredTeachers.objects.get(username=uname)
            user = User.objects.get(username=uname)
            contactF = user2.contact1
            contactF2 = user2.contact2
            if request.method == 'POST':
                Ffname = request.POST.get('fname')
                Flname = request.POST.get('lname')
                Fcontact1 = request.POST.get('contact')
                Femail = request.POST.get('email')
                Fcontact2 = request.POST.get('contact2')

                user2.contact2 = Fcontact2
                user2.fname = Ffname
                user2.lname = Flname
                user2.contact1 = Fcontact2
                user2.email = Femail

                user.first_name = Ffname
                user.last_name = Flname
                user.email = Femail

                user.save()
                user2.save()
                messages.info(request, 'Updated user information successfully!')
                return redirect('/accounts/user-dashboard/'+str(uname))

            else:
                params={'contact': contactF, 'contact2': contactF2}
                return render(request, 'user-edit-info-t.html', params)
    else:
        messages.info(request, 'Please login as ' + uname + ' first')
        return redirect('/accounts/login')
    
    
def securitySettings(request, uname):
    if request.user.is_authenticated and request.user.username == uname:
        userall = AllUsers.objects.get(username=uname)
        if userall.accounts_type == 'Student':
            user = Student.objects.get(username=uname)
            if user.accounts_type == 'Student':
                return render(request, 'account-settings-s.html')
            else:
                return render(request, 'account-settings-t.html')
        else:
            return render(request, 'account-settings-t.html')

    else:
        messages.info(request, 'Please login as ' + uname + ' first')
        return redirect('/accounts/login')


def deleteUser(request, uname):
    if request.user.is_authenticated and request.user.username == uname:
        userall = AllUsers.objects.get(username=uname)
        if userall.accounts_type == 'Student':
            user = User.objects.get(username=uname)
            user1 = Student.objects.get(username=uname)
            if Comments.objects.filter(username=uname).exists():
                comments = Comments.objects.filter(username=uname)
            if Enrollment.objects.filter(uname=uname).exists():
                enrolls = Enrollment.objects.filter(uname=uname)
            
            if request.method == 'POST':
                password = request.POST.get('password')
                if password == user1.password:
                    user.delete()
                    user1.delete()
                    userall.delete()
                    if Comments.objects.filter(username=uname).exists():
                        comments.delete()
                    else: 
                        pass
                    if Enrollment.objects.filter(uname=uname).exists():
                        enrolls.delete()
                    else: 
                        pass
                    messages.info(request, 'Account deleted successfully')        
                    return redirect('/accounts/login')
                else:
                    messages.info(request, 'Incorrect Password')        
                    return render(request, 'account-settings.html')
            else:    
                return render(request, 'account-settings.html')
        else:
            user = User.objects.get(username=uname)
            user1 = RegisteredTeachers.objects.get(username=uname)
            userall = AllUsers.objects.get(username=uname)
            if Comments.objects.filter(username=uname).exists():
                comments = Comments.objects.filter(username=uname)
            if Enrollment.objects.filter(uname=uname).exists():
                enrolls = Enrollment.objects.filter(uname=uname)

            if request.method == 'POST':
                password = request.POST.get('password')
                if password == user1.password:
                    user.delete()
                    user1.delete()
                    userall.delete()
                    if Comments.objects.filter(username=uname).exists():
                        comments.delete()
                    else: 
                        pass
                    if Enrollment.objects.filter(uname=uname).exists():
                        enrolls.delete()
                    else: 
                        pass
                    messages.info(request, 'Account deleted successfully')        
                    return redirect('/accounts/login')
                else:
                    messages.info(request, 'Incorrect Password')        
                    return render(request, 'account-settings.html')
            else:    
                return render(request, 'account-settings.html')


    else:
        messages.info(request, 'Please login as ' + uname + ' first')
        return redirect('/accounts/login')



def changePassword(request, uname):
    if request.user.is_authenticated and request.user.username == uname:
        if request.method == 'POST':
            oldPass = request.POST.get('old-password')
            newPass = request.POST.get('new-password')
            newPassConf = request.POST.get('new-password-confirm')
            userall = AllUsers.objects.get(username=uname)
            if userall.accounts_type == 'Student':
                user2 = User.objects.get(username=uname)
                user3 = Student.objects.get(username=uname)
                

                if oldPass == user3.password:
                    if newPass == newPassConf:
                        user2.set_password(newPass)
                        user3.password = newPass
                        userall.password = newPass
                        user2.save()
                        user3.save()
                        userall.save()
                        messages.success(request, 'Successfully changed password! PLease Log in again.')
                        return redirect('/')
                    else:
                        messages.info(request, 'Passwords do not match!')
                else:
                    messages.info(request, 'Incorrect Password')
            else:
                user2 = User.objects.get(username=uname)
                user3 = RegisteredTeachers.objects.get(username=uname)
                userall = AllUsers.objects.get(username=uname)

                if oldPass == user3.password:
                    if newPass == newPassConf:
                        user2.set_password(newPass)
                        user3.password = newPass
                        userall.password = newPass
                        user2.save()
                        user3.save()
                        userall.save()
                        messages.success(request, 'Successfully changed password! PLease Log in again.')
                        return redirect('/')
                    else:
                        messages.info(request, 'Passwords do not match!')

        return render(request, 'account-settings.html')
    else:
        messages.info(request, 'Please login as ' + uname + ' first')
        return redirect('/accounts/login')
    # return HttpResponse(oldPass)

def adminPanel(request):
    if request.user.is_active and request.user.is_superuser:
        students = Student.objects.all()
        teachers = TeachersApplied.objects.all()
        courses = Courses.objects.all()
        subjects = AllSubjects.objects.all()
        contacts = Contacts.objects.all()
        teachersreg = RegisteredTeachers.objects.all()

        params = {
            'students': students, 
            'teachers':teachers,
            'courses':courses,
            'contacts':contacts,
            'teachersreg': teachersreg,
            'subjects': subjects
            }

        return render(request, 'admin-panel.html', params)
        # return HttpResponse(students.values_list('username'))
    else:
        messages.error(request, 'You are not logged in as an Admin!')
        return redirect('/accounts/login')
        # return redirect('http://stackoverflow.com/')
    
def confirmTeacher(request, username):
    if request.user.is_active and request.user.is_superuser:
        applicants = TeachersApplied.objects.get(email=username)
        password = random.randint(100000, 999999)
        if request.method == 'POST':
            pay = request.POST.get('pay')
            subj1 = request.POST.get('subject1')
            subj2 = request.POST.get('subject2')
            subj3 = request.POST.get('subject3')
            vers = request.POST.get('version')

            reg = RegisteredTeachers(fname=applicants.fname, lname=applicants.lname, contact1=applicants.contact1, contact2=applicants.contact2, 
                    email=applicants.email, facebook=applicants.facebook, institute=applicants.institute, dept=applicants.dept, 
                    hscPass=applicants.hscPass, religion=applicants.religion, gender=applicants.gender, subject1=applicants.subject1, 
                    subject2=applicants.subject2, subject3=applicants.subject3, vers1=applicants.vers1, vers2=applicants.vers2, 
                    appointment=applicants.appointment, date_of_apply=applicants.date_of_apply, date_of_joining=datetime.now().strftime('%m/%d/%Y, %H:%M:%S'),
                    username=applicants.email, password=password, pay=pay, subject=[subj1, subj2, subj3], vers=vers, classLink=applicants.classLink)
            reg.save()
            userall = AllUsers(fname=applicants.fname, lname=applicants.lname, 
                                contact=applicants.contact1,
                                email=applicants.email, username=applicants.email, 
                                password=password, accounts_type='Teacher')
            userall.save()
        else:
            pass

    user = User.objects.create_user(applicants.email, applicants.email, password)
    user.first_name = applicants.fname
    user.last_name = applicants.lname
    user.save()

    subject = 'Account Confirmation from Imperia Education'
    body = 'Congratulations! You have been recruited as a Teacher in Imperia Eduactions. Now you can log in to our website with your email and use the teachers database. Your password is: ' + str(password) + '.'
    message = subject + '\n' + body
    email_to = [applicants.email]
    
    obj = smtplib.SMTP('smtp.gmail.com', 587)
    obj.starttls()
    obj.login('abiralmahdi@gmail.com', 'Doors.290')
    obj.sendmail('abiralmahdi@gmail.com', email_to, message)

    applicants.delete()
    messages.success(request, 'Hired teacher successfully. Now you need to set the password, pay and subject of the teacher manually.')
    return redirect('/accounts/adminPanel')

def deleteApplicant(request, username):
    if request.user.is_active and request.user.is_superuser:    
        applicants = TeachersApplied.objects.get(email=username)
        applicants.delete()
        messages.success(request, 'Deleted applicant successfully.')
        return redirect('/accounts/adminPanel')

def deleteStudent(request, username):
    students = Student.objects.get(username=username)
    student_user = User.objects.get(username=username)
    userall = AllUsers.objects.get(username=username)
    students.delete()
    student_user.delete()
    userall.delete()
    messages.success(request, 'Deleted student successfully.')
    return redirect('/accounts/adminPanel')

def deleteTeacher(request, username):
    if request.user.is_active and request.user.is_superuser:    
        applicants = RegisteredTeachers.objects.get(username=username)
        user = User.objects.get(username=username)
        userall = AllUsers.objects.get(username=uname)
        applicants.delete()
        user.delete()
        userall.delete()
        messages.success(request, 'Deleted applicant successfully.')
        return redirect('/accounts/adminPanel')


def show_addContent_page(request):
    if request.user.is_authenticated:
        return render(request, 'add-content.html')


def addContent(request, subj, uname):
    if request.user.is_authenticated and request.user.username == uname:
        user = User.objects.get(username=uname)
        userModel = Student.objects.filter(username=user.username)
        userall = AllUsers.objects.get(username=uname)
        if userall.accounts_type == 'Teacher':
            userr = RegisteredTeachers.objects.get(username=uname)
            subject = AllSubjects.objects.get(slug=subj)

            if request.method == 'POST':
                chno = request.POST.get('chno')
                name = request.POST.get('name')
                slug = 'ch' + str(chno)
                topicName = request.POST.get('topicName')
                desc = request.POST.get('desc')
                videoID = request.POST.get('videoID')
                notes = request.FILES['notes']

                content = allContent(subj=subject.name, subjSlug=subj, 
                                    chno=chno, chapname=name,
                                    topic=topicName, desc=desc, 
                                    videoID=videoID, chapSlug=slug, pdf=notes
                                    )
                if ChapterList.objects.filter(name=name, subj=subject.name).exists():
                    pass
                else:
                    chapters = ChapterList(name=name, slug=slug, no=chno, subj=subject.name, subjSlug=subj)
                    chapters.save()
                if subject.totLectures == '':
                    subject.totLectures = 1
                    subject.save()
                else:
                    subject.totLectures = int(subject.totLectures) + 1
                    subject.save()
                content.save()
                
            return render(request, 'add-content.html', {'subslug':subj})
            
        else:
            messages.error(request, 'Please Log In as ' + str(uname))
            return redirect('/accounts/login')


def addCourse(request):
    teachers = RegisteredTeachers.objects.all()
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'POST':
            name = request.POST.get('name')
            teacehr = request.POST.get('teacherName')
            teacher_specified = RegisteredTeachers.objects.get(username=teacehr)
            slug = request.POST.get('slug')
            price = request.POST.get('price')

            course = Courses(name=name, slug=slug, totLectures=0, teacher=teacehr, totStudents=0, link=teacher_specified.classLink, price=price)
            course.save()

            
            if teacher_specified.courseList == '':
                teacher_specified.courseList = [slug]
                teacher_specified.courses = 1
                teacher_specified.save()

            else:
                courseListManual = ast.literal_eval(teacher_specified.courseList)
                courseListManual.append(slug)
                teacher_specified.courseList = courseListManual
                teacher_specified.courses = len(courseListManual)
                teacher_specified.save()

            messages.success(request, 'Successfully added course')
            return redirect('/accounts/adminPanel')
            
            
            # return HttpResponse(teachers.values_list('email', flat=True)[0])
            
        params = {'teachers':teachers}
        return render(request, 'add-course.html', params)


def addQuestion(request, subj, uname):
    if request.user.is_authenticated and request.user.username == uname:
        user = User.objects.get(username=uname)
        userModel = Student.objects.filter(username=user.username)
        userall = AllUsers.objects.get(username=uname)
        if userall.accounts_type == 'Teacher':

            subject = AllSubjects.objects.get(slug=subj)
            if request.method == 'POST':
                # For Desktop View
                chapNo = request.POST.get('chapNo')
                chapname = request.POST.get('chapName')
                ques = request.POST.get('question')
                optionA = request.POST.get('option-a')
                optionB = request.POST.get('option-b')
                optionC = request.POST.get('option-c')
                optionD = request.POST.get('option-d')
                correctAns = request.POST.get('correct-ans')
                
                optionDict = {
                    'a': optionA,
                    'b': optionB,
                    'c': optionC,
                    'd': optionD
                            }


                entry = QuestionBank(subject=subj, chapterNo=chapNo, chapSlug='ch'+str(chapNo), ques=ques, options=optionDict, answer=correctAns)
                if QuizChapterList.objects.filter(name=chapname, subj=subject.name).exists():
                    pass
                else:
                    chapters = QuizChapterList(name=chapname, slug='ch'+str(chapNo), no=chapNo, subj=subject.name, subjSlug=subj)
                    chapters.save()

                entry.save()
                messages.success(request, 'Successfully added question!')
                return redirect('/accounts/user-dashboard/'+str(request.user.username))
                        
        

            params = {'subject':subject.name}
            return render(request, 'add-quiz.html', params)
    else:
        messages.success(request, 'Please log in as a teacher ')
        return redirect('/accounts/login')



def fileComplaint(request, uname):
    userall = AllUsers.objects.get(username=uname)
    tcr = RegisteredTeachers.objects.get(username=uname)
    if userall.accounts_type == 'Teacher':
        if request.method == 'POST':
            idd = request.POST.get('id')
            name = request.POST.get('name')
            desc = request.POST.get('desc')
            submit = Reports(name=str(tcr.fname)+' '+str(tcr.lname), desc=desc, against_id=idd, against=name)
            submit.save()
            messages.success(request, 'Your complaint has bee recorded in the database. We will contact you soon and take necessary actions')
        return redirect('/accounts/user-dashboard/'+uname)
    else:
        messages.error(request, 'Please log in as a teacher')
        return redirect('/accounts/login')


def send_mail_newsletter(request):
    emails = Newsletter.objects.all()
    email_list = [email.email for email in emails]
    
    if request.method == 'POST':

        subject = request.POST.get('topic')
        body = request.POST.get('desc')
        message = subject + '\n' + body
        email_to = email_list
    
        obj = smtplib.SMTP('smtp.gmail.com', 587)
        obj.starttls()
        obj.login('abiralmahdi@gmail.com', 'Doors.290')
        obj.sendmail('abiralmahdi@gmail.com', email_to, message)
        messages.success(request, 'Your emails have been sent')
        return redirect('/accounts/adminPanel')
    else:
        return render(request, 'newsletter.html')


