from django.db import IntegrityError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import NoteSerializer
from .models import Note


# Create your views here.
class BaseNoteView(GenericAPIView):
    serializer_class = NoteSerializer
    queryset = Note.objects


class ListNoteView(BaseNoteView):

    def get(self, request):
        try:
            notes = self.queryset.all()
            serializer = self.serializer_class(notes, many=True)
            return Response({
                'notes': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({'message': f'{error}'}, status=status.HTTP_400_BAD_REQUEST)


class AddNoteView(BaseNoteView):

    def post(self, request):
        try:
            note_data = request.data

            topic: str = note_data.get('topic')
            info: str = note_data.get('info')
            new_note = Note(
                topic=topic.strip(), info=info.strip()
            )
            new_note.save()
            serializer = self.serializer_class(new_note, many=False)
            return Response({
                'note': serializer.data
            }, status=status.HTTP_201_CREATED)
        except  IntegrityError as error:
            return Response({'message': f'{error}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'message': f'{error}'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateNoteView(BaseNoteView):

    def patch(self, request, id):
        try:
            data = request.data
            note = self.queryset.get(id=id)
            serializer = self.serializer_class(data=data, instance=note, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'note': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': 'not valid'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Note.DoesNotExist:
            return Response({'message': 'Note does not exist'}, status=status.HTTP_404_NOT_FOUND)


class DeleteNoteView(BaseNoteView):

    def delete(self, request, id):
        try:
            note = self.queryset.get(id=id)
            note.delete()
            return Response({'messsage': 'success'}, status=status.HTTP_200_OK)
        except Note.DoesNotExist:
            return Response({'message': 'Note does not exist'}, status=status.HTTP_404_NOT_FOUND)
