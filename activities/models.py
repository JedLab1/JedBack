from django.db import models

class Field(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Chapter(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='chapters')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.field.name} - {self.name}"

class Level(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Method(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='methods')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.chapter.name} - {self.name}"

class DifficultyAspect(models.Model):
    method = models.ForeignKey(Method, on_delete=models.CASCADE, related_name='aspects')
    name = models.CharField(max_length=100)  # e.g., "Common Divisors", "One Denominator is Multiple of Other"

    def __str__(self):
        return f"{self.method.name} - {self.name}"

class Student(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class StudentDifficulty(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='difficulties')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    aspect = models.ForeignKey(DifficultyAspect, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.name} - {self.chapter.name} - {self.method.name} - {self.aspect.name}"

class Activity(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='activities')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='activities')
    expression = models.TextField()  # Stores algebra expressions
    aspects_covered = models.ManyToManyField(DifficultyAspect, related_name='activities', blank=True)

    def __str__(self):
        return f"{self.chapter.field.name} - {self.chapter.name} ({self.level.name}): {self.expression}"
