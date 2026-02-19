from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType

def render_to_pdf(template_src, context_dict={}):
    """
    Render a Django template to PDF and return it as an HttpResponse.
    """
    template = get_template(template_src)
    html  = template.render(context_dict)
    
    result = BytesIO()
    
    # Generate PDF
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def log_activity(user, obj, action_flag, message=''):
    """
    Log an activity to the recent activities list.
    """
    try:
        LogEntry.objects.log_action(
            user_id=user.pk,
            content_type_id=ContentType.objects.get_for_model(obj).pk,
            object_id=obj.pk,
            object_repr=str(obj),
            action_flag=action_flag,
            change_message=message
        )
    except Exception as e:
        # Fails silently to not break the main flow
        pass
