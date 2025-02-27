import datetime
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from apps.message.models import MessageProfileAssignment
from apps.notify.models import NotificationRecipient


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print(self.room_name)
        print(self.room_group_name)
        print(self.channel_name)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        print('CHAT MESSAGEEE')
        message = event['message']
        print('read_check' in message)
        if not 'read_check' in message:
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message': message
            }))
        else:
            try:
                message = message['message']
                message_id = message['id']
                dest_id = message['dest']['id']
                mpa = MessageProfileAssignment.objects.filter(message_id=message_id, profile_id=dest_id)
                print(mpa)
                if len(mpa) > 0:
                    mpa[0].read = True
                    mpa[0].save()
                    print(mpa[0].read)
            except Exception as e:
                print(e.__str__())

class NotifyConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'notify_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print("RECEIVE NotifyConsumerNotifyConsumerNotifyConsumerNotifyConsumerNotifyConsumer")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'notify_message',
                'message': message
            }
        )

    # Receive message from room group
    def notify_message(self, event):
        print('NOTIFY MESSAGEEE')
        message = event['message']
        print('read_check' in message)
        if not 'read_check' in message:
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message': message
            }))
        else:
            try:
                message = message['message']
                notify_id = message['id']
                mpa = NotificationRecipient.objects.filter(id=notify_id)
                print(mpa)
                if len(mpa) > 0:
                    mpa[0].reading_date = datetime.datetime.now()
                    mpa[0].save()
                    print(mpa[0].reading_date)
            except Exception as e:
                print(e.__str__())


class ReportConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'report_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        # Receive message from WebSocket

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'report_message',
                'message': message
            }
        )

        # Receive message from room group

    def report_message(self, event):
        print('REPORT MESSAGEEE')
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
