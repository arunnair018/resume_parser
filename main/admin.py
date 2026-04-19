# Register your models here.
from django.contrib import admin
from .models import (
    Candidate, Resume, WorkExperience,
    Education, Skill, ResumeSkill, Certification, ParseJob
)

admin.site.register(Candidate)
admin.site.register(Resume)
admin.site.register(WorkExperience)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(ResumeSkill)
admin.site.register(Certification)
admin.site.register(ParseJob)