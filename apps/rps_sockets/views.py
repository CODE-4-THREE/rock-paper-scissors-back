# views.py

from django.http import HttpResponse
from asgiref.sync import async_to_sync
import json
from random import choice


from channels.generic.websocket import AsyncWebsocketConsumer



def game_ws_view(request):
    return HttpResponse("WebSocket endpoint for the game.")


def ws_game_consumer(message):
    choice_list = ["piedra", "papel", "tijera"]

    data = json.loads(message['text'])
    user_choice = data.get('choice')

    if user_choice not in choice_list:
        async_to_sync(message.channel.send)(
            json.dumps({'error': 'Opción no válida'}))
        return

    opponent_choice = choice(choice_list)

    result = get_winner(user_choice, opponent_choice)

    async_to_sync(message.channel_layer.group_send)(
        'game_room',
        {
            'type': 'send_choice',
            'user_choice': user_choice,
            'opponent_choice': opponent_choice,
            'result': result
        }
    )


def get_winner(user_choice, opponent_choice):
    if user_choice == opponent_choice:
        return 'Empate'
    elif (
        (user_choice == 'piedra' and opponent_choice == 'tijera') or
        (user_choice == 'papel' and opponent_choice == 'piedra') or
        (user_choice == 'tijera' and opponent_choice == 'papel')
    ):
        return 'Ganaste'
    else:
        return 'Perdiste'
