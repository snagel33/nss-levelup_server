from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game

class GameView(ViewSet):

    def retrieve(self, request, pk):
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def list(self, request):
        games = Game.objects.all()
        game_type = request.query_params.get('type', None)
        if game_type is not None:
            games = games.filter(game_type_id=game_type)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('game_type', 'title', 'maker', 'gamer', 'number_of_players', 'skill_level')
        depth = 1