import ast
import json
import logging

import emoji
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from web.settings import BASE_URL, PROTOCOL
from web.utils import build_array_message
from . import models as project_models
from apps.notify import models as notify_models
from web.core.middleware.thread_local import get_current_profile
from web.core.utils import get_bell_notification_status, get_email_notification_status
from ..notify.signals import send_push_notification

# @receiver([post_save, post_delete], sender=project_models.Project)
# def project_notification(sender, instance, **kwargs):
#     company_staff = instance.profiles.all().union(
#         instance.company.get_owners_and_delegates()
#     )
#     profile = get_current_profile()
#     # If there is no JWT token in the request,
#     # then we don't create notifications (Useful at admin & shell for debugging)
#     if not profile:
#         return
#
#     try:
#         endpoint = '/apps/projects/{}'.format(str(instance.id))
#         if 'created' in kwargs:
#             if kwargs['created']:
#                 subject = _('New Project (%s) created in company (%s)'% (instance.name, instance.company.name))
#             else:
#                 subject = _('Project (%s) updated in company (%s)'% (instance.name, instance.company.name))
#         else:
#             subject = _('Project (%s) deleted in company (%s)'% (instance.name, instance.company.name))
#
#         body = json.dumps({
#             'content': subject.__str__(),
#             'url': endpoint
#         })
#         type = ContentType.objects.get(model=sender.__name__.lower())
#
#         notify_obj = notify_models.Notify.objects.create(
#             sender=profile, subject=subject, body=body,
#             content_type=type, object_id=instance.id,
#             creator=profile.user, last_modifier=profile.user
#         )
#
#         for staff in company_staff:
#             bell_status = get_bell_notification_status(
#                 staff, sender.__base__.__name__.lower()
#             )
#             email_status = get_email_notification_status(
#                 staff, sender.__base__.__name__.lower()
#             )
#
#             if bell_status or email_status:
#                 notify_recipient = notify_models.NotificationRecipient(
#                     notification=notify_obj, is_email=email_status,
#                     is_notify=bell_status, recipient=staff,
#                     creator=profile.user, last_modifier=profile.user)
#                 notify_recipient.save()
#                 send_push_notification(notify_obj, staff, body)
#
#     except Exception as e:
#         print(e)
from ..profile.models import Company

EMOJI_UNICODES = {
    'construction': '\U0001F3D7',
    'speech_baloon': '\U0001F4AC',
    'alarm': '\U0001F6A8',
    'brick': '\U0001F9F1',
    'stop': '\U0001F6A8',
    'stars': '\U00002728',
    'bullseye': '\U0001F3AF',
    'newspaper': '\U0001F4F0',
    'mailbox': '\U0001F4EC',
    'warning': '\U000026A0',
    'nopass': '\U0001F6B7',
    'checked': '\U00002705',
    'worker1': '\U0001F477',
    'worker2': '\U00002642',
    'activity': '\U00002692',
    'clipboard': '\U0001F4CB',
    'pushpin': '\U0001F4CC',
    'envelope': '\U0001F4E9'
}


def remove_team_member_notification(sender, instance):
    company_staff = instance.project.profiles.all().union(
        instance.project.company.get_owners_and_delegates()
    )
    profile = get_current_profile()
    # If there is no JWT token in the request,
    # then we don't create notifications (Useful at admin & shell for debugging)
    if not profile:
        return

    try:
        subject = build_array_message(EMOJI_UNICODES['construction'], [
            _('You have been removed from a project')
        ])
        endpoint = '/apps/projects'.format(str(instance.project.id))
        body = json.dumps({
            'content': build_array_message(None, [
                _('You have been removed from project'),
                instance.project.name,
                _('from company'),
                instance.project.company.name
            ]),
            'url': endpoint,
            'project_id': instance.project.id
        })
        type = ContentType.objects.get(model=sender.__name__.lower())

        notify_obj = notify_models.Notify.objects.create(
            sender=profile, subject=subject, body=body,
            content_type=type, object_id=instance.id,
            creator=profile.user, last_modifier=profile.user
        )

        bell_status = get_bell_notification_status(
            instance.profile, sender.__name__.lower()
        )
        email_status = get_email_notification_status(
            instance.profile, sender.__name__.lower()
        )
        translation.activate(profile.user.get_main_profile().language)
        if bell_status or email_status:
            notify_recipient = notify_models.NotificationRecipient(
                notification=notify_obj, is_email=email_status,
                is_notify=bell_status, recipient=instance.profile,
                creator=profile.user, last_modifier=profile.user)
            notify_recipient.save()
            send_push_notification(notify_obj, instance.profile, subject, body)
    except Exception as e:
        print(e)


