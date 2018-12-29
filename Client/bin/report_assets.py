#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib
import os
import sys

BASE_DIR = os.path.dirname(os.getcwd())
# 设置工作目录，使得包和模块能够正常导入
sys.path.append(BASE_DIR)
from conf import settings

'''
解决 UnicodeDecodeError: 'ascii' codec can't decode byte 0xe5 in position 0: ordinal not in range(128)
经过搜寻网络上的资料，发现是ascii编码的问题，在自己程序代码前面加上以下三句，即可解决问题：
'''
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def update_test(data):
    data = {'asset_data': json.dumps(data)}
    url = 'http://%s:%s%s' % (settings.Params['server'], settings.Params['port'], settings.Params['url'])
    print('正在将数据发送至： [%s]  ......' % url)
    
    try:
        data_encode = urllib.urlencode(data).encode()
        response = urllib.urlopen(url=url, data=data_encode)
        print('\033[31;1m发送完毕！\033[0m ')
        message = response.read().decode()
        print('返回结果: %s' % message)
    except Exception as e:
        message = '发送失败'
        print('\033[31;1m%s，%s\033[0m' % (message, e))

if __name__ == '__main__':
    windows_data = {
        "os_type": "Windows",
        "os_release": "7 64bit  6.1.7601 ",
        "os_distribution": "Microsoft",
        "asset_type": "server",
        "cpu_count": 2,
        "cpu_model": "Intel(R) Core(TM) i5-2300 CPU @ 2.80GHz",
        "cpu_core_count": 8,
        "ram": [
            {
                "slot": "A1",
                "capacity": 8,
                "model": "Physical Memory",
                "manufacturer": "kingstone ",
                "sn": "456"
            },

        ],
        "manufacturer": "Intel",
        "model": "P67X-UD3R-B3",
        "wake_up_type": 6,
        "sn": "00426-OEM-8992662-111112",
        "physical_disk_driver": [
            {
                "iface_type": "unknown",
                "slot": 0,
                "sn": "3830414130423230343234362020202020202021",
                "model": "KINGSTON SV100S264G ATA Device",
                "manufacturer": "(标准磁盘驱动器)",
                "capacity": 128
            },
            {
                "iface_type": "SATA",
                "slot": 1,
                "sn": "383041413042323023234362020102020202021",
                "model": "KINGSTON SV100S264G ATA Device",
                "manufacturer": "(标准磁盘驱动器)",
                "capacity": 2048
            },

        ],
        "nic": [
            {
                "mac": "14:CF:22:FF:48:35",
                "model": "[00000011] Realtek RTL8192CU Wireless LAN 802.11n USB 2.0 Network Adapter",
                "name": 11,
                "ip_address": "192.168.1.111",
                "net_mask": [
                    "255.255.255.0",
                    "64"
                ]
            },
            {
                "mac": "0A:01:27:00:00:01",
                "model": "[00000013] VirtualBox Host-Only Ethernet Adapter",
                "name": 13,
                "ip_address": "192.168.56.2",
                "net_mask": [
                    "255.255.255.0",
                    "64"
                ]
            },
            {
                "mac": "14:CF:22:FF:48:35",
                "model": "[00000017] Microsoft Virtual WiFi Miniport Adapter",
                "name": 17,
                "ip_address": "",
                "net_mask": ""
            },
            {
                "mac": "14:CF:22:FF:48:35",
                "model": "Intel Adapter",
                "name": 17,
                "ip_address": "192.1.1.2",
                "net_mask": ""
            },


        ]
    }


    linux_data = {
        "asset_type": "server",
        "manufacturer": "innotek GmbH",
        "sn": "00002",
        "model": "VirtualBox",
        "uuid": "E8DE611C-4279-495C-9B58-502B6FCED076",
        "wake_up_type": "Power Switch",
        "os_distribution": "Ubuntu",
        "os_release": "Ubuntu 16.04.3 LTS",
        "os_type": "Linux",
        "cpu_count": "2",
        "cpu_core_count": "4",
        "cpu_model": "Intel(R) Core(TM) i5-2300 CPU @ 2.80GHz",
        "ram": [
            {
                "slot": "A1",
                "capacity": 8,
            }
        ],
        "ram_size": 3.858997344970703,
        "nic": [],
        "physical_disk_driver": [
            {
                "model": "VBOX HARDDISK",
                "size": "50",
                "sn": "VBeee1ba73-09085303"
            }
        ]
    }
    
    update_test(windows_data)
    update_test(linux_data)
