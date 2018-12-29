# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models
from . import asset_handler

class NewAssetAdmin(admin.ModelAdmin):
    list_display = ['asset_type', 'sn', 'model', 'manufacturer', 'c_time', 'm_time']
    list_filter = ['asset_type', 'manufacturer', 'c_time']
    search_fields = ('sn',)
    actions = ['approve_selected_new_assets',]

    def approve_selected_new_assets(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        success_upline_number = 0
        if selected:
            for asset_id in selected:
                obj = asset_handler.ApproveAsset(request, asset_id)
                rel = obj.asset_upline()
                if rel:
                    success_upline_number += 1
            self.message_user(request, '成功批准  %s  条新资产上线！' % success_upline_number)
        else:
            self.message_user(request, '请选择要操作的项')
    approve_selected_new_assets.short_description = '批准选择的新资产'
            

class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_type', 'name', 'status', 'approved_by', 'c_time', "m_time"]

# Register your models here.
admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.Server)
admin.site.register(models.SecurityDevice)
admin.site.register(models.StorageDevice)
admin.site.register(models.NetworkDevice)
admin.site.register(models.Software)
admin.site.register(models.IDC)
admin.site.register(models.Manufacturer)
admin.site.register(models.BusinessUnit)
admin.site.register(models.Contract)
admin.site.register(models.Tag)
admin.site.register(models.CPU)
admin.site.register(models.RAM)
admin.site.register(models.Disk)
admin.site.register(models.NIC)
admin.site.register(models.EventLog)
admin.site.register(models.NewAssetApprovalZone, NewAssetAdmin)