def team_invite_notification(sender, instance, **kwargs):
    company_staff = instance.project.profiles.all().union(
        instance.project.company.get_owners_and_delegates()
    )
    profile = get_current_profile()
    # If there is no JWT token in the request,
    # then we don't create notifications (Useful at admin & shell for debugging)
    if not profile:
        return

    try:
        subject = build_array_message(EMOJI_UNICODES['construction'], [
            _('You have been invited in a project')
        ])
        endpoint = '/apps/projects'.format(str(instance.project.id))
        body = json.dumps({
            'content': build_array_message(None, [
                _('You have been invited in project'),
                instance.project.name,
                _('from company'),
                instance.project.company.name
            ]),
            'url': endpoint,
            'project_id': instance.project.id
        })
        type = ContentType.objects.get(model=sender.__name__.lower())

        notify_obj = notify_models.Notify.objects.create(
            sender=profile, subject=subject, body=body,
            content_type=type, object_id=instance.id,
            creator=profile.user, last_modifier=profile.user
        )

        bell_status = get_bell_notification_status(
            instance.profile, sender.__name__.lower()
        )
        email_status = get_email_notification_status(
            instance.profile, sender.__name__.lower()
        )
        translation.activate(profile.user.get_main_profile().language)
        if bell_status or email_status:
            notify_recipient = notify_models.NotificationRecipient(
                notification=notify_obj, is_email=email_status,
                is_notify=bell_status, recipient=instance.profile,
                creator=profile.user, last_modifier=profile.user)
            notify_recipient.save()
            send_push_notification(notify_obj, instance.profile, subject, body)
    except Exception as e:
        print(e)


@receiver([post_save, post_delete], sender=project_models.Team)
def team_notification(sender, instance, **kwargs):
    company_staff = instance.project.profiles.all().union(
        instance.project.company.get_owners_and_delegates()
    )
    profile = get_current_profile()
    # If there is no JWT token in the request,
    # then we don't create notifications (Useful at admin & shell for debugging)
    if not profile:
        return

    try:
        if 'created' in kwargs:
            if kwargs['created']:
                subject = build_array_message(EMOJI_UNICODES['worker1'], [
                    _('You have been added in a project')
                ])
                content = build_array_message(None, [
                    _('You have been added in project'),
                    instance.project.name
                ])
            else:
                return
        else:
            subject = build_array_message(EMOJI_UNICODES['worker1'], [
                _('You have been deleted from project')
            ])
            content = build_array_message(None, [
                _('User'),
                "{} {}".format(profile.first_name, profile.last_name),
                _('has removed you from project'),
                instance.project.name
            ])

        endpoint = '/apps/projects/{}/team'.format(str(instance.project.id))
        body = json.dumps({
            'content': content,
            'url': endpoint,
            'project_id': instance.project.id
        })
        type = ContentType.objects.get(model=sender.__name__.lower())

        notify_obj = notify_models.Notify.objects.create(
            sender=profile, subject=subject, body=body,
            content_type=type, object_id=instance.id,
            creator=profile.user, last_modifier=profile.user
        )

        for staff in company_staff:
            if 'created' in kwargs:
                if kwargs['created']:
                    if instance.profile.id == staff.id:
                        continue
            bell_status = get_bell_notification_status(
                staff, sender.__name__.lower()
            )
            email_status = get_email_notification_status(
                staff, sender.__name__.lower()
            )
            translation.activate(staff.user.get_main_profile().language)
            if bell_status or email_status:
                notify_recipient = notify_models.NotificationRecipient(
                    notification=notify_obj, is_email=email_status,
                    is_notify=bell_status, recipient=staff,
                    creator=profile.user, last_modifier=profile.user)
                notify_recipient.save()
                send_push_notification(notify_obj, staff, subject, body)
    except Exception as e:
        print(e)


