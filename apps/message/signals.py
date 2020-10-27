# -*- coding: utf-8 -*-

import os
import emoji
import filetype
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from . import models as message_models
from apps.profile import models as profile_models
from apps.notify import models as notify_models
from web.core.middleware.thread_local import get_current_profile, get_current_request
from web.core.utils import get_html_message, get_bell_notification_status, get_email_notification_status
from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
from websocket import create_connection

from .models import MessageFileAssignment
from ..project.models import Project


def get_filetype(file):
    kind = filetype.guess(file)
    if kind is None:
        return
    return kind.mime

def get_files(obj):
    media_list = []
    request = get_current_request()
    medias = MessageFileAssignment.objects.filter(message=obj)
    for media in medias:
        try:
            photo_url = media.media.url
            protocol = request.is_secure()
            if protocol:
                protocol = 'https://'
            else:
                protocol = 'http://'
            host = request.get_host()
            media_url = protocol + host + photo_url
        except:
            media_url = None
        name, extension = os.path.splitext(media.media.name)
        if extension == '.mp3':
            type = 'audio/mp3'
        else:
            type = get_filetype(media.media)
        media_list.append(
            {
                "media_url": media_url,
                "id": media.id,
                "size": media.media.size,
                "name": name.split('/')[-1],
                "extension": extension,
                "type": type,
                "message": media.message.id
            }
        )
    return media_list

def addRedirectUrl(talk):
    if talk.content_type.name == 'company':
        return "https://www.edilcloud.it/apps/chat"
    if talk.content_type.name == 'project':
        return "https://www.edilcloud.it/apps/projects/{}".format(str(talk.object_id))
    return "https://www.edilcloud.it"

def addHeading(talk, notify_obj):
    if talk.content_type.name == 'company':
        return "{} Company Chat".format(notify_obj.sender.company.name)
    if talk.content_type.name == 'project':
        pr = Project.objects.filter(id=talk.object_id)
        if pr:
            return "{} Project Chat".format(pr[0].name)
        else:
            return "Project Chat"

