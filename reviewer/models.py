from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, help_text='Enter your full name')

    
class CourseItem(models.Model):
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    avg_usefulness_rating = models.FloatField(default=0)
    avg_easiness_rating = models.FloatField(default=0)

    def update_rating(self):
        ratings = Rating.objects.filter(course_item=self)
        usefulness_sum = 0
        easiness_sum = 0
        for rating in ratings:
            usefulness_sum += rating.rating_usefulness
            easiness_sum += rating.rating_easiness
        if len(ratings) == 0:
            self.avg_usefulness_rating = 0
            self.avg_easiness_rating = 0
        else:
            self.avg_usefulness_rating = usefulness_sum / len(ratings)
            self.avg_easiness_rating = easiness_sum / len(ratings)
        self.save()

    def __str__(self):
        return self.name + ' - ' + self.teacher + ' - ' + str(self.avg_usefulness_rating) + ' - ' + str(self.avg_easiness_rating)
    

class Rating(models.Model):
    course_item = models.ForeignKey(CourseItem, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # ratings cannot be empty
    rating_usefulness = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1 )
    rating_easiness = models.IntegerField(choices=[(i, i) for i in range(1, 6)] , default=1)
    comment = models.TextField(max_length=1000, default='')

    def __str__(self):
        return self.course_item.name + ' - ' + self.user.username + ' - ' + str(self.rating_usefulness) + ' - ' + str(self.rating_easiness)
    