@receiver([post_save, post_delete], sender=project_models.Task)
def task_notification(sender, instance, **kwargs):
    try:
        company_staff = instance.project.profiles.all().union(
            instance.project.company.get_owners_and_delegates()
        )
        profile = get_current_profile()
    except:
        return
    # If there is no JWT token in the request,
    # then we don't create notifications (Useful at admin & shell for debugging)
    if not profile:
        return

    try:
        if instance.assigned_company:
            company_staff = company_staff.union(
                instance.assigned_company.get_owners_and_delegates()
            )

        if instance.shared_task:
            company_staff = company_staff.union(
                instance.shared_task.project.company.get_owners_and_delegates()
            )

        if 'created' in kwargs:
            if kwargs['created']:
                subject = build_array_message(EMOJI_UNICODES['clipboard'], [
                    _('New assignment for your company')
                ])
            else:
                subject = _('Task (%s) updated in project (%s)' %
                            (instance.name, instance.project.name))
                return
        else:
            subject = _('Task (%s) deleted in project (%s)' %
                        (instance.name, instance.project.name))
            return

        endpoint = '/apps/projects/{}/task'.format(str(instance.project.id))
        body = json.dumps({
            'content': build_array_message(None, [
                _('Company'),
                instance.project.company.name,
                _('has assigned you task'),
                instance.name,
                _('in project'),
                instance.project.name
            ]),
            'url': endpoint,
            'project_id': instance.project.id
        })
        type = ContentType.objects.get(model=sender.__name__.lower())

        notify_obj = notify_models.Notify.objects.create(
            sender=profile, subject=subject, body=body,
            content_type=type, object_id=instance.id,
            creator=profile.user, last_modifier=profile.user
        )
        for staff in company_staff:
            bell_status = get_bell_notification_status(
                staff, sender.__name__.lower()
            )
            email_status = get_email_notification_status(
                staff, sender.__name__.lower()
            )
            translation.activate(staff.user.get_main_profile().language)
            if bell_status or email_status:
                notify_recipient = notify_models.NotificationRecipient(
                    notification=notify_obj, is_email=email_status,
                    is_notify=bell_status, recipient=staff,
                    creator=profile.user, last_modifier=profile.user)
                notify_recipient.save()
                body = json.loads(body)
                body['url'] = endpoint + '/{}/'.format(instance.id)
                body = json.dumps(body)
                send_push_notification(notify_obj, staff, subject, body)

    except Exception as e:
        print(e)


@receiver([post_save, post_delete], sender=project_models.Activity)
def activity_notification(sender, instance, **kwargs):
    try:
        company_staff = instance.workers.all().union(
            instance.task.project.company.get_owners_and_delegates()
        )
    except:
        return
    profile = get_current_profile()
    # If there is no JWT token in the request,
    # then we don't create notifications (Useful at admin & shell for debugging)
    if not profile:
        return

    try:
        if 'created' in kwargs:
            if kwargs['created']:
                subject = build_array_message(EMOJI_UNICODES['pushpin'], [
                    _('New activity assigned')
                ])
            else:
                subject = _('Activity').__str__() + " %s " % instance.title + \
                          _("updated in project").__str__() + \
                          " %s" % instance.task.project.name
                return
        else:
            subject = _('Activity').__str__() + " %s " % instance.title + \
                      _("deleted in project").__str__() + \
                      " %s" % instance.task.project.name
            return

        endpoint = '/apps/projects/{}/task'.format(
            str(instance.task.project.id))
        body = json.dumps({
            'content': build_array_message(None, [
                _('Person'),
                "{} {}".format(profile.first_name, profile.last_name),
                _('has assigned you activity'),
                instance.title,
                _('in project'),
                instance.task.project.name
            ]),
            'url': endpoint,
            'task_id': instance.task.id,
            'project_id': instance.task.project.id
        })
        type = ContentType.objects.get(model=sender.__name__.lower())

        notify_obj = notify_models.Notify.objects.create(
            sender=profile, subject=subject, body=body,
            content_type=type, object_id=instance.id,
            creator=profile.user, last_modifier=profile.user
        )

        for staff in company_staff:
            bell_status = get_bell_notification_status(
                staff, sender.__name__.lower()
            )
            email_status = get_email_notification_status(
                staff, sender.__name__.lower()
            )
            translation.activate(staff.user.get_main_profile().language)
            if bell_status or email_status:
                notify_recipient = notify_models.NotificationRecipient(
                    notification=notify_obj, is_email=email_status,
                    is_notify=bell_status, recipient=staff,
                    creator=profile.user, last_modifier=profile.user)
                notify_recipient.save()
                body = json.loads(body)
                body['url'] = endpoint + \
                              '/{}/activity/{}/'.format(instance.task.id, instance.id)
                body = json.dumps(body)
                send_push_notification(notify_obj, staff, subject, body)

    except Exception as e:
        print(e)


