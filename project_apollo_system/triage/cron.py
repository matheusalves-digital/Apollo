from .models import Triage

def update_judicial_determination():
    for triage in Triage.objects.all():
        triage.save()
