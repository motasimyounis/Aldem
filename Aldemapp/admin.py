from django.contrib import admin
from .models import *
from django import forms
from django.contrib.auth.models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from markdownx.widgets import MarkdownxWidget
from django.core.mail import send_mass_mail
from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from django.core.exceptions import ValidationError
from django.utils.text import Truncator
import logging

logger = logging.getLogger(__name__)



User = get_user_model()

# Unregister the default User admin
admin.site.unregister(User)
admin.site.unregister(Group)







admin.site.site_title = 'ALDEMERDASH'
admin.site.site_header = 'ALDEMERDASH'





class VideosAdmin(admin.ModelAdmin):
    list_display= ('subject','title','order',)
    list_editable= ['order']
    search_fields = ['subject__name', 'title']
    list_filter = ('subject','title')



admin.site.register(Videos,VideosAdmin)








class ContactAdmin(admin.ModelAdmin):
    list_display= ('email','msg','phone_number','msg_date')
    
    

admin.site.register(Contact,ContactAdmin)









class subjectAdmin(admin.ModelAdmin):
    list_display= ('id','name',)
    

admin.site.register(Subject,subjectAdmin)



class ServicesAdmin(admin.ModelAdmin):
    list_filter = ('id','name')  
    search_fields = ('id','name')
    

admin.site.register(Services)





class PackageAdminForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'
        widgets = {
            'points': MarkdownxWidget(),
        }

class packageAdmin(admin.ModelAdmin):
    form = PackageAdminForm
    list_display= ('name','price')
    

admin.site.register(Package,packageAdmin)







class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (_('اسم الباقة المشترك بها'), {'fields': ('package',)}),
    )

admin.site.register(User, CustomUserAdmin)




class ProfileAdmin(admin.ModelAdmin):
    list_display= ('user','device_id')
    list_editable= ['device_id']
    search_fields = ['user__username']
    list_filter = ['user__email','user__username']




admin.site.register(Profile,ProfileAdmin)



@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('short_message', 'user', 'is_for_all', 'is_read', 'created_at')
    list_filter = ('is_for_all', 'is_read', 'created_at')
    search_fields = ('message', 'user__email')
    readonly_fields = ('is_read',)

    def short_message(self, obj):
        truncator = Truncator(obj.message)
        return truncator.chars(50, truncate='...')

    short_message.admin_order_field = 'message'
    short_message.short_description = 'Message'

    def save_model(self, request, obj, form, change):
        if obj.is_for_all:
            # إنشاء الإشعارات لجميع المستخدمين
            self.create_notifications_for_all_users(obj.message)
        else:
            super().save_model(request, obj, form, change)
            if obj.user and obj.user.email:
                self.notify_user_with_email(obj.user.email, obj.message)

    def create_notifications_for_all_users(self, message):
        """إنشاء الإشعارات وإرسال البريد لجميع المستخدمين"""
        users = User.objects.exclude(email__isnull=True).exclude(email__exact='')

        # إنشاء الإشعارات في قاعدة البيانات
        notifications = [
            Notification(user=user, message=message, is_for_all=True) for user in users
        ]
        Notification.objects.bulk_create(notifications)  # إنشاء السجلات دفعة واحدة

        # إعداد رسائل البريد الإلكتروني
        email_messages = [
            ('إشعار جديد من منصة الأستاذة الدمرداش', message, settings.DEFAULT_FROM_EMAIL, [user.email]) for user in users
        ]

        try:
            if email_messages:
                send_mass_mail(email_messages, fail_silently=False)
                print(f"Emails sent successfully to {len(users)} users.")
        except Exception as e:
            logger.error(f"Error sending email notifications: {str(e)}")
            print(f"Error: {e}")

    def notify_user_with_email(self, email, message):
        """إرسال إشعار بالبريد الإلكتروني لمستخدم فردي"""
        try:
            send_mail(
                'إشعار جديد من منصة الأستاذة الدمرداش',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False
            )
            print(f"Email sent successfully to {email}.")
        except Exception as e:
            logger.error(f"Error sending email to {email}: {str(e)}")
            print(f"Error sending email to {email}: {e}")