def alert_notification(sender, instance, **kwargs):
    try:
        if instance.sub_task is not None:
            company_staff = instance.sub_task.workers.all().union(
                instance.sub_task.task.project.company.get_owners_and_delegates()
            )
            post_for_model = 'activity'
        else:
            company_staff = instance.task.project.profiles.all().union(
                instance.task.project.company.get_owners_and_delegates()
            )
            post_for_model = 'task'

    except:
        return
    profile = get_current_profile()
    # If there is no JWT token in the request,
    # then we don't create notifications (Useful at admin & shell for debugging)
    if not profile:
        return

    try:
        if post_for_model == 'activity':
            if instance.alert:
                subject = build_array_message(EMOJI_UNICODES['alarm'], [
                    _('There is an issue in an activity')
                ])
                content = build_array_message(None, [
                    "{} {}".format(profile.first_name, profile.last_name),
                    _('has reported an issue in activity'),
                    instance.sub_task.title,
                    _('of project'),
                    instance.sub_task.task.project.name
                ])
            else:
                subject = build_array_message(EMOJI_UNICODES['stars'], [
                    _('Issue resolved in an activity')
                ])
                content = build_array_message(None, [
                    "{} {}".format(profile.first_name, profile.last_name),
                    _('has resolved an issue in activity'),
                    instance.sub_task.title,
                    _('of project'),
                    instance.sub_task.task.project.name
                ])
        else:
            if instance.alert:
                subject = build_array_message(EMOJI_UNICODES['alarm'], [
                    _('There is an issue in a task')
                ])
                content = build_array_message(None, [
                    _('User'),
                    "{} {}".format(profile.first_name, profile.last_name),
                    _('has reported an issue in task'),
                    instance.task.name,
                    _('of project'),
                    instance.task.project.name
                ])
            else:
                subject = build_array_message(EMOJI_UNICODES['stars'], [
                    _('Issue resolved in a task')
                ])
                content = build_array_message(None, [
                    _('User'),
                    "{} {}".format(profile.first_name, profile.last_name),
                    _('has resolved an issue in task'),
                    instance.task.name,
                    _('of project'),
                    instance.task.project.name
                ])

        try:
            endpoint = '/apps/projects/{}/task'.format(
                str(instance.task.project.id))
        except:
            endpoint = '/apps/projects/{}/task'.format(
                str(instance.sub_task.task.project.id))
        if instance.sub_task is not None:
            body = json.dumps({
                'content': content,
                'url': endpoint,
                'activity_id': instance.sub_task.id,
                'task_id': instance.sub_task.task.id,
                'project_id': instance.sub_task.task.project.id
            })
        else:
            body = json.dumps({
                'content': content,
                'url': endpoint,
                'task_id': instance.task.id,
                'project_id': instance.task.project.id
            })
        type = ContentType.objects.get(model=sender.__name__.lower())

        notify_obj = notify_models.Notify.objects.create(
            sender=profile, subject=subject, body=body,
            content_type=type, object_id=instance.id,
            creator=profile.user, last_modifier=profile.user
        )

        for staff in company_staff:
            bell_status = get_bell_notification_status(
                staff, sender.__name__.lower()
            )
            email_status = get_email_notification_status(
                staff, sender.__name__.lower()
            )
            translation.activate(staff.user.get_main_profile().language)
            if bell_status or email_status:
                notify_recipient = notify_models.NotificationRecipient(
                    notification=notify_obj, is_email=email_status,
                    is_notify=bell_status, recipient=staff,
                    creator=profile.user, last_modifier=profile.user)
                notify_recipient.save()
                body = json.loads(body)
                if post_for_model == 'task':
                    body['url'] = endpoint + \
                                  '/{}/post/{}/'.format(instance.task.id, instance.id)
                    body = json.dumps(body)
                    send_push_notification(notify_obj, staff, subject, body)
                else:
                    body['url'] = endpoint + '/{}/activity/{}/post/{}/'.format(
                        instance.sub_task.task.id, instance.sub_task.id, instance.id)
                    body = json.dumps(body)
                    send_push_notification(notify_obj, staff, subject, body)
    except Exception as e:
        print(e)


