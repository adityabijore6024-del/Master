# ==========================================
# Imports
# ==========================================

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.http import (
    JsonResponse,
    HttpResponseForbidden
)

from django.contrib import messages

from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash
)

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db.models import (
    Q,
    Avg,
    Max
)

from django.conf import settings

import razorpay

from google import genai


# ==========================================
# Models
# ==========================================

from .models import (
    Profile,
    Slide,
    Teacher,
    Course,
    PurchasedCourse,
    SupportTicket,
    Test,
    Question,
    Option,
    TestAttempt,
    StudentAnswer,
)

# ==========================================
# Gemini Client
# ==========================================

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


# ==========================================
# Landing Page
# ==========================================

def landing_view(request):

    return render(
        request,
        "index.html"
    )

# ==========================================
# Policy Page
# ==========================================

def policy_view(request):

    if request.method == "POST":

        data = request.session.get("signup_data")

        if not data:
            return redirect("signup")

        if User.objects.filter(username=data["username"]).exists():
            request.session.pop("signup_data", None)
            return render(
                request,
                "login.html",
                {"error": "Username already exists."}
            )

        if User.objects.filter(email=data["email"]).exists():
            request.session.pop("signup_data", None)
            return render(
                request,
                "login.html",
                {"error": "Email already registered."}
            )

        user = User.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"]
        )

        Profile.objects.create(
            user=user,
            phone=data["mobile"],
            age=data["age"]
        )

        request.session.pop("signup_data", None)

        return redirect("login")

    return render(request, "policy.html")


# ==========================================
# Signup
# ==========================================

def signup_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        age = request.POST.get("age")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if User.objects.filter(username=username).exists():

            return render(
                request,
                "login.html",
                {"error": "Username already exists."}
            )

        if User.objects.filter(email=email).exists():

            return render(
                request,
                "login.html",
                {"error": "Email already registered."}
            )

        if password1 != password2:

            return render(
                request,
                "login.html",
                {"error": "Passwords do not match."}
            )

        request.session["signup_data"] = {
            "username": username,
            "age": age,
            "mobile": mobile,
            "email": email,
            "password": password1
        }

        return redirect("policy")

    return render(request, "login.html")

# ==========================================
# Login
# ==========================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get(
            "username3"
        )

        password = request.POST.get(
            "password3"
        )

        user = authenticate(

            request,

            username=username,

            password=password

        )

        if user:

            login(
                request,
                user
            )

            return redirect(
                "home"
            )

        return render(

            request,

            "login.html",

            {
                "error":
                "Invalid username or password."
            }

        )

    return render(
        request,
        "login.html"
    )


# ==========================================
# PROFILE
# ==========================================

