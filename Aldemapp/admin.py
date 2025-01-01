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
    list_display= ('subject','title','order','chapter')
    list_editable= ('order','chapter')
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


admin.site.register(Chapter)




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
        if obj.is_for_all:  # إذا كان الإشعار موجهًا للجميع
            if obj.method == 'email':  # إذا تم اختيار الإرسال عبر البريد الإلكتروني
                self.create_notifications_via_email(obj.message)  # فقط إرسال البريد
            elif obj.method == 'site':  # إذا تم اختيار الإرسال عبر الموقع
                self.create_notifications_via_site(obj.message)  # فقط إنشاء الإشعارات في الموقع
        else:  # إذا كان الإشعار لمستخدم واحد
            if obj.method == 'email':  # إذا كان الإرسال بالبريد فقط
                if obj.user and obj.user.email:
                    self.notify_user_with_email(obj.user.email, obj.message)  # إرسال بريد إلكتروني
            elif obj.method == 'site':  # إذا كان الإرسال عبر الموقع فقط
                super().save_model(request, obj, form, change)  # حفظ الإشعار في قاعدة البيانات


    def create_notifications_via_email(self, message):
        users = User.objects.exclude(email__isnull=True).exclude(email__exact='')
        email_messages = [
            ('إشعار جديد من منصة الأستاذة الدمرداش', message, settings.DEFAULT_FROM_EMAIL, [user.email]) for user in users
        ]
        send_mass_mail(email_messages, fail_silently=False)
        print(f"Emails sent successfully to {len(users)} users.")

    def create_notifications_via_site(self, message):
        users = User.objects.all()
        notifications = [
            Notification(user=user, message=message, is_for_all=True, method='site') for user in users
        ]
        Notification.objects.bulk_create(notifications)
        print(f"Site notifications created successfully for {len(users)} users.")

    def notify_user_with_email(self, email, message):
        send_mail(
            'إشعار جديد من منصة الأستاذة الدمرداش',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False
        )
        print(f"Email sent successfully to {email}.")

    def create_notification_for_user(self, user, message):
        Notification.objects.create(user=user, message=message, method='site')
        print(f"Site notification created for {user.username}.")

