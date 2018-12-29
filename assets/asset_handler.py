#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from . import models
'''
解决 UnicodeDecodeError: 'ascii' codec can't decode byte 0xe5 in position 0: ordinal not in range(128)
经过搜寻网络上的资料，发现是ascii编码的问题，在自己程序代码前面加上以下三句，即可解决问题：
'''
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class NewAsset(object):
    def __init__(self, request, data):
        self.request = request
        self.data = data
    def add_to_new_assets_zone(self):
        ram_size = 0
        if self.data.get('ram'):
            for capacity in self.data.get('ram'):
                ram_size += capacity['capacity']
                print(ram_size)
        defaults = {
            'data': json.dumps(self.data),
            'asset_type': self.data.get('asset_type'),
            'manufacturer': self.data.get('manufacturer'),
            'model': self.data.get('model'),
            'ram_size': ram_size,
            'cpu_model': self.data.get('cpu_model'),
            'cpu_count': self.data.get('cpu_count'),
            'cpu_core_count': self.data.get('cpu_core_count'),
            'os_distribution': self.data.get('os_distribution'),
            'os_release': self.data.get('os_release'),
            'os_type': self.data.get('os_type'),
        }
        models.NewAssetApprovalZone.objects.update_or_create(sn=self.data['sn'], defaults=defaults)
        #models.NewAssetApprovalZone.objects.update_or_create(sn=self.data.get('sn'), defaults=defaults)
        return '资产已经加入或更新待审批区！'

def log(log_type, msg=None, asset=None, new_asset=None, request=None):
    '''
    记录日志
    '''
    event = models.EventLog()

    if log_type == 'upline':
        event.name = '%s <%s>:    上线' % (asset.name, asset.sn)
        event.asset = asset
        event.detail = '资产成功上线'
        event.user = request.user
    elif log_type == 'approve_failed':
        event.name = '%s <%s>:    审批失败' % (new_asset.asset_type, new_asset.sn)
        event.new_asset = new_asset
        event.detail = '审批失败: %s' % msg
        event.user = request.user
    event.save()

class ApproveAsset(object):
#class ApproveAsset():
    '''
    审批资产并上线。
    '''
    def __init__(self, request, asset_id):
        self.request = request
        self.new_asset = models.NewAssetApprovalZone.objects.get(id=asset_id)
        self.data = json.loads(self.new_asset.data)

    def asset_upline(self):
        func = getattr(self, '_%s_upline' % self.new_asset.asset_type)
        ret = func()
        return ret and True

    def _server_upline(self):
        asset = self._create_asset()
        try:
            self._create_manufacturer(asset) # 创建厂商
            self._create_server(asset)       # 创建服务器
            self._create_CPU(asset)          # 创建CPU
            self._create_RAM(asset)          # 创建内存
            self._create_disk(asset)         # 创建硬盘
            self._create_nic(asset)          # 创建网卡
            self._delete_original_asset()    # 从待审批资产区删除已审批上线的资产
        except Exception as e:
            asset.delete()
            log('approve_failed', msg=e, new_asset=self.new_asset, request=self.request)
            print(e)
            return False
        else:
            log('upline', asset=asset, request=self.request)
            print('新服务器上线')
            return True
    def _create_asset(self):
        '''
        创建资产并上线
        :return:
        '''
        asset = models.Asset.objects.create(
            asset_type = self.new_asset.asset_type,
            name = '%s: %s' % (self.new_asset.asset_type, self.new_asset.sn),
            sn = self.new_asset.sn,
            approved_by = self.request.user,
        )
        return asset
    def _create_manufacturer(self, asset):
        '''
        创建厂商
        :param asset:
        :return:
        '''
        # 判断数据中是否有厂商信息，再判断数据库中厂商是否已经存在，不存在才创建
        m = self.new_asset.manufacturer
        if m:
            manufacturer_obj,_ = models.Manufacturer.objects.get_or_create(name=m)
            asset.manufacturer = manufacturer_obj
            asset.save()
    def _create_server(self, asset):
        '''
        创建服务器
        :param asset:
        :return:
        '''
        models.Server.objects.create(
            asset = asset,
            model = self.new_asset.model,
            os_type = self.new_asset.os_type,
            os_distribution = self.new_asset.os_distribution,
            os_release = self.new_asset.os_release,
        )
    def _create_CPU(self, asset):
        '''
        创建CPU
        :param asset:
        :return:
        '''
        cpu = models.CPU.objects.create(asset=asset)
        cpu.cpu_model = self.new_asset.cpu_model
        cpu.cpu_count = self.new_asset.cpu_count
        cpu.cpu_core_count = self.new_asset.cpu_core_count
        cpu.save()
    def _create_RAM(self, asset):
        '''
        创建RAM
        :param asset:
        :return:
        '''
        ram_list = self.data.get('ram')
        # 如果一条ram数据都没有的话
        if not ram_list:
            return
        for ram_dict in ram_list:
            if not ram_dict.get('slot'):
                raise ValueError('未知插槽')
            ram = models.RAM()
            ram.asset = asset
            ram.sn = ram_dict.get('sn')
            ram.model = ram_dict.get('model')
            ram.manufacutrer = ram_dict.get('manufacutrer')
            ram.slot = ram_dict.get('slot')
            ram.capacity = ram_dict.get('capacity', 0)
            ram.save()
    def _create_disk(self, asset):
        '''
        创建disk
        :param asset:
        :return:
        '''
        disk_list = self.data.get('physical_disk_driver')
        if not disk_list:
            return
        for disk_dict in disk_list:
            if not disk_dict.get('sn'):
                raise ValueError('未知硬盘序列号')
            disk = models.Disk()
            disk.asset = asset
            disk.sn = disk_dict.get('sn')
            disk.slot = disk_dict.get('slot')
            disk.model = disk_dict.get('model')
            disk.manufacturer = disk_dict.get('manufacturer')
            disk.capacity = disk_dict.get('capacity', 0)
            iface = disk_dict.get('interface_type')
            if iface in ['SATA', 'SAS', 'SCSI', 'SSD', 'unknown',]:
                disk.interface_type = iface
            disk.save()
    def _create_nic(self, asset):
        '''
        创建nic
        :param asset:
        :return:
        '''
        nic_list = self.data.get('nic')
        if not nic_list:
            return
        for nic_dict in nic_list:
            if not nic_dict.get('mac'):
                raise ValueError('缺少mac地址')
            if not nic_dict.get('model'):
                raise ValueError('缺少网卡型号')
            nic = models.NIC()
            nic.asset = asset
            nic.name = nic_dict.get('name')
            nic.model = nic_dict.get('model')
            nic.mac = nic_dict.get('mac')
            nic.ip_address = nic_dict.get('ip_address')
            if nic_dict.get('net_mask'):
                if len(nic_dict.get('net_mask')) > 0:
                    nic.net_mask = nic_dict.get('net_mask')[0]
            nic.bonding = nic_dict.get('bonding')
            nic.save()
    def _delete_original_asset(self):
        '''
        这里的逻辑是已经审批上线的资产，就从待审批区删除。
        也可以设置为修改成已审批状态但不删除，只是在管理界面特别处理，不让再次审批，灰色显示。
        不过这样可能导致待审批区越来越大。
        :return:
        '''
        self.new_asset.delete() 
