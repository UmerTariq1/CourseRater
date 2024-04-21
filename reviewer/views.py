from .models import CourseItem, Rating
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from .forms import CustomUserCreationForm
import json 

# Create your views here.

def course_list(request):
    if request.method == 'GET':
        # For now, let's create some mock data
        # use the table: CourseItem
        courses = CourseItem.objects.all()
        # update the rating for each course using the update_rating method

        for course in courses:
            course.update_rating()
            # round the rating to 2 decimal places
            course.avg_usefulness_rating = round(course.avg_usefulness_rating, 2)
            course.avg_easiness_rating = round(course.avg_easiness_rating, 2)


        context = {'courses': courses}

    return render(request, 'reviewer/homepage.html', context)



class course_detail(View):

    def get_course_data(self, course_id):
        # use the table: CourseItem
        course_review = CourseItem.objects.get(course_id=course_id)

        # use the table: Rating
        reviews = Rating.objects.filter(course_item=course_review)
        # add the user name to the review
        for review in reviews:
            review.reviewer_name = review.user.full_name
        
        course_review.update_rating()
        course_review.avg_usefulness_rating = round(course_review.avg_usefulness_rating, 2)
        course_review.avg_easiness_rating = round(course_review.avg_easiness_rating, 2)

        # get the user rating for the course if the user is logged in and has rated the course
        user_review = {}
        if self.request.user.is_authenticated:
            user_rating = Rating.objects.filter(course_item=course_review, user=self.request.user)
            if user_rating:
                print("user_rating[0] : ", user_rating[0])
                user_review["rating_usefulness"] = user_rating[0].rating_usefulness
                user_review["rating_easiness"] = user_rating[0].rating_easiness
                user_review["comment"] = user_rating[0].comment

        reviews_json = json.dumps(list(reviews.values()))
        course_review_json = json.dumps({'course_id': course_review.course_id, 'name': course_review.name, 'teacher': course_review.teacher, 'avg_usefulness_rating': course_review.avg_usefulness_rating, 'avg_easiness_rating': course_review.avg_easiness_rating})

        context = {'course_review': course_review, 'reviews': reviews, 'user_review': user_review, 'reviews_json': reviews_json, 'course_review_json': course_review_json}
        return context
    
    def get(self, request, course_id):
        context = self.get_course_data(course_id)
        return render(request, 'reviewer/course_details.html', context)

    def post(self, request, course_id):
        print("User rated the course")
        rating_usefulness = request.POST['usefulness']
        rating_easiness = request.POST['easiness']
        comment = request.POST['comment']
        # get the user
        user = request.user

        # check if the user has already rated the course
        user_rating = Rating.objects.filter(course_item=course_id, user=user)
        if user_rating:
            print("User has already rated the course. Updating the rating")
            user_rating = user_rating[0]
            user_rating.rating_usefulness = rating_usefulness
            user_rating.rating_easiness = rating_easiness
            user_rating.comment = comment
            user_rating.save()
        else:
            print("User has not rated the course. Adding the rating")
            course = CourseItem.objects.get(course_id=course_id)
            rating = Rating(course_item=course, user=user, rating_usefulness=rating_usefulness, rating_easiness=rating_easiness, comment=comment)
            rating.save()
        context = self.get_course_data(course_id)
        return render(request, 'reviewer/course_details.html', context)


@csrf_protect
def register_request(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Make sure to import Django's login function
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': "Username already taken"}, status=400)

    else:
        return JsonResponse({'error': "Invalid request"}, status=400)
    


def login_request(request):
    if request.method == "POST":
        print("------------- Logging in ---------------")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)
    else:
        print("------------- Logging in 2 ---------------")
        return JsonResponse({'Invalid request': True})
    

@require_POST
@csrf_exempt
def logout_request(request):
    print("------------- Logging out ---------------")
    logout(request)
    return JsonResponse({'success': 'Logged out successfully'}, status=200)