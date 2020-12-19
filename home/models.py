from django.db import models

# Create your models here.
class Contacts(models.Model):
    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=15)
    contact = models.CharField(max_length=15)
    email = models.CharField(max_length=30)
    message = models.CharField(max_length=500)
    

class AllSubjects(models.Model):
    name = models.CharField(max_length=30)
    slug = models.CharField(max_length=30)
    totLectures = models.CharField(max_length=30, default='')

    def __str__(self):
        return str(self.name) + ' || ' + str(self.slug) + ' || '

class ChapterList(models.Model):
    name = models.CharField(max_length=30)
    no = models.CharField(max_length=30)
    subj = models.CharField(max_length=30)
    subjSlug = models.CharField(max_length=30)
    slug = models.CharField(max_length=30)

    def __str__(self):
        return str(self.no) + ' || '+ str(self.name) + ' || ' + str(self.slug) + ' || '+ str(self.subj) + ' || '


class QuizChapterList(models.Model):
    name = models.CharField(max_length=30)
    no = models.CharField(max_length=30)
    subj = models.CharField(max_length=30)
    subjSlug = models.CharField(max_length=30)
    slug = models.CharField(max_length=30)

    def __str__(self):
        return str(self.no) + ' || '+ str(self.name) + ' || ' + str(self.slug) + ' || '+ str(self.subj) + ' || '


class CV(models.Model):
    email = models.CharField(max_length=30)
    img = models.FileField(upload_to='static/images')


class Enrollment(models.Model):
    name = models.CharField(max_length=30)
    uname = models.CharField(max_length=30)
    contact = models.CharField(max_length=30)
    version = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    link = models.CharField(max_length=3000, default='')


class Comments(models.Model):
    username = models.CharField(max_length=30)
    comment = models.CharField(max_length=10000)
    video = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    chapter = models.CharField(max_length=30)
    datetime = models.CharField(max_length=30)
    replies = models.CharField(max_length=9999999999999999, default='')
    def __str__(self):
        return str(self.username) + ' || '+ str(self.video) + ' || ' + str(self.subject) + ' || '+ str(self.chapter) + ' || '


class Replies(models.Model):
    username = models.CharField(max_length=30)
    comment_id = models.CharField(max_length=30)
    video = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    chapter = models.CharField(max_length=30)
    datetime = models.CharField(max_length=30)
    reply = models.CharField(max_length=500)

    def __str__(self):
        return str(self.username) + ' || '+ str(self.video) + ' || ' + str(self.subject) + ' || '+ str(self.chapter) + ' || '


class allContent(models.Model):
    chno = models.CharField(max_length=30)
    chapname = models.CharField(max_length=50)
    topic = models.CharField(max_length=100)
    subj = models.CharField(max_length=50)
    subjSlug = models.CharField(max_length=50)
    desc = models.CharField(max_length=300)
    videoID = models.CharField(max_length=30)
    pdf = models.FileField(upload_to='static/files')
    chapSlug = models.CharField(max_length=30)
    comments = models.CharField(max_length=99999999999999, default='')
    def __str__(self):
        return str(self.chno) + ' || '+ str(self.chapname) + ' || ' + str(self.subj) + ' || '+ str(self.videoID) + ' || '

class noticeBoard(models.Model):
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=300)
    icons = models.CharField(max_length=300, default='')


class Reports(models.Model):
    name = models.CharField(max_length=50)
    against_id = models.CharField(max_length=50)
    against = models.CharField(max_length=50)
    desc = models.CharField(max_length=1000)

class Newsletter(models.Model):
    email = models.CharField(max_length=100)


class Courses(models.Model):
    name = models.CharField(max_length=30)
    slug = models.CharField(max_length=30)
    teacher = models.CharField(max_length=30, default='')
    link = models.CharField(max_length=5000, default='')
    totStudents = models.CharField(max_length=30, default='')
    totLectures = models.CharField(max_length=30, default='')
    price = models.CharField(max_length=10, default='')

    def __str__(self):
        return str(self.name) + ' || ' + str(self.slug) + ' || '

