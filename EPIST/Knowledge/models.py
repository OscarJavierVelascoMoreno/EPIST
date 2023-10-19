from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from datetime import date
from Users.models import User
from Projects.models import Project

KNL_STATE_CHOICES = (
    ("new", "Nuevo"),
    ("for_approval", "Por Aprobar"),
    ("approved", "Aprobado"),
    ("archived", "Archivado"),
)


# Models for Knowledge management
class KnowledgeType(models.Model):

    class Meta:
        verbose_name = "Tipo de Conocimiento"

    title = models.CharField(max_length=100, unique=True, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")

    def __str__(self):
        return self.title


class Knowledge(models.Model):

    class Meta:
        verbose_name = "Conocimiento"

    title = models.CharField(max_length=100, unique=True, verbose_name="Título")
    state = models.CharField(choices=KNL_STATE_CHOICES, default='new', verbose_name="Estado")
    type_id = models.ForeignKey(KnowledgeType, null=True, on_delete=models.SET_NULL, verbose_name="Tipo")
    project_id = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL, verbose_name="Proyecto")
    note = models.TextField(verbose_name="Descripción")
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='%(class)s_created', verbose_name="Creado Por")
    approved_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='%(class)s_approved', verbose_name="Aprobado Por")
    creation_date = models.DateField(default=timezone.now, verbose_name="Fecha de Creación")
    approved_date = models.DateField(blank=True, null=True, verbose_name="Fecha de Aprobación")
    active = models.BooleanField(default=True, verbose_name="Activo")

    def approve_knowledge(self):
        self.state = 'approved'
        self.approved_date = date.today()

    def archive_record(self):
        self.state = 'archived'
        self.active = False

    def __str__(self):
        return self.title


class KnowledgeStep(models.Model):

    class Meta:
        verbose_name = "Pasos de Conocimiento"

    title = models.CharField(max_length=100, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    image = models.ImageField(upload_to='uploads/KnowledgeSteps/', null=True, verbose_name="Imagen")
    knowledge_id = models.ForeignKey(Knowledge, on_delete=models.CASCADE, verbose_name="Conocimiento")
    creation_date = models.DateField(default=timezone.now, verbose_name="Fecha de Creación")
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name="Creado Por")

    def __str__(self):
        return self.title
