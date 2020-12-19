from django.db import models

# Create your models here.
class Student(models.Model):
    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=15)
    contact = models.CharField(max_length=15)
    email = models.CharField(max_length=30, primary_key=True, unique=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    address = models.CharField(max_length=300)
    enrolled = models.CharField(max_length=5000, default=0)
    points = models.CharField(max_length=30, default=0)
    successRate = models.CharField(max_length=10, default=0)
    quizAttended = models.CharField(max_length=300, default=0)
    results = models.CharField(max_length=5000, default='[]')
    accounts_type = models.CharField(max_length=50, default='Student')

    def __str__(self):
        return str(self.fname) + ' || ' + str(self.email) + ' || ' + str(self.username) + ' || '


class StudentsWithoutOTP(models.Model):
    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=15)
    contact = models.CharField(max_length=15)
    email = models.CharField(max_length=30)
    username = models.CharField(max_length=30, primary_key=True, unique=True)
    password = models.CharField(max_length=30)
    address = models.CharField(max_length=300)
    enrolled = models.CharField(max_length=5000, default=0)
    points = models.CharField(max_length=30)
    results = models.CharField(max_length=5000)
    accounts_type = models.CharField(max_length=50, default='Student')
    otp = models.CharField(max_length=10)

    def __str__(self):
        return str(self.fname) + ' || ' + str(self.email) + ' || ' + str(self.username) + ' || '




class TeachersApplied(models.Model):
    fname = models.CharField(max_length=15, default='')
    lname = models.CharField(max_length=15, default='')
    contact1 = models.CharField(max_length=15)
    contact2 = models.CharField(max_length=15)
    email = models.CharField(max_length=30, primary_key=True, unique=True)
    facebook = models.CharField(max_length=250)
    institute = models.CharField(max_length=30)
    dept = models.CharField(max_length=30)
    hscPass = models.CharField(max_length=30)
    religion = models.CharField(max_length=30)
    gender  =models.CharField(max_length=30)
    subject1 = models.CharField(max_length=30)
    subject2 = models.CharField(max_length=30)
    subject3 = models.CharField(max_length=30)
    classLink = models.CharField(max_length=5000, default='')
    vers1 = models.CharField(max_length=30)
    vers2 = models.CharField(max_length=30)
    appointment = models.CharField(max_length=500)
    date_of_apply = models.CharField(max_length=30)
  
    def __str__(self):
        return str(self.fname) + ' || ' + str(self.email) + ' || ' + str(self.contact1) + ' || '


class RegisteredTeachers(models.Model):
    fname = models.CharField(max_length=15, default='')
    lname = models.CharField(max_length=15, default='')
    contact1 = models.CharField(max_length=15)
    contact2 = models.CharField(max_length=15)
    email = models.CharField(max_length=30, primary_key=True, unique=True)
    facebook = models.CharField(max_length=250)
    institute = models.CharField(max_length=30)
    dept = models.CharField(max_length=30)
    hscPass = models.CharField(max_length=30)
    religion = models.CharField(max_length=30)
    gender  =models.CharField(max_length=30)
    subject1 = models.CharField(max_length=30)
    subject2 = models.CharField(max_length=30)
    subject3 = models.CharField(max_length=30)
    classLink = models.CharField(max_length=5000, default='')
    vers1 = models.CharField(max_length=30)
    vers2 = models.CharField(max_length=30)
    courses = models.CharField(max_length=3000, default=0)
    courseList = models.CharField(max_length=99999999)
    appointment = models.CharField(max_length=500)
    date_of_apply = models.CharField(max_length=30)

    #The meaningful information
    pay = models.CharField(max_length=30)
    subject = models.CharField(max_length=300)
    vers = models.CharField(max_length=30)
    date_of_joining = models.CharField(max_length=30)

    # The account informations (sensitive)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    account_type = models.CharField(max_length=50, default='Teacher')


    def __str__(self):
        return str(self.fname) + ' || ' + str(self.email) + ' || ' + str(self.contact1) + ' || '


class AllUsers(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    accounts_type = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return str(self.fname) + ' || ' + str(self.email) + ' || ' + str(self.username) + ' || '

