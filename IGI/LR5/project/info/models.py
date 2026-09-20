from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class AboutCompany(models.Model):
    """О компании"""
    title = models.CharField(
        max_length=200,
        default='О компании'
    )
    text = models.TextField(
        verbose_name='Текст о компании'
    )

    video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на видео'
    )

    logo = models.ImageField(
        upload_to='company/logo/',
        blank=True,
        null=True,
        verbose_name='Логотип'
    )
    history = models.TextField(
        blank=True,
        null=True,
        verbose_name='История по годам'
    )
    requisites = models.TextField(
        blank=True,
        null=True,
        verbose_name='Реквизиты'
    )
    certificate = models.TextField(
        blank=True,
        null=True,
        verbose_name='Сертификат'
    )
    class Meta:
        verbose_name = "О компании"
        verbose_name_plural = "О компании"
    def clean(self):
        if not self.pk and AboutCompany.objects.exists():
            raise ValidationError(
                "В базе может быть только одна запись об о компании."
            )
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class News(models.Model):
    """Новости"""
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    short_content = models.CharField(max_length=300, verbose_name='Краткое содержание')
    content = models.TextField(verbose_name='Полная статья')
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

class Review(models.Model):
    """Отзывы пользователей"""
    name = models.CharField(max_length=150, verbose_name='Имя')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оценка (1-5)'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')
    
    def __str__(self):
        return f'{self.name} — {self.rating}/5'
    
class Term(models.Model):
    """Словарь терминов и понятий"""
    question = models.CharField(
        max_length=255,
        verbose_name='Вопрос'
    )
    answer = models.TextField(
        verbose_name='Краткий ответ'
    )
    detailed_answer = models.TextField(
        blank=True,
        null=True,
        verbose_name='Развернутый ответ'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления'
    )
    def __str__(self):
        return self.question

class Partner(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название компании"
    )

    description = models.CharField(
        max_length=300,
        blank=True,
        default="",
        verbose_name="Описание"
    )

    website_url = models.URLField(
        verbose_name="Сайт компании"
    )

    logo = models.ImageField(
        upload_to="partners/",
        blank=True,
        null=True,
        verbose_name="Логотип"
    )

    logo_url = models.CharField(
        max_length=500,
        blank=True,
        default="",
        verbose_name="Логотип (URL или путь)"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Показывать на главной"
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок"
    )

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name