from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Field, Chapter, Level, Method, DifficultyAspect, Student, StudentDifficulty, Activity
from .utils import generate_basic_expression  # custom utility to create expressions


def create_activity(request):
    student_name = request.GET.get('student_name')
    field_name = request.GET.get('field_name')
    chapter_name = request.GET.get('chapter_name')
    level_name = request.GET.get('level_name')
    
    if not (student_name and field_name and chapter_name and level_name):
        return JsonResponse({"error": "Missing required query parameters"}, status=400)

    student = get_object_or_404(Student, name=student_name)
    field = get_object_or_404(Field, name=field_name)
    chapter = get_object_or_404(Chapter, name=chapter_name, field=field)
    level = get_object_or_404(Level, name=level_name)

    difficulties = StudentDifficulty.objects.filter(student=student, chapter=chapter)

    if difficulties.exists():
        aspects = [difficulty.aspect for difficulty in difficulties]
        
        activity = (
            Activity.objects.filter(chapter=chapter, level=level, aspects_covered__in=aspects)
            .distinct()
            .first()
        )

        if not activity:
            expression, steps = generate_basic_expression()
            activity = Activity.objects.create(
                chapter=chapter, level=level, expression=expression
            )
            activity.aspects_covered.set(aspects)
    else:
        expression, steps = generate_basic_expression()
        activity = Activity.objects.create(
            chapter=chapter, level=level, expression=expression
        )

    methods_covered = {aspect.method.name for aspect in activity.aspects_covered.all()}

    response_data = {
        "field": field.name,
        "chapter": chapter.name,
        "level": level.name,
        "expression": activity.expression,
        "steps": steps,
        "difficulties_targeted": [aspect.name for aspect in activity.aspects_covered.all()],
        "methods_covered": list(methods_covered)
    }
    
    return JsonResponse(response_data)
