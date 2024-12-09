from django.contrib import admin
from .models import *
from django import forms
from django.contrib.auth.models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from markdownx.widgets import MarkdownxWidget


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


