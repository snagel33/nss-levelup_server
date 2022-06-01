from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event

class EventView(ViewSet):

    def retrieve(self, request, pk):
        try:
            event_type = Event.objects.get(pk=pk)
            serializer = EventSerializer(event_type)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        event_types = Event.objects.all()
        game = request.query_params.get('game', None)
        if game is not None:
            event_types = event_types.filter(game=game)
        serializer = EventSerializer(event_types, many=True)
        return Response(serializer.data)
    
class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = ('game', 'description', 'date', 'time', 'organizer')
        depth = 1