@receiver([post_save, post_delete], sender=message_models.Message)
def message_notification(sender, instance, **kwargs):
    import requests
    import json

    company_staff = []
    profile = get_current_profile()
    # If there is no JWT token in the request,
    # then we don't create notifications (Useful at admin & shell for debugging)
    if not profile or instance.status == 0:
        return

    try:
        endpoint = os.path.join(settings.PROTOCOL+'://', settings.BASE_URL, 'comunica')
        if instance.talk.content_type.name == 'company':
            company_staff = instance.talk.content_object.profiles.all()
            title = instance.talk.content_type.name
            source = instance.talk.content_object.name
        elif instance.talk.content_type.name == 'project':
            endpoint = os.path.join(settings.PROTOCOL+'://', settings.BASE_URL, 'project')
            title = instance.talk.content_type.name
            company_staff = instance.talk.content_object.profiles.all().union(
                instance.talk.content_object.company.get_owners_and_delegates(),
                instance.sender.company.get_owners_and_delegates()
            )
            all_staff = instance.talk.content_object.internal_projects.all().values_list('profiles', flat=True)
            if all_staff:
                company_staff = company_staff.union(profile_models.Profile.objects.filter(id__in=all_staff))
            source = instance.talk.content_object.name
        elif instance.talk.content_type.name == 'profile':
            company_staff = [instance.talk.content_object]
            title = 'staff'
            source = instance.sender.last_name

        content = "Mr <strong>%s %s</strong> have created this event. " % (profile.first_name, profile.last_name)

        if 'created' in kwargs:
            if kwargs['created']:
                subject = _('New Message from %s (%s)' % (title, source))
            else:
                subject = _('Message updated by %s (%s)' % (title, source))
        else:
            subject = _('Message deleted by %s (%s)' % (title, source))

        final_content = "For simplicity, the following button will redirect to the target page."
        body = get_html_message(content, final_content, endpoint)
        type = ContentType.objects.get(model=instance.talk.content_type.name.lower())

        notify_obj = notify_models.Notify.objects.create(
            sender=profile, subject=subject, body=body,
            content_type=type, object_id=instance.talk.object_id,
            creator=profile.user, last_modifier=profile.user
        )

        recipient_objs = []

        for staff in company_staff:
            bell_status = get_bell_notification_status(
                staff, instance.talk.content_type.name
            )
            email_status = get_email_notification_status(
                staff, instance.talk.content_type.name
            )

            if bell_status or email_status:
                recipient_objs.append(notify_models.NotificationRecipient(
                    notification=notify_obj, is_email=email_status,
                    is_notify=bell_status, recipient=staff,
                    creator=profile.user, last_modifier=profile.user)
                )

        notify_models.NotificationRecipient.objects.bulk_create(
            recipient_objs,
            batch_size=100
        )
        # send push notification

        header = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Basic ZWI0NmI5NGItMTJjZC00YWJhLWI5YTUtNjA3MTQ1ZDgzM2Vl"
        }

        req_players = requests.get(
            "https://onesignal.com/api/v1/players?app_id=8fc7c8ff-a4c8-4642-823d-4675b809a3c9&limit=300&offset=0",
            headers=header)
        print(req_players)
        company_profiles = notify_obj.sender.company.profiles
        list_profiles_id = []
        list_players_recipients = []
        for profile in company_profiles.all():
            list_profiles_id.append(str(profile.id))
        print(req_players.status_code, req_players.json())

        for req_player in req_players.json()['players']:
            print('player external user id')
            print(str(req_player['external_user_id']))
            if str(req_player['external_user_id']) in list_profiles_id:
                list_players_recipients.append(req_player['id'])

        print('list ids')
        print(list_profiles_id)
        print('list players to sent')
        print(list_players_recipients)

        payload = {
            "app_id": "8fc7c8ff-a4c8-4642-823d-4675b809a3c9",
            "include_player_ids": list_players_recipients,
            "contents": {
                "en": "{} {}: {}".format(notify_obj.sender.first_name, notify_obj.sender.last_name, instance.body if instance.body != '' else emoji.emojize(':camera:'))
            },
            "headings": {
                "en": addHeading(instance.talk, notify_obj)
            },
            "data": {
                "custom_data": "New Message from Edilcloud",
                "redirect_url": addRedirectUrl(instance.talk)
            },
            "small_icon": "ic_stat_onesignal_default"
        }

        # "android_channel_id": "8d3bd99c-1755-4a33-a043-60a92c8b153c",
        # "wp_wns_sound": "erotic_girl_sound",
        # "android_sound": "erotic_girl_sound",

        req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
        print(req.status_code, req.reason)

        files = get_files(instance)
        # SOCKET_HOST = os.environ.get('SOCKET_HOST')
        # SOCKET_PORT = os.environ.get('SOCKET_PORT')
        # SOCKET_URL = os.environ.get('SOCKET_URL')
        # if SOCKET_URL:
        #     socketIO = SocketIO(SOCKET_URL)
        # else:
        #     socketIO = SocketIO(SOCKET_HOST, SOCKET_PORT)
        # socketIO.emit('join', {'room': str(instance.talk.code), 'name': 'django-admin'})
        # socketIO.emit("chat_channel", {
        #     "message": {
        #         "id": notify_obj.id,
        #         "body": instance.body,
        #         "unique_code": instance.unique_code,
        #         "read": False,
        #         "talk": {
        #             "id": instance.talk.id,
        #             "code": instance.talk.code,
        #             "content_type_name": instance.talk.content_type.name,
        #             "object_id": instance.talk.object_id
        #         },
        #         "sender": {
        #             "id": notify_obj.sender.id,
        #             "first_name": notify_obj.sender.first_name,
        #             "last_name": notify_obj.sender.last_name,
        #             "photo": None,
        #             "role": notify_obj.sender.role,
        #             "company": {
        #                 "id": notify_obj.sender.company.id,
        #                 "name": notify_obj.sender.company.name,
        #                 "category": {}
        #             }
        #         },
        #         "files": files
        #     }
        # })
        # socketIO.emit('leave', {'room': str(instance.talk.code), 'name': 'django-admin'})
        # socketIO.disconnect()

        from websocket import create_connection
        try:
            ws = create_connection("ws://35.176.179.55:8000/ws/chat/chat_channel/")
        except:
            ws = create_connection("wss://35.176.179.55:8000/ws/chat/chat_channel/")
        print("Sending 'Hello, World'...")
        profiles_to_send = instance.messageprofileassignment_set.all()
        for profile in profiles_to_send:
            ws.send(json.dumps(
                {
                    "message":  {
                        "id": notify_obj.id,
                        "body": instance.body,
                        "read": profile.read,
                        "unique_code": instance.unique_code,
                        "talk": {
                            "id": instance.talk.id,
                            "code": instance.talk.code,
                            "content_type_name": instance.talk.content_type.name,
                            "object_id": instance.talk.object_id
                        },
                        "sender": {
                            "id": notify_obj.sender.id,
                            "first_name": notify_obj.sender.first_name,
                            "last_name": notify_obj.sender.last_name,
                            "photo": None,
                            "role": notify_obj.sender.role,
                            "company": {
                                "id": notify_obj.sender.company.id,
                                "name": notify_obj.sender.company.name,
                                "category": {}
                            }
                        },
                        "dest": {
                            "id": profile.profile.pk
                        },
                        "files": files
                    }
                 }))
            print("Sent")
        ws.close()

    except Exception as e:
        print(e)