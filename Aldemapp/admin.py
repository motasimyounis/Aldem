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
    readonly_fields = ('is_read',)  # إضافة is_read للحقل القابل للقراءة فقط


    # طريقة لعرض أول 20 كلمة من الرسالة باستخدام Truncator
    def short_message(self, obj):
        truncator = Truncator(obj.message)
        return truncator.chars(50, truncate='...')  # تقطيع النص إلى 100 حرف فقط مع إضافة "..."

    short_message.admin_order_field = 'message'  # لجعل الترتيب بناءً على الرسالة الأصلية
    short_message.short_description = 'Message'  # تغيير عنوان العمود في الجدولMessage'  # تغيير عنوان العمود في الجدول


    def save_model(self, request, obj, form, change):
        if obj.is_for_all:  # إذا كان الإشعار لجميع المستخدمين
            # إرسال الإشعارات عبر البريد الإلكتروني لجميع المستخدمين
            self.notify_all_users_with_email(obj.message)
            # إضافة الإشعارات لجميع المستخدمين
            users = User.objects.exclude(email__isnull=True).exclude(email__exact='')
            notifications = [
                Notification(user=user, message=obj.message, is_for_all=True) for user in users
            ]
            Notification.objects.bulk_create(notifications)
        else:  # إشعار فردي
            super().save_model(request, obj, form, change)
            # إذا كان المستخدم لديه بريد إلكتروني صالح، أرسل إشعارًا بالبريد
            if obj.user and obj.user.email:
                self.notify_user_with_email(obj.user.email, obj.message)

    def notify_all_users_with_email(self, message):
        users = User.objects.exclude(email__isnull=True).exclude(email__exact='')

        email_messages = [
            ('إشعار جديد من منصة الأستاذة الدمرداش', message, settings.DEFAULT_FROM_EMAIL, [user.email]) for user in users
        ]

        try:
            if email_messages:
                send_mass_mail(email_messages, fail_silently=False)
                print("Emails sent successfully.")  # رسالة تأكيد عند الإرسال
        except Exception as e:
            logger.error(f"Error sending email notifications: {str(e)}")
            print(f"Error: {e}")  # طباعة الخطأ للتشخيص

    def notify_user_with_email(self, email, message):
        """إرسال إشعار بالبريد الإلكتروني لمستخدم فردي."""
        try:
            send_mail(
                'إشعار جديد من منصة الأستاذة الدمرداش',  # عنوان البريد
                message,  # محتوى البريد
                settings.DEFAULT_FROM_EMAIL,  # المرسل
                [email],  # المستقبل
                fail_silently=False
            )
            print(f"Email sent successfully to {email}.")  # تأكيد نجاح الإرسال
        except Exception as e:
            logger.error(f"Error sending email to {email}: {str(e)}")
            print(f"Error sending email to {email}: {e}")  # طباعة الخطأ
