"""
Retired for now

from push_notifications.models import APNSDevice, GCMDevice
import logging
logger = logging.getLogger(__name__)


def push_message(user, msg, regid=None, extra=None):
    args = {}
    if regid:
        args['registration_id'] = regid
    else:
        args['user'] = user
        
    devs = APNSDevice.objects.filter(**args)
    if not devs:
        devs = GCMDevice.objects.filter(**args)
    
    if len(devs):
        device = devs.first()
        logger.debug('sending push to device')
        if extra:
            device.send_message(msg, badge=1, extra={'action':extra})
        else: 
            device.send_message(msg, badge=1)
        logger.debug('sent to device')
    else:
        logger.debug('Wanted to send a push, but could not find a device.')
"""
