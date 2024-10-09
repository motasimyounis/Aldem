from django.db import models
from django.contrib.auth.models import AbstractUser,User,Subject
from django.dispatch import receiver
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


# Create your models here.

class Videos(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(_("عنوان الفيديو"),max_length=255)
    video_file = models.FileField(_("الفيديو"),blank=True,null=True,upload_to='videos/')
    thumbnail = models.ImageField(_("غلاف المقطع"),upload_to='thumbnails/', blank=True, null=True)
    description = models.TextField(_("وصف الفيديو"), blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.subject.name})"

    class Meta:
        verbose_name = "فيديو"
        verbose_name_plural = "فيديوهات"




class Services(models.Model):     
    filter=[
        ('math','رياضيات'),
        ('counting','إحصاء'),
        ('phsic','فيزياء'),
        ('cimstry','كيمياء'),
        ('economy','إقتصاد'),
        ('etc','أخرى')
        ]  
    name = models.CharField(_("اسم المادة"),max_length=80)
    url = models.CharField(_("رابط قائمة التشغيل"),max_length=250)
    type = models.CharField(_("قسم المادة"),max_length=20,choices=filter,default='')
    
    
    def get_absolute_url(self):
        # This will return the URL for the details page of the specific service
        return reverse('exper')


    def __str__(self):
        return self.name
    

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'المحاضرات التجريبية'
        verbose_name_plural = 'المحاضرات التجريبية'






class Contact(models.Model):
    email = models.EmailField(_("البريد الإلكتروني"),blank=False,null=False)
    msg = models.TextField(_("رسالة الطالب"))
    phone_number = models.CharField(_("رقم الجوال"),max_length=15,)
    msg_date = models.DateTimeField(_("تاريخ الرسالة"),auto_now_add=True,blank=True,null=True)


    def __str__(self):
        return self.email
    
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'رسائل الطلاب'
        verbose_name_plural = 'رسائل الطلاب'




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=255, blank=True, null=True)
    device_info = models.CharField(max_length=255, blank=True, null=True)
    browser_fingerprint = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "معرف المستخدم"
        verbose_name_plural ="معرفات المستخدمين"