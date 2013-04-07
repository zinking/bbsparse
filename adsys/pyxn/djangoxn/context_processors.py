def messages(request):
    """Returns messages similar to ``django.core.context_processors.auth``."""
    if hasattr(request, 'xiaonei') and request.xiaonei.uid is not None:
        from models import Message
        messages = Message.objects.get_and_delete_all(uid=request.xiaonei.uid)
    return {'messages': messages}