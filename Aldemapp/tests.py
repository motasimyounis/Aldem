from django.test import TestCase
from django.contrib.auth.models import User
from Aldemapp.models import Notification
from Aldemapp.admin import NotificationAdmin
from django.contrib import admin

class NotificationPerformanceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # إنشاء 10,000 مستخدم
        users = [
            User(username=f"user{i}", email=f"user{i}@example.com", password="password123")
            for i in range(10000)
        ]
        User.objects.bulk_create(users)
        print("Test users created successfully.")

    def test_notification_creation_for_all_users(self):
        # إنشاء إشعار لجميع المستخدمين
        notification = Notification(message="Test notification for all users", is_for_all=True)
        admin_instance = NotificationAdmin(Notification, admin.site)

        # قياس الزمن المستغرق
        import time
        start_time = time.time()

        admin_instance.save_model(None, notification, None, False)

        elapsed_time = time.time() - start_time
        print(f"Time taken to create notifications and send emails: {elapsed_time:.2f} seconds")

        # التحقق من عدد الإشعارات في قاعدة البيانات
        self.assertEqual(Notification.objects.count(), 10000, "Not all notifications were created.")

    def test_individual_notification_creation(self):
        # إنشاء إشعار فردي
        user = User.objects.first()
        notification = Notification(user=user, message="Individual test notification", is_for_all=False)
        admin_instance = NotificationAdmin(Notification, admin.site)

        # قياس الزمن المستغرق
        import time
        start_time = time.time()

        admin_instance.save_model(None, notification, None, False)

        elapsed_time = time.time() - start_time
        print(f"Time taken to create an individual notification and send an email: {elapsed_time:.2f} seconds")

        # التحقق من الإشعار في قاعدة البيانات
        self.assertEqual(Notification.objects.filter(user=user).count(), 1, "Individual notification not created.")

