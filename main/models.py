import uuid
from django.db import models


class Candidate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)
    portfolio_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'candidates'

    def __str__(self):
        return self.full_name


class Resume(models.Model):
    class ParseStatus(models.TextChoices):
        PENDING = 'pending'
        PROCESSING = 'processing'
        DONE = 'done'
        FAILED = 'failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='resumes')
    raw_text = models.TextField(null=True, blank=True)
    file_url = models.TextField(null=True, blank=True)
    file_type = models.CharField(max_length=20, null=True, blank=True)  # pdf, docx, etc.
    parse_status = models.CharField(
        max_length=20,
        choices=ParseStatus.choices,
        default=ParseStatus.PENDING
    )
    parse_metadata = models.JSONField(default=dict, blank=True)
    parsed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'resumes'

    def __str__(self):
        return f"Resume({self.candidate.full_name} - {self.parse_status})"


class WorkExperience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='work_experiences')
    company = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'work_experiences'
        ordering = ['display_order']

    def __str__(self):
        return f"{self.title} at {self.company}"


class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, null=True, blank=True)
    field_of_study = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    gpa = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'education'
        ordering = ['display_order']

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    normalized_name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, null=True, blank=True)  # e.g. "frontend", "devops"

    class Meta:
        db_table = 'skills'

    def __str__(self):
        return self.name


class ResumeSkill(models.Model):
    class Proficiency(models.TextChoices):
        BEGINNER = 'beginner'
        INTERMEDIATE = 'intermediate'
        ADVANCED = 'advanced'
        EXPERT = 'expert'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='resume_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='resume_skills')
    proficiency_level = models.CharField(
        max_length=20,
        choices=Proficiency.choices,
        null=True,
        blank=True
    )
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    is_inferred = models.BooleanField(default=False)

    class Meta:
        db_table = 'resume_skills'
        unique_together = ('resume', 'skill')

    def __str__(self):
        return f"{self.skill.name} ({self.resume})"


class Certification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255, null=True, blank=True)
    issued_at = models.DateField(null=True, blank=True)
    expires_at = models.DateField(null=True, blank=True)
    credential_url = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'certifications'

    def __str__(self):
        return f"{self.name} by {self.issuer}"


class ParseJob(models.Model):
    class Status(models.TextChoices):
        QUEUED = 'queued'
        RUNNING = 'running'
        SUCCESS = 'success'
        FAILED = 'failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='parse_job')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED)
    parser_version = models.CharField(max_length=50, null=True, blank=True)
    attempt_count = models.PositiveIntegerField(default=0)
    error_message = models.TextField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'parse_jobs'

    def __str__(self):
        return f"ParseJob({self.resume} - {self.status})"