from django.db import models

class Athlete(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    sport = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=255, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    coach = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=255)
    sport = models.CharField(max_length=100)
    sport_code = models.CharField(max_length=20, null=True, blank=True)  # Allow null

    def __str__(self):
        return self.name 

class Medal(models.Model):
    medal_type = models.CharField(max_length=10, null=True, blank=True)  # Allow null
    medal_date = models.DateField(null=True, blank=True)  # Allow null
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, null=True, blank=True)
    discipline = models.CharField(max_length=255, null=True, blank=True)  # Allow null
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)  # Allow null

    def __str__(self):
        return f"{self.athlete.name if self.athlete else 'Unknown'} - {self.medal_type}"
