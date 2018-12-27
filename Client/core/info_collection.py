#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import platform

def linux_sys_info():
    from plugins.linux import sys_info
    return sys_info.collect()
    #return {'sssss': 'ssssss'}

def windows_sys_info():
    from plugins.windows import sys_info as win_sys_info
    return win_sys_info.collect()

class InfoCollection(object):
    def collect(self):
        try:
            #return {'pytest': platform.system()}
            func = getattr(self, platform.system())
            info_data = func()
            formatted_data = self.build_report_data(info_data)
            return formatted_data
        except AttributeError:
            sys.exit('未知系统: [%s]' % platform.system())
    def Linux(self):
        return linux_sys_info()
    def Windows(self):
        return windows_sys_info()
    def build_report_data(self, data):
        return data
