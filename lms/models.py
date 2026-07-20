from django.db import models


# ==========================
# Course Model
# ==========================

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ==========================
# Video Lesson Model
# ==========================

class VideoLesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.title


# ==========================
# Quiz Model
# ==========================

class Quiz(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="quizzes"
    )
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


# ==========================
# Question Model
# ==========================

class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    question_text = models.TextField()

    def __str__(self):
        return self.question_text


# ==========================
# Answer Model
# ==========================

class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    answer_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text
    
# ==========================
# Student Progress Model
# ==========================

from django.contrib.auth.models import User


class StudentProgress(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="progress"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="student_progress"
    )

    lesson = models.ForeignKey(
        VideoLesson,
        on_delete=models.CASCADE,
        related_name="student_progress"
    )

    completed = models.BooleanField(default=False)

    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "lesson")

    def __str__(self):
        return f"{self.student.username} - {self.lesson.title}"    