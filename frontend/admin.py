from django.contrib import admin

from .models import (
    Profile,
    Slide,
    Teacher,
    Course,
    Lecture,
    PurchasedCourse,
    SupportTicket,
    Test,
    Question,
    Option,
    TestAttempt,
)


# =====================================================
# PROFILE
# =====================================================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "phone",
        "age",
        "gender",
        "city"
    )

    search_fields = (
        "user__username",
        "phone",
        "city"
    )


# =====================================================
# SLIDER
# =====================================================

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "section_id",
        "is_active"
    )

    list_filter = (
        "is_active",
    )


# =====================================================
# LECTURE INLINE
# =====================================================

class LectureInline(admin.TabularInline):

    model = Lecture

    extra = 1


# =====================================================
# COURSE INLINE
# =====================================================

class CourseInline(admin.TabularInline):

    model = Course

    extra = 1


# =====================================================
# TEACHER
# =====================================================

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )

    inlines = [
        CourseInline
    ]


# =====================================================
# COURSE
# =====================================================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        "course_name",
        "teacher",
        "price",
    )

    search_fields = (
        "course_name",
    )

    list_filter = (
        "teacher",
    )

    inlines = [
        LectureInline
    ]


# =====================================================
# PURCHASED COURSE
# =====================================================

@admin.register(PurchasedCourse)
class PurchasedCourseAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "course",
        "purchased_at"
    )

    search_fields = (
        "user__username",
        "course__course_name"
    )

    list_filter = (
        "course",
    )


# =====================================================
# SUPPORT
# =====================================================

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "category",
        "priority",
        "status",
        "created_at"
    )

    search_fields = (
        "user__username",
        "subject"
    )

    list_filter = (
        "status",
        "category",
        "priority"
    )


# =====================================================
# OPTION INLINE
# =====================================================

class OptionInline(admin.TabularInline):

    model = Option

    extra = 4


# =====================================================
# QUESTION INLINE
# =====================================================

class QuestionInline(admin.StackedInline):

    model = Question

    extra = 1


# =====================================================
# TEST
# =====================================================

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "course",
        "duration_minutes",
        "total_marks",
        "is_active"
    )

    search_fields = (
        "title",
    )

    list_filter = (
        "course",
        "is_active"
    )

    inlines = [
        QuestionInline
    ]


# =====================================================
# QUESTION
# =====================================================

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        "question_text",
        "test",
        "question_type",
        "marks"
    )

    list_filter = (
        "question_type",
    )

    search_fields = (
        "question_text",
    )

    inlines = [
        OptionInline
    ]


# =====================================================
# OPTION
# =====================================================

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):

    list_display = (
        "question",
        "option_text",
        "is_correct"
    )


# =====================================================
# TEST ATTEMPT
# =====================================================

@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "test",
        "attempt_number",
        "score",
        "percentage",
        "result",
        "submitted_at"
    )

    search_fields = (
        "user__username",
    )

    list_filter = (
        "result",
        "test",
    )

    readonly_fields = (
        "user",
        "test",
        "attempt_number",
        "score",
        "percentage",
        "submitted_at",
        "correct_answers",
        "wrong_answers",
        "skipped_answers",
        "time_taken_seconds",
    )