# @receiver([post_save, post_delete], sender=project_models.Post)
def post_notification(sender, instance, request, **kwargs):
    if not 'company_ids' in request.data:
        return
    company_ids = request.data['company_ids']
    print(company_ids)
    profile = get_current_profile()

    try:
        if instance.sub_task is not None:
            # if type_notify == 'mycompany':
            #     company_staff = instance.sub_task.workers.filter(company=profile.company)
            # if type_notify == 'mycompany_and_creator':
            #     company_staff = instance.sub_task.workers.filter(company__in=[profile.company, ])
            # if type_notify == 'all':
            # company_staff = instance.sub_task.workers.all().union(
            #     instance.sub_task.task.project.company.get_owners_and_delegates()
            # )
            companies_choosen = Company.objects.filter(id__in=company_ids)
            company_staff = instance.sub_task.task.project.profiles.filter(company__in=companies_choosen).union(
                instance.sub_task.task.project.company.get_owners_and_delegates()
            )
            post_for_model = 'activity'
        else:
            #  if instance.is_public:
            #    company_staff = instance.task.project.profiles.all().union(
            #         instance.task.project.company.get_owners_and_delegates()
            #     )
            # else:
            #     company_staff = instance.task.project.profiles.all().union(
            #         instance.task.project.company.get_owners_and_delegates()
            #     )
            companies_choosen = Company.objects.filter(id__in=company_ids)
            company_staff = instance.task.project.profiles.filter(company__in=companies_choosen).union(
                instance.task.project.company.get_owners_and_delegates()
            )
            post_for_model = 'task'
    except:
        return
    # If there is no JWT token in the request,
    # then we don't create notifications (Useful at admin & shell for debugging)
    if not profile:
        return

    try:
        if post_for_model == 'activity':
            subject = build_array_message(EMOJI_UNICODES['newspaper'], [
                'Nuovo post notificato'
            ])
            content = build_array_message(None, [
                "{} {}".format(profile.first_name, profile.last_name),
                "ha notificato il post",
                instance.sub_task.title,
                '\n"' + instance.text + '"'
            ])
        else:
            subject = build_array_message(EMOJI_UNICODES['newspaper'], [
                'Nuovo post notificato'
            ])
            content = build_array_message(None, [
                "{} {}".format(profile.first_name, profile.last_name),
                "ha notificato il post",
                instance.task.name,
                '\n"' + instance.text + '"'
            ])
        try:
            endpoint = '/apps/projects/{}/task'.format(str(instance.task.project.id))
        except:
            endpoint = '/apps/projects/{}/task'.format(str(instance.sub_task.task.project.id))
        if instance.sub_task is not None:
            body = json.dumps({
                'content': content,
                'url': endpoint,
                'big_picture': PROTOCOL + '://back-test.edilcloud.io' + instance.mediaassignment_set.all()[
                    0].media.url if instance.mediaassignment_set.all().count() > 0 else '',
                'activity_id': instance.sub_task.id,
                'task_id': instance.sub_task.task.id,
                'project_id': instance.sub_task.task.project.id
            })
        else:
            body = json.dumps({
                'content': content,
                'url': endpoint,
                'big_picture': PROTOCOL + '://back-test.edilcloud.io' + instance.mediaassignment_set.all()[
                    0].media.url if instance.mediaassignment_set.all().count() > 0 else '',
                'task_id': instance.task.id,
                'project_id': instance.task.project.id
            })
        type = ContentType.objects.get(model=sender.__name__.lower())

        notify_obj = notify_models.Notify.objects.create(
            sender=profile, subject=subject, body=body,
            content_type=type, object_id=instance.id,
            creator=profile.user, last_modifier=profile.user
        )

        for staff in company_staff:
            bell_status = get_bell_notification_status(
                staff, sender.__name__.lower()
            )
            email_status = get_email_notification_status(
                staff, sender.__name__.lower()
            )
            translation.activate(staff.user.get_main_profile().language)
            if bell_status or email_status:
                notify_recipient = notify_models.NotificationRecipient(
                    notification=notify_obj, is_email=email_status,
                    is_notify=bell_status, recipient=staff,
                    creator=profile.user, last_modifier=profile.user)
                notify_recipient.save()
                body = json.loads(body)
                if post_for_model == 'task':
                    body['url'] = endpoint + '/{}/post/{}/'.format(instance.task.id, instance.id)
                    body = json.dumps(body)
                    send_push_notification(notify_obj, staff, subject, body)
                else:
                    body['url'] = endpoint + '/{}/post/{}/'.format(instance.sub_task.id, instance.id)
                    body = json.dumps(body)
                    send_push_notification(notify_obj, staff, subject, body)
    except Exception as e:
        print(e)


