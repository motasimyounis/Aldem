from .models import Notification

def unread_notifications_count(request):
    if not request.user.is_authenticated:
        return {'unread_count': 0}
    
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return {'unread_count': unread_count}
