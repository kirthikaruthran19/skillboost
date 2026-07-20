from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from reportlab.pdfgen import canvas

from django.utils import timezone

import json

from .groq_service import generate_quiz

from .models import (
    Course,
    VideoLesson,
    Quiz,
    Question,
    Answer,
    StudentProgress,
)

from .serializers import (
    CourseSerializer,
    VideoLessonSerializer,
    QuizSerializer,
    QuestionSerializer,
    AnswerSerializer,
    StudentProgressSerializer,
)


# ==========================================================
# Course ViewSet
# ==========================================================

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by("-created_at")
    serializer_class = CourseSerializer


# ==========================================================
# Video Lesson ViewSet
# ==========================================================

class VideoLessonViewSet(viewsets.ModelViewSet):
    queryset = VideoLesson.objects.all()
    serializer_class = VideoLessonSerializer


# ==========================================================
# Quiz ViewSet
# ==========================================================

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


# ==========================================================
# Question ViewSet
# ==========================================================

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# ==========================================================
# Answer ViewSet
# ==========================================================

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


# ==========================================================
# AI Quiz Generator
# ==========================================================

@api_view(["POST"])
def ai_generate_quiz(request):

    course_id = request.data.get("course_id")

    if not course_id:
        return Response(
            {"error": "course_id is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    course = get_object_or_404(Course, id=course_id)

    try:
        quiz = generate_quiz(course.title)
        return Response(json.loads(quiz))

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ==========================================================
# Student Progress
# ==========================================================

class StudentProgressViewSet(viewsets.ModelViewSet):

    serializer_class = StudentProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return StudentProgress.objects.filter(
            student=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


# ==========================================================
# Completed Courses API
# ==========================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def completed_courses(request):

    completed_list = []

    courses = Course.objects.all()

    for course in courses:

        total_lessons = VideoLesson.objects.filter(
            course=course
        ).count()

        completed_lessons = StudentProgress.objects.filter(
            student=request.user,
            course=course,
            completed=True,
        ).count()

        if total_lessons > 0 and total_lessons == completed_lessons:

            latest_progress = StudentProgress.objects.filter(
                student=request.user,
                course=course,
                completed=True,
            ).order_by("-completed_at").first()

            completed_list.append(
                {
                    "id": course.id,
                    "title": course.title,
                    "completed": True,
                    "completed_at": latest_progress.completed_at,
                    "certificate_url": f"/api/certificate/{course.id}/",
                }
            )

    return Response(completed_list)


# ==========================================================
# Certificate Generator
# ==========================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def generate_certificate(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    total_lessons = VideoLesson.objects.filter(
        course=course
    ).count()

    completed_lessons = StudentProgress.objects.filter(
        student=request.user,
        course=course,
        completed=True,
    ).count()

    if total_lessons == 0 or completed_lessons != total_lessons:

        return Response(
            {
                "error": "Complete all lessons before downloading the certificate."
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = (
        f'attachment; filename="{course.title}_certificate.pdf"'
    )

    pdf = canvas.Canvas(response)

    width = 595
    height = 842

    pdf.setPageSize((width, height))
    pdf.setTitle("Certificate of Completion")

    # Border
    pdf.setStrokeColorRGB(0.1, 0.3, 0.8)
    pdf.setLineWidth(4)
    pdf.rect(30, 30, width - 60, height - 60)

    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(
    width / 2,
    790,
    "SkillBoost LMS"
)

    pdf.setFont("Helvetica", 15)
    pdf.drawCentredString(
    width / 2,
    770,
    "Online Learning Platform"
)

    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawCentredString(
    width / 2,
    725,
    "CERTIFICATE OF COMPLETION"
)

    # Subtitle
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        width / 2,
        710,
        "This certificate is proudly presented to"
    )

    # Student Name
    student_name = request.user.get_full_name() or request.user.username

    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(
        width / 2,
        660,
        student_name
    )

    pdf.line(140, 645, 455, 645)

    # Course Name
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        width / 2,
        600,
        "For successfully completing the course"
    )

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawCentredString(
        width / 2,
        560,
        course.title
    )

    # Issued By
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        width / 2,
        500,
        "Issued by SkillBoost LMS"
    )
    pdf.setFont("Helvetica", 13)

    pdf.drawCentredString(
    width / 2,
    470,
    f"Completion Date : {timezone.now().strftime('%d %B %Y')}"
)
    pdf.setFont("Helvetica", 13)

    pdf.drawCentredString(
    width / 2,
    470,
    f"Completion Date : {timezone.now().strftime('%d %B %Y')}"
)
    # Date
    pdf.setFont("Helvetica", 13)
    pdf.drawString(
        70,
        170,
        f"Issue Date: {timezone.now().strftime('%d %B %Y')}"
    )

    # Student
    pdf.drawString(
        70,
        145,
        f"Student: {request.user.username}"
    )

    pdf.line(360,170,520,170)

    pdf.drawCentredString(
    440,
    150,
    "Instructor"
)

    pdf.line(70,170,230,170)

    pdf.drawCentredString(
    150,
    150,
    "Student"
)

    pdf.showPage()
    pdf.save()

    return response




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def complete_course(request):

    course_id = request.data.get("course_id")

    course = get_object_or_404(Course, id=course_id)

    lessons = VideoLesson.objects.filter(course=course)

    for lesson in lessons:

        StudentProgress.objects.update_or_create(
            student=request.user,
            lesson=lesson,
            defaults={
                "course": course,
                "completed": True,
                "completed_at": timezone.now(),
            },
        )

    return Response({"message": "Course completed successfully"})