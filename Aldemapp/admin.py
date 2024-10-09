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




admin.site.register(Videos)






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



admin.site.register(Profile)