@login_required(login_url="login")
def profile_view(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        # ==========================================
        # CHANGE PASSWORD
        # ==========================================

        if "change_password" in request.POST:

            old_password = request.POST.get(
                "old_password"
            )

            new_password = request.POST.get(
                "new_password"
            )

            confirm_password = request.POST.get(
                "confirm_password"
            )

            if not request.user.check_password(
                old_password
            ):

                messages.error(
                    request,
                    "Current password is incorrect."
                )

                return redirect("profile")

            if new_password != confirm_password:

                messages.error(
                    request,
                    "New passwords do not match."
                )

                return redirect("profile")

            if len(new_password) < 8:

                messages.error(
                    request,
                    "Password must be at least 8 characters."
                )

                return redirect("profile")

            request.user.set_password(
                new_password
            )

            request.user.save()

            update_session_auth_hash(
                request,
                request.user
            )

            messages.success(
                request,
                "Password changed successfully."
            )

            return redirect("profile")

        # ==========================================
        # CHANGE EMAIL
        # ==========================================

        elif "change_email" in request.POST:

            new_email = request.POST.get(
                "new_email"
            )

            password = request.POST.get(
                "email_password"
            )

            if not request.user.check_password(
                password
            ):

                messages.error(
                    request,
                    "Current password is incorrect."
                )

                return redirect("profile")

            if User.objects.filter(
                email=new_email
            ).exclude(
                id=request.user.id
            ).exists():

                messages.error(
                    request,
                    "Email already exists."
                )

                return redirect("profile")

            request.user.email = new_email

            request.user.save()

            messages.success(
                request,
                "Email changed successfully."
            )

            return redirect("profile")

        # ==========================================
        # UPDATE PROFILE
        # ==========================================

        profile.phone = request.POST.get(
            "phone"
        )

        profile.age = request.POST.get(
            "age"
        )

        profile.gender = request.POST.get(
            "gender"
        )

        profile.city = request.POST.get(
            "city"
        )

        profile.instagram = request.POST.get(
            "instagram"
        )

        profile.github = request.POST.get(
            "github"
        )

        profile.hobbies = request.POST.get(
            "hobbies"
        )

        profile.bio = request.POST.get(
            "bio"
        )

        if request.FILES.get(
            "profile_image"
        ):

            profile.profile_image = request.FILES.get(
                "profile_image"
            )

        profile.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("profile")

    return render(

        request,

        "profile.html",

        {
            "profile": profile
        }

    )

# ==========================================
# Logout
# ==========================================

def logout_view(request):

    logout(request)

    return redirect(
        "index"
    )


# ==========================================
# ACTIVITY DASHBOARD
# ==========================================

from django.db.models import Avg, Max
from .models import PurchasedCourse, TestAttempt


@login_required
def activity(request):

    purchases = PurchasedCourse.objects.filter(
        user=request.user
    ).order_by("-purchased_at")

    attempts = TestAttempt.objects.filter(
        user=request.user
    ).order_by("-submitted_at")

    total_courses = purchases.count()

    total_spent = sum(
        item.course.price
        for item in purchases
    )

    last_purchase = purchases.first()

    total_tests = attempts.count()

    avg_score = (
        attempts.aggregate(
            Avg("percentage")
        )["percentage__avg"]
        or 0
    )

    best_score = (
        attempts.aggregate(
            Max("percentage")
        )["percentage__max"]
        or 0
    )

    return render(
        request,
        "activity.html",
        {
            "purchases": purchases,
            "attempts": attempts,
            "total_courses": total_courses,
            "total_spent": total_spent,
            "last_purchase": last_purchase,
            "total_tests": total_tests,
            "avg_score": round(avg_score, 2),
            "best_score": best_score,
        },
    )

# ==========================================
# HOME
# ==========================================


# @login_required(login_url="login")

from django.db.models import Q

def home_view(request):

    slides = Slide.objects.all().order_by("id")

    teachers = Teacher.objects.all()

    profile = None

    purchased_ids = []

    if request.user.is_authenticated:

        profile, created = Profile.objects.get_or_create(
            user=request.user
        )

        purchased_ids = list(
            PurchasedCourse.objects.filter(
                user=request.user
            ).values_list(
                "course_id",
                flat=True
            )
        )

    query = request.GET.get("q")

    courses = Course.objects.none()

    if query:

        courses = Course.objects.filter(

            Q(course_name__icontains=query) |

            Q(description__icontains=query)

        )

    return render(

        request,

        "home.html",

        {

            "slides": slides,

            "teacher": teachers,

            "courses": courses,

            "profile": profile,

            "purchased_ids": purchased_ids,

        }

    )

# ==========================================
#COURSE
# ==========================================
# @login_required(login_url="login")
def teacher_courses(request, id):

    teacher = get_object_or_404(
        Teacher,
        id=id
    )

    courses = Course.objects.filter(
        teacher=teacher
    )

    purchased_ids = []

    if request.user.is_authenticated:

        purchased_ids = PurchasedCourse.objects.filter(

            user=request.user

        ).values_list(

            "course_id",

            flat=True

        )

    return render(

        request,

        "teacher.html",

        {

            "teacher": teacher,

            "courses": courses,

            "purchased_ids": purchased_ids,

        }

    )

# ==========================================
# COURSE PAYMENT
# ==========================================
@login_required
def payment2_view(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    client = razorpay.Client(

        auth=(

            settings.RAZORPAY_KEY_ID,

            settings.RAZORPAY_KEY_SECRET

        )

    )

    order = client.order.create({

        "amount": course.price * 100,

        "currency": "INR",

        "payment_capture": 1,

    })

    return render(

        request,

        "payment2.html",

        {

            "course": course,

            "payment": order,

            "razorpay_key": settings.RAZORPAY_KEY_ID,

        }

    )


# ==========================================
# COURSE PAYMENT SUCCESS
# ==========================================
@login_required
def course_payment_success(request, course_id):

    course = get_object_or_404(

        Course,

        id=course_id

    )

    PurchasedCourse.objects.get_or_create(

        user=request.user,

        course=course

    )

    return redirect(

        "course_access",

        course_id=course.id

    )


# ==========================================
# COURSE ACCESS
# ==========================================
@login_required
def course_access(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    purchased = PurchasedCourse.objects.filter(
        user=request.user,
        course=course
    ).exists()

    if not purchased:
        return redirect("payment2", course_id=course.id)

    lecture = course.lectures.first()

    return render(
        request,
        "course.html",
        {
            "course": course,
            "lecture": lecture,
        }
    )


# ==========================================
# DOUBT
# ==========================================

def doubt_solver(request):

    return render(

        request,

        "doubt.html",

        {

            "api_key": settings.GEMINI_API_KEY  # Ye line jaruri hai

        }

    )

# ==========================================
# LIVE SEARCH
# ==========================================

from django.http import JsonResponse
from django.urls import reverse
from .models import Course, Test
from django.http import JsonResponse
from django.db.models import Q


def live_search(request):

    query = request.GET.get("q", "").strip()

    courses = []

    tests = []

    purchased_ids = []

    if request.user.is_authenticated:

        purchased_ids = list(

            PurchasedCourse.objects.filter(

                user=request.user

            ).values_list(

                "course_id",
                flat=True

            )

        )

    if query:

        course_queryset = Course.objects.filter(

            Q(course_name__icontains=query) |

            Q(description__icontains=query)

        ).select_related("teacher")


        for course in course_queryset:

            courses.append({

                "id": course.id,

                "course_name": course.course_name,

                "description": course.description,

                "price": course.price,

                "teacher_name": course.teacher.name,

                "course_image": (
                    course.course_image.url
                    if course.course_image
                    else ""
                ),

            })


        test_queryset = Test.objects.filter(

            title__icontains=query

        ).select_related(

            "course"

        )


        for test in test_queryset:

            tests.append({

                "id": test.id,

                "title": test.title,

                "course_id": test.course.id,

                "purchased": test.course.id in purchased_ids,

            })

    return JsonResponse({

        "courses": courses,

        "tests": tests,

    })
# ==========================================
# ALL COURSE
# ==========================================
from .models import Course

def all_courses(request):

    courses = Course.objects.all().order_by("course_name")

    return render(
        request,
        "all_courses.html",
        {
            "courses": courses
        }
    )

# ==========================================
# CONTACT SUPPORT
# ==========================================

from .models import SupportTicket


@login_required
def contact_support(request):

    success = False

    if request.method == "POST":

        subject = request.POST.get("subject")

        message = request.POST.get("message")

        SupportTicket.objects.create(
            user=request.user,
            subject=subject,
            message=message,
        )

        success = True

    tickets = (
        SupportTicket.objects.filter(
            user=request.user
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "contact_support.html",
        {
            "success": success,
            "tickets": tickets,
        },
    )


# ==========================================
# TEST LIST
# ==========================================

from django.shortcuts import get_object_or_404
from .models import (
    Course,
    Test,
    Question,
    Option,
    StudentAnswer,
)


@login_required
def test_list(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    tests = Test.objects.filter(
        course=course
    )

    return render(
        request,
        "test_list.html",
        {
            "course": course,
            "tests": tests,
        },
    )



# ==========================================
# RESULT PAGE
# ==========================================

@login_required
def result_page(request, attempt_id):

    attempt = get_object_or_404(
        TestAttempt,
        id=attempt_id,
        user=request.user,
    )

    return render(
        request,
        "result.html",
        {
            "attempt": attempt,
        },
    )


# ==========================================
# MY TEST HISTORY
# ==========================================

@login_required
def my_test_history(request):

    attempts = TestAttempt.objects.filter(
        user=request.user
    ).order_by("-submitted_at")

    return render(
        request,
        "attempt_history.html",
        {
            "attempts": attempts,
        },
    )

# ==========================================================
# ACTIVITY DASHBOARD
# ==========================================================

from django.db.models import Avg, Max
from .models import PurchasedCourse, TestAttempt


@login_required
def activity(request):

    purchases = PurchasedCourse.objects.filter(
        user=request.user
    ).select_related(
        "course"
    ).order_by("-purchased_at")

    all_attempts = TestAttempt.objects.filter(
        user=request.user
    ).select_related(
        "test",
        "test__course"
    ).order_by("-submitted_at")

    attempts = all_attempts[:5]

    total_courses = purchases.count()

    total_spent = sum(
        purchase.course.price
        for purchase in purchases
    )

    last_purchase = purchases.first()

    total_attempts = attempts.count()

    avg_percentage = (
        attempts.aggregate(
            Avg("percentage")
        )["percentage__avg"] or 0
    )

    best_percentage = (
        attempts.aggregate(
            Max("percentage")
        )["percentage__max"] or 0
    )

    return render(
        request,
        "activity.html",
        {
            "purchases": purchases,
            "attempts": attempts,

            "total_courses": total_courses,
            "total_spent": total_spent,

            "last_purchase": last_purchase,

            "total_attempts": total_attempts,
            "avg_percentage": round(avg_percentage, 2),
            "best_percentage": best_percentage,
        }
    )


# ==========================================================
# CONTACT SUPPORT
# ==========================================================

from .models import SupportTicket


@login_required
def contact_support(request):

    success = False

    if request.method == "POST":

        SupportTicket.objects.create(

            user=request.user,

            subject=request.POST.get("subject"),

            message=request.POST.get("message")

        )

        success = True

    tickets = SupportTicket.objects.filter(

        user=request.user

    ).order_by("-created_at")

    return render(

        request,

        "contact_support.html",

        {

            "tickets": tickets,

            "success": success

        }

    )


# ==========================================================
# TEST LIST
# ==========================================================

from django.shortcuts import get_object_or_404
from .models import Course, Test


@login_required
def test_list(request, course_id):

    course = get_object_or_404(

        Course,

        id=course_id

    )

    tests = Test.objects.filter(

        course=course

    )

    return render(

        request,

        "test_list.html",

        {

            "course": course,

            "tests": tests

        }

    )


# ==========================================================
# START TEST
# ==========================================================

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect


@login_required
def start_test(request, test_id):

    test = get_object_or_404(
        Test,
        id=test_id
    )

    # Agar test sirf purchased course ke students ko dena hai
    if not PurchasedCourse.objects.filter(
        user=request.user,
        course=test.course
    ).exists():

        return redirect("test_list", course_id=test.course.id)

    questions = (
        Question.objects
        .filter(test=test)
        .prefetch_related("options")
        .order_by("id")
    )

    context = {

        "test": test,
        "questions": questions,

    }

    return render(
        request,
        "test_page.html",
        context
    )

# ==========================================================
# SUBMIT TEST
# ==========================================================

from .models import Option
from .models import StudentAnswer


@login_required
def submit_test(request, test_id):

    if request.method != "POST":
        return redirect("start_test", test_id=test_id)

    test = get_object_or_404(Test, id=test_id)

    questions = Question.objects.filter(test=test)

    attempt = TestAttempt.objects.create(
        user=request.user,
        test=test
    )

    correct = 0
    wrong = 0
    skipped = 0
    score = 0

    for question in questions:

        # -----------------------------
        # SINGLE CORRECT
        # -----------------------------

        if question.question_type == "single":

            answer = request.POST.get(
                f"question_{question.id}"
            )

            if not answer:
                skipped += 1
                continue

            option = Option.objects.get(
                id=answer,
                question=question
            )

            is_correct = option.is_correct

            StudentAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_option=option,
                is_correct=is_correct
            )

            if is_correct:
                correct += 1
                score += question.marks
            else:
                wrong += 1

        # -----------------------------
        # MULTIPLE CORRECT
        # -----------------------------

        elif question.question_type == "multiple":

            selected_ids = request.POST.getlist(
                f"question_{question.id}"
            )

            if not selected_ids:
                skipped += 1
                continue

            student_answer = StudentAnswer.objects.create(
                attempt=attempt,
                question=question
            )

            selected_options = Option.objects.filter(
                id__in=selected_ids,
                question=question
            )

            student_answer.selected_options.set(
                selected_options
            )

            correct_options = Option.objects.filter(
                question=question,
                is_correct=True
            )

            selected_set = set(
                selected_options.values_list(
                    "id",
                    flat=True
                )
            )

            correct_set = set(
                correct_options.values_list(
                    "id",
                    flat=True
                )
            )

            if selected_set == correct_set:

                student_answer.is_correct = True
                student_answer.save()

                correct += 1
                score += question.marks

            else:

                student_answer.is_correct = False
                student_answer.save()

                wrong += 1

        # -----------------------------
        # INTEGER TYPE
        # -----------------------------

        elif question.question_type == "integer":

            answer = request.POST.get(
                f"question_{question.id}"
            )

            if answer == "" or answer is None:

                skipped += 1
                continue

            try:
                value = int(answer)
            except:
                skipped += 1
                continue

            is_correct = (
                value ==
                question.correct_integer_answer
            )

            StudentAnswer.objects.create(
                attempt=attempt,
                question=question,
                integer_answer=value,
                is_correct=is_correct
            )

            if is_correct:

                correct += 1
                score += question.marks

            else:

                wrong += 1

    total_questions = questions.count()

    percentage = (
        round(
            (correct / total_questions) * 100,
            2
        )
        if total_questions
        else 0
    )

    attempt.score = score
    attempt.total_questions = total_questions
    attempt.correct_answers = correct
    attempt.wrong_answers = wrong
    attempt.skipped_answers = skipped
    attempt.percentage = percentage

    attempt.time_taken_seconds = int(
        request.POST.get(
            "time_taken",
            0
        )
    )

    attempt.save()

    # Keep only latest 5 attempts of this user

    old_attempts = TestAttempt.objects.filter(        
            user=request.user
    ).order_by("-submitted_at")

    if old_attempts.count() > 5:
        old_attempts[5:].delete()

    return redirect(
        "result_page",
        attempt_id=attempt.id
    )

# ==========================================================
# RESULT PAGE
# ==========================================================


@login_required
def result_page(request, attempt_id):

    attempt = get_object_or_404(

        TestAttempt,

        id=attempt_id,

        user=request.user

    )

    return render(

        request,

        "result.html",

        {

            "attempt": attempt

        }

    )


# ==========================================================
# ATTEMPT HISTORY
# ==========================================================


@login_required
def my_test_history(request):

    attempts = TestAttempt.objects.filter(

        user=request.user

    ).order_by("-submitted_at")

    return render(

        request,

        "attempt_history.html",

        {

            "attempts": attempts

        }

    )


# ==========================================================
# LOGOUT
# ==========================================================

from django.contrib.auth import logout


def logout_view(request):

    logout(request)

    return redirect("index")