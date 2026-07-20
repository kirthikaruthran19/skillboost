from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CourseViewSet,
    VideoLessonViewSet,
    QuizViewSet,
    QuestionViewSet,
    AnswerViewSet,
    StudentProgressViewSet,
    ai_generate_quiz,
    generate_certificate,
    completed_courses,
    complete_course,   # <-- ADD THIS
)
router = DefaultRouter()

router.register("courses", CourseViewSet)
router.register("lessons", VideoLessonViewSet)
router.register("quizzes", QuizViewSet)
router.register("questions", QuestionViewSet)
router.register("answers", AnswerViewSet)
router.register("progress", StudentProgressViewSet, basename="progress")

urlpatterns = [
    path("", include(router.urls)),

    # AI Quiz
    path("generate-quiz/", ai_generate_quiz, name="generate-quiz"),

    # Complete Course
    path(
        "complete-course/",
        complete_course,
        name="complete-course",
    ),

    # Completed Courses API
    path(
        "completed-courses/",
        completed_courses,
        name="completed-courses",
    ),

    # Certificate Download
    path(
        "certificate/<int:course_id>/",
        generate_certificate,
        name="generate-certificate",
    ),
]