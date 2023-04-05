from django.db import models

class Tracks(models.Model):
    klngTrackID = models.IntegerField(primary_key=True)
    strTrackTitle = models.CharField(max_length=255)
    strArtist = models.CharField(max_length=255, null=True, blank=True)
    strAlbum = models.CharField(max_length=255, null=True, blank=True)
    strRefTrCIMEB = models.CharField(max_length=255)
    durTrackLength = models.DurationField(null=True, blank=True)
    strFile = models.CharField(max_length=255, null=True, blank=True)
    ysnVinyl = models.BooleanField()

    class Meta:
        db_table = "Tracks"

    def __str__(self):
        return self.strTrackTitle

class Exercises(models.Model):
    klngExerciseID = models.IntegerField(primary_key=True)
    strRefExCIMEB = models.CharField(max_length=20, null=True)
    strExerciseEN = models.CharField(max_length=255, null=True)
    memDescriptionEN = models.TextField(null=True)
    ysnFilterOn = models.BooleanField(null=True)
    strExerciseTypeID = models.CharField(max_length=20, null=True)
    ysnLineV = models.BooleanField(null=True)
    ysnLineS = models.BooleanField(null=True)
    ysnLineC = models.BooleanField(null=True)
    ysnLineA = models.BooleanField(null=True)
    ysnLineT = models.BooleanField(null=True)

    class Meta:
        db_table = "Exercises"

    def __str__(self):
        return self.strExerciseEN
    
class ExerciseTrack(models.Model):
    exercise = models.ForeignKey(Exercises, on_delete=models.CASCADE)
    track = models.ForeignKey(Tracks, on_delete=models.CASCADE)
    strRefExCIMEB = models.CharField(max_length=20, null=True)
    strRefTrCIMEB = models.CharField(max_length=20, null=True)
    strVersRefExTrCIMEB = models.CharField(max_length=5, null=True)
    ysnFavorite = models.BooleanField(null=True)
    memUserComment = models.TextField(null=True)
    ysnLineV = models.BooleanField(null=True)
    ysnLineS = models.BooleanField(null=True)
    ysnLineC = models.BooleanField(null=True)
    ysnLineA = models.BooleanField(null=True)
    ysnLineT = models.BooleanField(null=True)
    ysnAt1 = models.BooleanField(null=True)
    ysnAt2 = models.BooleanField(null=True)
    ysnAt3 = models.BooleanField(null=True)
    ysnAt5 = models.BooleanField(null=True)
    ysnAtG = models.BooleanField(null=True)

    class Meta:
        db_table = "ExercisesTracks"

