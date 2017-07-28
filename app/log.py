# -*- coding: utf-8 -*-
import logging

_app_log = logging.getLogger('tornado.application')

debug_log = _app_log.debug
info_log = _app_log.info
warning_log = _app_log.warning
error_log = _app_log.error
