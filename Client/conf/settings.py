#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
Params = {
    'server': '192.168.1.209',
    'port': 58014,
    'url': '/assets/report/',
    'request_timeout': 30,
}

PATH = os.path.join(os.path.dirname(os.getcwd()), 'log', 'cmdb.log')
