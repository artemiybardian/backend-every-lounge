from django.db import models




class Airport(models.Model):
    name = models.CharField(max_length=255)
    # Код аэропорта
    code = models.CharField(max_length=10, unique=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    location = models.JSONField(null=False)  # Координаты (широта и долгота)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Lounge(models.Model):
    airport_id = models.ForeignKey(
        Airport, related_name="lounges", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    terminal = models.CharField(max_length=100, blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.airport.name}"


class LoungeSchedule(models.Model):
    lounge = models.ForeignKey(
        Lounge, related_name="schedule", on_delete=models.CASCADE)
    valid_from_time = models.TimeField()
    valid_till_time = models.TimeField()
    # Дни работы (например, ["mon", "tue", ...])
    valid_days = models.JSONField()


class EntryCondition(models.Model):
    lounge = models.ForeignKey(
        Lounge, related_name="entry_conditions", on_delete=models.CASCADE)
    type = models.IntegerField()  # Тип доступа (например, 0 - бесплатно, 1 - платно)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    max_stay_duration = models.DurationField()


class Feature(models.Model):
    lounge = models.ForeignKey(
        Lounge, related_name="features", on_delete=models.CASCADE)
    # Название услуги (например, "wifi", "snacks")
    name = models.CharField(max_length=100)


class GalleryImage(models.Model):
    lounge = models.ForeignKey(
        Lounge, related_name="gallery", on_delete=models.CASCADE)
    image_url = models.URLField()
