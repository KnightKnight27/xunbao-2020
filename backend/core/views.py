from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import json

from .serializers import UserSerializer, SubmissionSerializer, QuestionSerializer, UserProfileSerializer, HintSerializer
from .models import Question, Submission, UserProfile, HintModel
import requests


def fb_get_fid(input_token):
    URL = "https://graph.facebook.com/debug_token"
    access_token = '206217843919244|EKo744gwUQJD-NBySyKd-1IUrRM'
    PARAMS = {'input_token': input_token, 'access_token': access_token}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()
    return data["data"]


def get_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def home(request):
    return redirect('api/')


class JWTViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        token = body_data['input']
        try:
            fid = fb_get_fid(token)
            userprofile = UserProfile.objects.get(fid=fid["user_id"])
            if userprofile is not None:
                token = get_token(userprofile)
                data = {
                    'fid': fid,
                    'access': token,
                }
                return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class UserProfileAPIViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    # queryset = UserProfile.objects.all()

    def get_queryset(self):
        fid = self.request.query_params.get('fid', None)
        user = UserProfile.objects.filter(fid=fid)
        return user

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class LeaderboardAPIViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):

        return Response([], status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class QuestionAPIView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    # queryset = Question.objects.all()

    def get_queryset(self):
        id = self.request.user.id
        user = UserProfile.objects.get(id=id)
        level = user.level
        return Question.objects.filter(no=level)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class SubmissionAPIView(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    def list(self, request, *arg, **kwargs):
        return Response([], status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        data = request.data
        id = self.request.user.id
        user = UserProfile.objects.get(id=id)
        data['user'] = user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class HintView(viewsets.ModelViewSet):
    serializer_class = HintSerializer
    queryset = HintModel.objects.all()

    def list(self, request, *arg, **kwargs):
        return Response([], status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    def create(self, request, *args, **kwargs):
        data = request.data
        id = self.request.user.id
        user = UserProfile.objects.get(id=id)
        data['user'] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


