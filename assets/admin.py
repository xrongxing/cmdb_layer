# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Asset)
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
admin.site.register(models.NewAssetApprovalZone)
