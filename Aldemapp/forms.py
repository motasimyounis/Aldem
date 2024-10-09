# myapp/forms.py
from django import forms
from django.contrib.auth.forms import *
from .models import *
from django.contrib.auth.models import *


class CustomUserCreationForm(UserCreationForm):
    package = forms.ModelChoiceField(queryset=Package.objects.all(), required=True, label="الباقة",empty_label="اختر باقتك",)
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), required=True,widget=forms.SelectMultiple(attrs={'class': 'input-field','placeholder':'المواد', }))



    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs.update({ 
            'class': 'input-field', 
            'name':'username', 
            'id':'username',
            'type':'text', 
            'placeholder':'اسم الطالب', 
            'maxlength': '20', 
            'minlength': '4', 
            }) 

                
        self.fields['email'].widget.attrs.update({ 
            'class': 'input-field', 
            'name':'email', 
            'id':'email', 
            'type':'email', 
            'placeholder':'البريد الإلكتروني', 
            }) 
        
    
        
        self.fields['university_name'].widget.attrs.update({ 
            'class': 'input-field', 
            'name':'university_name', 
            'id':'university_name', 
            'type':'text', 
            'placeholder':'اسم الجامعة', 
            'maxlength': '20', 
            'minlength': '2', 
            }) 

        self.fields['subjects'].widget.attrs.update({ 
                'class': 'input-field', 
                'name':'subjects', 
                'id':'subjects', 
                'type':'text', 
                'placeholder':'المواد',
                }) 

                   
        self.fields['phone_number'].widget.attrs.update({ 
            'class': 'input-field', 
            'name':'phone_number', 
            'id':'phone_number', 
            'type':'phone_number', 
            'placeholder':'رقم الجوال', 
            }) 
        

                  
     
             
        self.fields['password1'].widget.attrs.update({ 
            'class': 'input-field', 
            'name':'password1', 
            'id':'password1', 
            'type':'password', 
            'placeholder':'كلمة السر', 
            }) 
    
            
        self.fields['password2'].widget.attrs.update({ 
            'class': 'input-field', 
            'name':'password2', 
            'id':'password2', 
            'type':'password', 
            'placeholder':'  تأكيد كلمة السر', 
            }) 
    

          
        self.fields['student_type'].widget.attrs.update({ 
            'class': 'input-field', 
            'name':'student_type', 
            'id':'student_type', 
            }) 
    
        self.fields['package'].widget.attrs.update({ 
                    'class': 'input-field', 
                    'name':'package', 
                    'id':'package', 
                    'type':'text', 
                    'placeholder':'اسم الباقة', 
                    }) 
    
        def save(self, commit=True):
        # First save the user instance
            user = super().save(commit=False)
            
            # Save the User instance if commit is True
            if commit:
                user.save()

            # Handle many-to-many field `subjects`
            user.subjects.set(self.cleaned_data['subjects'])

            return user
   
    class Meta:
        model = User
        fields = ('username', 'email', 'university_name', 'phone_number', 'subjects','student_type','package', 'mac_address','password1', 'password2')




class ContactForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField()
    msg = forms.Textarea()

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
                          
        self.fields['phone_number'].widget.attrs.update({ 
            'class': 'box', 
            'name':'phone_number', 
            'id':'phone_number', 
            'type':'phone_number', 
            'placeholder':'رقم الجوال', 
            }) 
        

                
        self.fields['email'].widget.attrs.update({ 
            'class': 'box', 
            'name':'email', 
            'id':'email', 
            'type':'email', 
            'placeholder':'البريد الإلكتروني', 
            }) 
        
    
       
                
        self.fields['msg'].widget.attrs.update({ 
            'class': 'box', 
            'name':'msg', 
            'id':'msg', 
            'type':'textarea', 
            'placeholder':"اكتب رسالتك"
            }) 
        
    
    class Meta:
        model = Contact
        fields = ('email', 'phone_number','msg',)






class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'box','placeholder':'كلمة السر القديمة', }),      
        label='كلمة السر القديمة',  
        required=True)
    
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'كلمة السر الجديدة', 'class': 'box'}),
        label='كلمة السر الجديدة',
        required=True
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'تأكيد كلمة السر الجديدة', 'class': 'box'}),
        label='تأكيد كلمة السر الجديدة',
        required=True
    )
 
