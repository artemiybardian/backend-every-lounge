from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название аэропорта")
    code = models.CharField(max_length=10, unique=True,
                            verbose_name="Код аэропорта")
    city = models.CharField(max_length=100, verbose_name="Город")
    country = models.CharField(max_length=100, verbose_name="Страна")
    location = models.JSONField(
        null=False, verbose_name="Координаты (широта и долгота)")

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "Аэропорт"
        verbose_name_plural = "Аэропорты"


class Lounge(models.Model):
    airport_id = models.ForeignKey(
        Airport, related_name="lounges", on_delete=models.CASCADE, verbose_name="Аэропорт"
    )
    name = models.CharField(
        max_length=255, verbose_name="Название бизнес-зала")
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание")
    terminal = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Терминал")
    base_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Базовая цена")

    def __str__(self):
        return f"{self.name} - {self.airport_id.name}"

    class Meta:
        verbose_name = "Бизнес-зал"
        verbose_name_plural = "Бизнес-залы"


class LoungeSchedule(models.Model):
    lounge = models.ForeignKey(
        Lounge, related_name="schedule", on_delete=models.CASCADE, verbose_name="Бизнес-зал"
    )
    valid_from_time = models.TimeField(verbose_name="Время начала")
    valid_till_time = models.TimeField(verbose_name="Время окончания")
    valid_days = models.JSONField(
        verbose_name="Дни работы (например, ['mon', 'tue', ...])")

    class Meta:
        verbose_name = "График работы бизнес-зала"
        verbose_name_plural = "Графики работы бизнес-залов"


class EntryCondition(models.Model):
    lounge = models.ForeignKey(
        Lounge, related_name="entry_conditions", on_delete=models.CASCADE, verbose_name="Бизнес-зал"
    )
    type = models.IntegerField(
        verbose_name="Тип доступа (например, 0 - бесплатно, 1 - платно)")
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Стоимость")
    max_stay_duration = models.DurationField(
        verbose_name="Максимальная продолжительность пребывания")

    class Meta:
        verbose_name = "Условие входа"
        verbose_name_plural = "Условия входа"


class Feature(models.Model):
    lounge = models.ForeignKey(
        Lounge, related_name="features", on_delete=models.CASCADE, verbose_name="Бизнес-зал"
    )
    name = models.CharField(
        max_length=100, verbose_name="Название услуги (например, 'wifi', 'snacks')")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class GalleryImage(models.Model):
    lounge = models.ForeignKey(
        Lounge, related_name="gallery", on_delete=models.CASCADE, verbose_name="Бизнес-зал"
    )
    image_url = models.URLField(verbose_name="URL изображения")

    class Meta:
        verbose_name = "Изображение галереи"
        verbose_name_plural = "Изображения галереи"
