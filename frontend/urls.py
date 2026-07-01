from django.urls import path
from . import views

urlpatterns = [

    # =====================================================
    # LANDING
    # =====================================================

    path(
        "",
        views.landing_view,
        name="index"
    ),

    path(
        "policy/",
        views.policy_view,
        name="policy"
    ),


    # =====================================================
    # AUTHENTICATION
    # =====================================================

    path(
        "signup/",
        views.signup_view,
        name="signup"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),


    # =====================================================
    # PAYMENT
    # =====================================================


    path(
        "payment2/<int:course_id>/",
        views.payment2_view,
        name="payment2"
    ),

    path(
        "course-payment-success/<int:course_id>/",
        views.course_payment_success,
        name="course_payment_success"
    ),


    # =====================================================
    # HOME
    # =====================================================

    path(
        "home/",
        views.home_view,
        name="home"
    ),

    path(
        "live-search/",
        views.live_search,
        name="live_search"
    ),


    # =====================================================
    # PROFILE
    # =====================================================

    path(
        "profile/",
        views.profile_view,
        name="profile"
    ),

    path(
        "activity/",
        views.activity,
        name="activity"
    ),


    # =====================================================
    # TEACHER / COURSE
    # =====================================================

    path(
        "teacher/<int:id>/",
        views.teacher_courses,
        name="teacher_courses"
    ),

    path(
        "all-courses/",
        views.all_courses,
        name="all_courses"
    ),

    path(
        "course-access/<int:course_id>/",
        views.course_access,
        name="course_access"
    ),


    # =====================================================
    # LECTURES
    # =====================================================

    # (Future me agar lecture detail page banaoge to yaha add hoga)


    # =====================================================
    # TESTS
    # =====================================================

    path(
        "course/<int:course_id>/tests/",
        views.test_list,
        name="test_list"
    ),

    path(
        "test/<int:test_id>/",
        views.start_test,
        name="start_test"
    ),

    path(
        "test/<int:test_id>/submit/",
        views.submit_test,
        name="submit_test"
    ),

    path(
        "result/<int:attempt_id>/",
        views.result_page,
        name="result_page"
    ),

    path(
        "my-tests/",
        views.my_test_history,
        name="my_test_history"
    ),


    # =====================================================
    # AI DOUBT
    # =====================================================

    path(
        "doubt/",
        views.doubt_solver,
        name="doubt"
    ),


    # =====================================================
    # SUPPORT
    # =====================================================

    path(
        "contact-support/",
        views.contact_support,
        name="contact_support"
    ),

]