# @receiver([post_save, post_delete], sender=project_models.Comment)
def comment_notification(sender, instance, kwargs=None):
    try:
        if instance.post.sub_task is not None:
            company_staff = instance.post.sub_task.workers.all().union(
                instance.post.sub_task.task.project.company.get_owners_and_delegates()
            )
            post_for_model = 'activity'
        else:
            company_staff = instance.post.task.project.profiles.all().union(
                instance.post.task.project.company.get_owners_and_delegates()
            )
            post_for_model = 'task'

    except Exception as e:
        logging.error(e.__str__())
    profile = get_current_profile()
    # If there is no JWT token in the request,
    # then we don't create notifications (Useful at admin & shell for debugging)
    if not profile:
        return

    try:
        if post_for_model == 'activity':
            subject = build_array_message(EMOJI_UNICODES['speech_baloon'], [
                _('There is a new comment')
            ])
            content = build_array_message(None, [
                "{} {}".format(profile.first_name, profile.last_name),
                _('has commented post'),
                instance.post.text[:50] + '..',
                _('in activity'),
                instance.post.sub_task.title,
                '\n"' + instance.text + '"'
            ])
        else:
            subject = build_array_message(EMOJI_UNICODES['speech_baloon'], [
                _('There is a new comment')
            ])
            content = build_array_message(None, [
                "{} {}".format(profile.first_name, profile.last_name),
                _('has commented post'),
                instance.post.text[:50] + '..',
                _('in task'),
                instance.post.task.name,
                '\n"' + instance.text + '"'
            ])
        print(subject)
        try:
            print('endpoint comment for task')
            endpoint = '/apps/projects/{}/task'.format(str(instance.post.task.project.id))
        except:
            print('endpoint comment for subtask')
            print(instance.post.sub_task.task)
            endpoint = '/apps/projects/{}/task'.format(str(instance.post.sub_task.task.project.id))
            print('---------------------------------')

        if instance.parent:
            body = {
                'content': content,
                'url': endpoint,
                'big_picture': PROTOCOL + '://back-test.edilcloud.io' + instance.mediaassignment_set.all()[
                    0].media.url if instance.mediaassignment_set.all().count() > 0 else '',
                'comment_id': instance.parent.id,
            }
        else:
            body = {
                'content': content,
                'big_picture': PROTOCOL + '://back-test.edilcloud.io' + instance.mediaassignment_set.all()[
                    0].media.url if instance.mediaassignment_set.all().count() > 0 else '',
                'url': endpoint,
            }
        if instance.post.task:
            body['task_id'] = instance.post.task.id
            body['project_id'] = instance.post.task.project.id
        else:
            body['task_id'] = instance.post.sub_task.task.id
            body['activity_id'] = instance.post.sub_task.id
            body['project_id'] = instance.post.sub_task.task.project.id

        body = json.dumps(body)
        type = ContentType.objects.get(model=sender.__name__.lower())

        notify_obj = notify_models.Notify.objects.create(
            sender=profile, subject=subject, body=body,
            content_type=type, object_id=instance.id,
            creator=profile.user, last_modifier=profile.user
        )

        for staff in company_staff:
            bell_status = get_bell_notification_status(
                staff, sender.__name__.lower()
            )
            email_status = get_email_notification_status(
                staff, sender.__name__.lower()
            )
            translation.activate(staff.user.get_main_profile().language)
            if bell_status or email_status:
                notify_recipient = notify_models.NotificationRecipient(
                    notification=notify_obj, is_email=email_status,
                    is_notify=bell_status, recipient=staff,
                    creator=profile.user, last_modifier=profile.user)
                notify_recipient.save()
                body = json.loads(body)
                if post_for_model == 'task':
                    body['url'] = endpoint + '/{}/post/{}/comment/{}/'.format(instance.post.task.id, instance.post.id,
                                                                              instance.id)
                    body = json.dumps(body)
                    send_push_notification(notify_obj, staff, subject, body)
                else:
                    body['url'] = endpoint + '/{}/activity/{}/post/{}/comment/{}/'.format(
                        instance.post.sub_task.task.id, instance.post.sub_task.id, instance.post.id, instance.id)
                    body = json.dumps(body)
                    send_push_notification(notify_obj, staff, subject, body)
    except Exception as e:
        logging.error(e.__str__())