class QuestionBank(models.Model):
    quesID = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=30)
    chapterNo = models.CharField(max_length=30)
    chapSlug = models.CharField(max_length=30)
    ques = models.CharField(max_length=5000)
    options = models.CharField(max_length=3324530)
    answer = models.CharField(max_length=30)

    def __str__(self):
        return str(self.quesID) + ' || ' +  str(self.ques) + ' || ' + str(self.subject) + ' || ' + str(self.chapterNo) + ' || ' + str(self.options)+ ' || ' + str(self.answer)


"""THE DATABASE MODELS FOR THE QUIZ PART"""


class JSCScienceQuiz(models.Model):
    question = models.CharField(max_length=30)
    a = models.CharField(max_length=30)
    b = models.CharField(max_length=30)
    c = models.CharField(max_length=30)
    d = models.CharField(max_length=30)
    ans = models.CharField(max_length=30)

class JSCMathQuiz(models.Model):
    question = models.CharField(max_length=30)
    a = models.CharField(max_length=30)
    b = models.CharField(max_length=30)
    c = models.CharField(max_length=30)
    d = models.CharField(max_length=30)
    ans = models.CharField(max_length=30)

class SSCPhysicsQuiz(models.Model):
    question = models.CharField(max_length=30)
    a = models.CharField(max_length=30)
    b = models.CharField(max_length=30)
    c = models.CharField(max_length=30)
    d = models.CharField(max_length=30)
    ans = models.CharField(max_length=30)

class SSCChemistryQuiz(models.Model):
    question = models.CharField(max_length=30)
    a = models.CharField(max_length=30)
    b = models.CharField(max_length=30)
    c = models.CharField(max_length=30)
    d = models.CharField(max_length=30)
    ans = models.CharField(max_length=30)

class SSCMathQuiz(models.Model):
    question = models.CharField(max_length=30)
    a = models.CharField(max_length=30)
    b = models.CharField(max_length=30)
    c = models.CharField(max_length=30)
    d = models.CharField(max_length=30)
    ans = models.CharField(max_length=30)

class SSCHMathQuiz(models.Model):
    question = models.CharField(max_length=30)
    a = models.CharField(max_length=30)
    b = models.CharField(max_length=30)
    c = models.CharField(max_length=30)
    d = models.CharField(max_length=30)
    ans = models.CharField(max_length=30)

class HSCPhysics1stQuiz(models.Model):
    question = models.CharField(max_length=30)
    a = models.CharField(max_length=30)
    b = models.CharField(max_length=30)
    c = models.CharField(max_length=30)
    d = models.CharField(max_length=30)
    ans = models.CharField(max_length=30)

class HSCPhysics2ndQuiz(models.Model):
    question = models.CharField(max_length=30)
    a = models.CharField(max_length=30)
    b = models.CharField(max_length=30)
    c = models.CharField(max_length=30)
    d = models.CharField(max_length=30)
    ans = models.CharField(max_length=30)

class HSCChemistry1stQuiz(models.Model):
    question = models.CharField(max_length=30)
    a = models.CharField(max_length=30)
    b = models.CharField(max_length=30)
    c = models.CharField(max_length=30)
    d = models.CharField(max_length=30)
    ans = models.CharField(max_length=30)

class HSCChemistry2ndQuiz(models.Model):
    question = models.CharField(max_length=30)
    a = models.CharField(max_length=30)
    b = models.CharField(max_length=30)
    c = models.CharField(max_length=30)
    d = models.CharField(max_length=30)
    ans = models.CharField(max_length=30)

class HSCMath1stQuiz(models.Model):
    question = models.CharField(max_length=30)
    a = models.CharField(max_length=30)
    b = models.CharField(max_length=30)
    c = models.CharField(max_length=30)
    d = models.CharField(max_length=30)
    ans = models.CharField(max_length=30)

class HSCMath2ndQuiz(models.Model):
    question = models.CharField(max_length=30)
    a = models.CharField(max_length=30)
    b = models.CharField(max_length=30)
    c = models.CharField(max_length=30)
    d = models.CharField(max_length=30)
    ans = models.CharField(max_length=30)

