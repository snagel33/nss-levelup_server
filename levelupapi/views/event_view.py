from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event

class EventView(ViewSet):

    def retrieve(self, request, pk):
        event_type = Event.objects.get(pk=pk)
        serializer = EventSerializer(event_type)
        return Response(serializer.data)

    def list(self, request):
        event_types = Event.objects.all()
        serializer = EventSerializer(event_types, many=True)
        return Response(serializer.data)
    
class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = ('game', 'description', 'date', 'time', 'organizer')