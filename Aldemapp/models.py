from django.db import models
from django.contrib.auth.models import AbstractUser,User,Subject,Chapter
from django.dispatch import receiver
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


# Create your models here.

class Videos(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='videos')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,null=True, blank=True,related_name='video',default='')
    title = models.CharField(_("عنوان الفيديو"),max_length=255)
    video_file = models.FileField(_("الفيديو"),max_length=355,blank=True,null=True,upload_to='videos/')
    thumbnail = models.ImageField(_("غلاف المقطع"),max_length=255,upload_to='thumbnails/', blank=True, null=True)
    description = models.TextField(_("وصف الفيديو"), blank=True, null=True)
    order = models.PositiveIntegerField(_("ترتيب الفيديو"), default=0)

    def __str__(self):
        return f"{self.title} ({self.subject.name})"

    class Meta:
        verbose_name = "فيديو"
        verbose_name_plural = "فيديوهات"
        ordering = ['order']




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





class Notification(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('email' , 'الارسال الى الإيميل'),
        ('site', 'الارسال الى المنصة'),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    message = models.TextField()
    method = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default='site',verbose_name='طريقة الإرسال')
    is_read = models.BooleanField(default=False,verbose_name='مقروء من الطالب')
    is_for_all = models.BooleanField(default=False,verbose_name='إرسال لكل الطلاب')  # تحديد إذا كان الإشعار لجميع المستخدمين
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "إشعار"
        verbose_name_plural ="الإشعارات"


    def __str__(self):
        if self.is_for_all:
            return f"Notification for all users: {self.message[:30]}"
        return f"Notification for {self.user.username}: {self.message[:30]}"
    

