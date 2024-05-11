# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from random import choice


class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'game_room'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        choice_list = ["piedra", "papel", "tijera"]
        user_choice = data.get('choice')

        if user_choice not in choice_list:
            await self.send(text_data=json.dumps({'error': 'Opción no válida'}))
            return

        opponent_choice = choice(choice_list)

        result = self.get_winner(user_choice, opponent_choice)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_choice',
                'user_choice': user_choice,
                'opponent_choice': opponent_choice,
                'result': result
            }
        )

    async def send_choice(self, event):
        user_choice = event['user_choice']
        opponent_choice = event['opponent_choice']
        result = event['result']

        await self.send(text_data=json.dumps({
            'user_choice': user_choice,
            'opponent_choice': opponent_choice,
            'result': result
        }))

    def get_winner(self, user_choice, opponent_choice):
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
