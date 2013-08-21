from etherpadlite.models import Pad

def pads(context):
    return {'pads': Pad.objects.all() }
