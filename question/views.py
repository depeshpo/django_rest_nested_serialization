from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from question.models import Question
from question.serializers import QuestionWriteSerializer, QuestionUpdateSerializer, QuestionReadSerializer


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestionWriteSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return QuestionUpdateSerializer
        else:
            return QuestionReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'message': 'Successfully created question',
                'status_code': 'HTTP_201_CREATED',
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({
                'message': 'Can not create question',
                'status_code': 'HTTP_400_BAD_REQUEST',
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                'message': "Successfully Updated question",
                "status_code": "HTTP_201_CREATED",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': "Can not Update question",
                "status_code": "HTTP_400_BAD_REQUEST",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
