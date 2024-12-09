from django.contrib import admin
from .models import Field, Chapter, Level, Method, DifficultyAspect, Student, StudentDifficulty, Activity

class FieldAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'field')
    search_fields = ('name',)
    list_filter = ('field',)

class LevelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class MethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'chapter')
    search_fields = ('name', 'chapter__name')
    list_filter = ('chapter',)

class DifficultyAspectAdmin(admin.ModelAdmin):
    list_display = ('name', 'method')
    search_fields = ('name', 'method__name')
    list_filter = ('method',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class StudentDifficultyAdmin(admin.ModelAdmin):
    list_display = ('student', 'chapter', 'aspect')
    list_filter = ('student', 'chapter', 'aspect')
    search_fields = ('student__name', 'chapter__name', 'aspect__name')

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'level', 'expression', 'get_aspects')
    search_fields = ('expression', 'chapter__name', 'level__name')
    list_filter = ('chapter', 'level', 'aspects_covered')
    
    def get_aspects(self, obj):
        return ", ".join([aspect.name for aspect in obj.aspects_covered.all()])
    get_aspects.short_description = 'Aspects Covered'

# Register your models with the admin interface
admin.site.register(Field, FieldAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Method, MethodAdmin)
admin.site.register(DifficultyAspect, DifficultyAspectAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(StudentDifficulty, StudentDifficultyAdmin)
admin.site.register(Activity, ActivityAdmin)
