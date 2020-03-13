from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from rest_framework.response import Response
from social_django.models import UserSocialAuth

from .serializers import UserSerializer,SubmissionSerializer,QuestionSerializer,UserProfileSerializer, HintSerializer
from .models import Question,Submission,Answer,UserProfile, HintModel
from .forms import AnswerForm
# Create your views here.


def login(request):
    logout(request)
    return render(request, 'login.html')


def home(request):
    # user = request.user
    #
    # try:
    #     facebook = user.social_auth.get(provider='facebook')
    #     picture = facebook.extra_data.get('picture')
    #     picturedata = picture.get('data')
    #     pictureurl = picturedata.get('url')
    #     userprofile,created = UserProfile.objects.get_or_create(
    #         user=user,
    #     )
    #
    # except:
    #     pass

    return redirect('api/')


@login_required
def QuestionView(request, no):
    user = request.user

    if user.userprofile.level == no:
        question = Question.objects.get(no=no)
        answers = Answer.objects.filter(ques=question).values_list('answer', flat=True)
        print(answers)
        if request.method == 'POST':
            answerform = AnswerForm(request.POST)
            if answerform.is_valid():
                answer = answerform.cleaned_data['answer']
                if answer.lower() in answers:
                    ##function to get score

                    submission = Submission.objects.create(answer=answer, user=user, question=question, response='Correct')
                else:
                    submission = Submission.objects.create(answer=answer,user=user,question=question)

                answerform.save()
        else:
            answerform = AnswerForm(request.POST)

        context = {
            'user': user,
            'question': question,
            'answers': answers,
        }
        return render(request, 'core/question.html', context, {'form': answerform})


# API VIEWS

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class UserProfileAPIViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class QuestionAPIView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class SubmissionAPIView(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    # def create(self, request, *args, **kwargs):
    #     context = {'request': request}
    #     serializer = SubmissionSerializer(context, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class HintView(viewsets.ModelViewSet):
    serializer_class = HintSerializer
    queryset = HintModel.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
