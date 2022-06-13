from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game, event

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
    
    def create(self, request):
        organizer = Gamer.objects.get(pk=request.data["organizer"])
        # game = Game.objects.get(pk=request.data["game"])
        # event_type = EventType.objects.get(pk=request.data["event_type"])
        
        # event = Event.objects.create(
        #     description=request.data["description"],
        #     date=request.data["date"],
        #     time=request.data["time"],
        #     # event_type=event_type,
        #     organizer=organizer,
        #     game=game
        # )
        # serializer = EventSerializer(event)
        # return Response(serializer.data)
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=organizer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        event = Event.objects.get(pk=pk)
        serializer = CreateEventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer')
        depth = 1
        
class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'game', 'description', 'date', 'time', 'organizer']