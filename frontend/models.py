from django.db import models
from django.contrib.auth.models import User



from django.db import models
from django.contrib.auth.models import User


# =====================================================
# 1. PROFILE MODEL
# =====================================================

class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    age = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=20,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    hobbies = models.CharField(
        max_length=300,
        blank=True
    )

    instagram = models.CharField(
        max_length=200,
        blank=True
    )

    github = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.user.username
    
# =====================================================
# 2. HOME PAGE SLIDER MODEL
# =====================================================

class Slide(models.Model):

    title = models.CharField(
        max_length=100,
        blank=True
    )

    section_id = models.CharField(
        max_length=100
    )

    image = models.ImageField(
        upload_to="slides/"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["id"]

    def __str__(self):

        return self.title if self.title else self.section_id


# =====================================================
# 3. TEACHER MODEL
# =====================================================

class Teacher(models.Model):

    name = models.CharField(
        max_length=100
    )

    image = models.ImageField(
        upload_to="teachers/",
        blank=True,
        null=True
    )

    contain = models.CharField(
        max_length=500
    )

    def __str__(self):
        return self.name


# =====================================================
# 4. COURSE MODEL
# =====================================================

class Course(models.Model):

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="courses"
    )

    course_name = models.CharField(
        max_length=200
    )

    course_image = models.ImageField(
        upload_to="courses/",
        blank=True,
        null=True
    )

    description = models.TextField()

    price = models.PositiveIntegerField(
        default=99
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.course_name


# =====================================================
# 5. LECTURE MODEL
# =====================================================

class Lecture(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lectures"
    )

    title = models.CharField(
        max_length=200
    )

    lecture_number = models.PositiveIntegerField(
        default=1
    )

    video_link = models.URLField(
        blank=True,
        null=True
    )

    notes_link = models.URLField(
        blank=True,
        null=True
    )

    assignment_link = models.URLField(
        blank=True,
        null=True
    )

    is_preview = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["lecture_number"]

    def __str__(self):

        return (
            f"{self.course.course_name}"
            f" - Lecture {self.lecture_number}"
        )
    
# =====================================================
# 6. PURCHASED COURSE MODEL
# =====================================================

class PurchasedCourse(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="purchased_courses"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="purchases"
    )

    purchased_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-purchased_at"]

        unique_together = (
            "user",
            "course"
        )

    def __str__(self):

        return (
            f"{self.user.username}"
            f" purchased "
            f"{self.course.course_name}"
        )


# =====================================================
# 7. SUPPORT TICKET MODEL
# =====================================================

class SupportTicket(models.Model):

    CATEGORY_CHOICES = [

        ("Course", "Course Problem"),

        ("Lecture", "Lecture Problem"),

        ("Payment", "Payment Problem"),

        ("Login", "Login Problem"),

        ("Technical", "Technical Issue"),

        ("AI", "AI Doubt"),

        ("Other", "Other"),

    ]


    STATUS_CHOICES = [

        ("Pending", "Pending"),

        ("In Review", "In Review"),

        ("Solved", "Solved"),

        ("Rejected", "Rejected"),

    ]


    PRIORITY_CHOICES = [

        ("Low", "Low"),

        ("Medium", "Medium"),

        ("High", "High"),

    ]


    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="support_tickets"

    )


    category = models.CharField(

        max_length=30,

        choices=CATEGORY_CHOICES,

        default="Other"

    )


    priority = models.CharField(

        max_length=20,

        choices=PRIORITY_CHOICES,

        default="Medium"

    )


    subject = models.CharField(

        max_length=250

    )


    message = models.TextField()


    admin_reply = models.TextField(

        blank=True

    )


    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default="Pending"

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )


    updated_at = models.DateTimeField(

        auto_now=True

    )


    class Meta:

        ordering = ["-created_at"]


    def __str__(self):

        return (

            f"{self.user.username}"

            f" | "

            f"{self.subject}"

        )
    
# =====================================================
# 8. TEST MODEL
# =====================================================

class Test(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="tests"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    duration_minutes = models.PositiveIntegerField(
        default=30
    )

    total_marks = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["id"]

    def __str__(self):

        return (
            f"{self.course.course_name}"
            f" - "
            f"{self.title}"
        )


# =====================================================
# 9. QUESTION MODEL
# =====================================================

class Question(models.Model):

    QUESTION_TYPES = [

        ("single", "Single Correct"),

        ("multiple", "Multiple Correct"),

        ("integer", "Integer Type"),

    ]

    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question_text = models.TextField()

    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        default="single"
    )

    marks = models.PositiveIntegerField(
        default=1
    )

    correct_integer_answer = models.IntegerField(
        blank=True,
        null=True
    )

    explanation = models.TextField(
        blank=True
    )

    def __str__(self):

        return self.question_text[:60]


# =====================================================
# 10. OPTION MODEL
# =====================================================

class Option(models.Model):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options"
    )

    option_text = models.CharField(
        max_length=500
    )

    is_correct = models.BooleanField(
        default=False
    )

    def __str__(self):

        return self.option_text
    
# =====================================================
# 11. TEST ATTEMPT MODEL
# =====================================================

class TestAttempt(models.Model):

    RESULT_STATUS = [

        ("Pass", "Pass"),

        ("Fail", "Fail"),

    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="test_attempts"
    )

    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name="attempts"
    )

    attempt_number = models.PositiveIntegerField(
        default=1
    )

    score = models.PositiveIntegerField(
        default=0
    )

    total_marks = models.PositiveIntegerField(
        default=0
    )

    total_questions = models.PositiveIntegerField(
        default=0
    )

    correct_answers = models.PositiveIntegerField(
        default=0
    )

    wrong_answers = models.PositiveIntegerField(
        default=0
    )

    skipped_answers = models.PositiveIntegerField(
        default=0
    )

    percentage = models.FloatField(
        default=0
    )

    result = models.CharField(
        max_length=10,
        choices=RESULT_STATUS,
        default="Fail"
    )

    time_taken_seconds = models.PositiveIntegerField(
        default=0
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-submitted_at"]

    def __str__(self):

        return (
            f"{self.user.username}"
            f" - "
            f"{self.test.title}"
            f" (Attempt {self.attempt_number})"
        )


# =====================================================
# 12. STUDENT ANSWER MODEL
# =====================================================

class StudentAnswer(models.Model):

    attempt = models.ForeignKey(
        TestAttempt,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    # Single Correct Question
    selected_option = models.ForeignKey(
        Option,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="single_answers"
    )

    # Multiple Correct Question
    selected_options = models.ManyToManyField(
        Option,
        blank=True,
        related_name="multiple_answers"
    )

    # Integer Question
    integer_answer = models.IntegerField(
        null=True,
        blank=True
    )

    is_correct = models.BooleanField(
        default=False
    )

    class Meta:

        ordering = ["id"]

    def __str__(self):

        return (
            f"{self.attempt.user.username}"
            f" - "
            f"Question {self.question.id}"
        )