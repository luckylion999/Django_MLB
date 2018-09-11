from datetime import datetime

import logging
logger = logging.getLogger(__name__)


class MiddleLog(object):

    def process_request(self, request):
        logger.debug(str(request))
        logger.debug(str(request.GET))
