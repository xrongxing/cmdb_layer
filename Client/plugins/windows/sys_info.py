#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
import win32com
import wmi
'''    pip install pypiwin32 wmi    '''

def collect():
    data = {
        'os_type': platform.system(),
        'os_release': '%s %s %s' % (platform.release(), platform.architecture()[0], platform.version()),
        'os_distribution': 'Microsoft',
        'asset_type': 'server', 
    }
    # 获取硬件信息，并更新到字典
    win32obj = Win32Info()
    data.update(win32obj.get_cpu_info())
    data.update(win32obj.get_ram_info())
    data.update(win32obj.get_motherboard_info())
    data.update(win32obj.get_disk_info())
    data.update(win32obj.get_nic_info())
    # 返回数据
    return data

class Win32Info(object):
    def __init__(self):
        self.wmi_obj = wmi.WMI()
        self.wmi_service_obj = win32com.client.Dispatch('WbemScripting.SWbemLocator')
        self.wmi_service_connector = self.wmi_service_obj.ConnectServer('.', 'root\cimv2')

    def get_cpu_info(self):
        '''
        获取CPU的相关数据，这里只采集了三个数据，实际有更多，请自行选择需要的数据
        :return:
        '''
        data = {}
        cpu_lists = self.wmi_obj.Win32_Processor()
        cpu_core_count = 0
        for cpu in cpu_lists:
            cpu_core_count += cpu.NumberOfCores

        cpu_model = cpu_lists[0].Name
        data['cpu_count'] = len(cpu_lists)
        data['cpu_model'] = cpu_model
        data['cpu_core_count'] = cpu_core_count
        
        return data

    def get_ram_info(self):
        '''
        收集内存信息
        :return:
        '''
        # 定义空列表
        data = []
        ram_collections = self.wmi_service_connector.ExecQuery('Select * from Win32_PhysicalMemory')
        # 多条内存循环
        for item in ram_collections:
            # B容量转换成GB
            ram_size = int(int(item.Capacity) / (1024**3))
            item_data = {
                'slot': item.DeviceLocator.strip(),
                'capacity': ram_size,
                'model': item.Caption,
                'manufacturer': item.Manufacturer,
                'sn': item.SerialNumber,
            }
            # 循环一条内存信息后，把数据插入列表
            data.append(item_data)
        # 全部循环完后的列表数据给一个字典的ram键,再返回给调用方
        return {'ram': data}
    def get_motherboard_info(self):
        '''
        获取主板信息
        :return:
        '''
        computer_info = self.wmi.obj_Win32_ComputerSystem()[0]
        system_info = self.wmi_obj.Win32_OperatingSystem()[0]
        data = dict()
        data['manufacturer'] = computer_info.Manufacturer
        data['model'] = computer_info.Model
        data['wake_up_type'] = computer_info.WakeUpType
        data['sn'] = system_info.SerialNumber
        return data
    def get_disk_info(self):
        '''
        硬盘信息
        :return:
        '''
        data = []
        for disk in self.wmi_obj.Win32_DiskDrive():
            item_data = dict()
            iface_choices = ['SAS', 'SCSI', 'SATA', 'SSD',]
            for iface in iface_choices:
                if iface in disk.Model:
                    item_data['iface_type'] = iface
                    break
                else:
                    item_data['iface_type'] = 'unknown'
            item_data['slot'] = disk.Index
            item_data['sn'] = disk.SerialNumber
            item_data['model'] = disk.Model
            item_data['manufacturer'] = disk.Manufacturer
            item_data['capacity'] = int(int(disk.Size) / (1024 ** 3))
            data.append(item_data)
        return {'physical_disk_driver': data}

    def get_nic_info(self):
        '''
        网卡信息
        :return:
        '''
        data = []
        for nic in self.wmi_obj.Win32_NetworkAdapterConfiguration():
            if nic.MACAddress is not None:
                item_data = dict()
                item_data['mac'] = nic.MACAddress
                item_data['model'] = nic.Caption
                item_data['name'] = nic.Index
                if nic.IPAddress is not None:
                    item_data['ip_address'] = nic.IPAddress[0]
                    item_data['net_mask'] = nic.IPSubnet
                else:
                    item_data['ip_address'] = ''
                    item_data['net_mask'] = ''
                data.append(item_data)
        return {'nic': data}

if __name__ == '__main__':
    dic = collect()
    print(dic)
