from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import AlbumImage
from channels.db import database_sync_to_async


class AlbumConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.album_id = self.scope['url_route']['kwargs']['album_id']
        self.album_group_name = 'album_%s' % self.album_id

        await self.channel_layer.group_add(
            self.album_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.album_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def update_database_record(self,image_id,is_selected,sheet_number,position,priority):
        album_image = AlbumImage.objects.get(id=image_id)
        if is_selected :
            album_image.isSelected = is_selected
        if sheet_number:
            album_image.sheetNumber = sheet_number
        if position :
            album_image.position = position
        if priority :
            album_image.priority = priority
        album_image.save()
        return True



    async def receive(self, text_data):
        data = json.loads(text_data)
        image_id = data['image_id']
        is_selected = data['is_selected']
        sheetNumber = data['sheet_number']
        position = data['position']
        priority = data['priority']

        # Update the database
        album_image = await self.update_database_record(image_id,is_selected,sheetNumber,position,priority)
        print(album_image)

        # Broadcast the update to all clients in the album group
        await self.channel_layer.group_send(
            self.album_group_name,
            {
                'type': 'update_album_image',
                'image_id': image_id,
                'is_selected': is_selected,
                'sheet_number': sheetNumber,
                'position': position,
                'priority': priority
            }
        )



    async def update_album_image(self, event):
        image_id = event['image_id']
        is_selected = event['is_selected']
        sheetNumber = event['sheet_number']
        position = event['position']
        priority = event['priority']

        # Send the update to the client
        await self.send(text_data=json.dumps({
            'image_id': image_id,
            'is_selected': is_selected,
            'sheet_number': sheetNumber,
            'position': position,
            'priority': priority
        }))
