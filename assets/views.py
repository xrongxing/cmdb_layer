# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from . import models, asset_handler

# Create your views here.
@csrf_exempt
def report(request):
    '''
    通过csrf_exempt装饰器，跳过Django的csrf安全机制，让post的数据能被接收，但这又会带来新的安全问题。
    可以在客户端，使用自定义的认证token，进行身份验证。这部分工作，请根据实际情况，自己进行。
    :param request:
    :return:
    '''
    if request.method == 'POST':
        if request.POST.get('asset_data'):
            asset_data = request.POST.get('asset_data')
            data = json.loads(asset_data)
        else:
            return HttpResponse('没有POST数据 asset_data')
        # 各种数据检查，请自行添加和完善！
        if not data:
            return HttpResponse('没有数据')
        if not issubclass(dict, type(data)):
            return HttpResponse('数据必须为字典格式')
        sn = data.get('sn', None)
        if sn:
            # 进入审批流程
            # 首先判断是否在上线资产中存在该sn
            asset_obj = models.Asset.objects.filter(sn=sn)
            if asset_obj:
                # 进入已经上线资产的数据更新流程
                update_asset = asset_handler.UpdateAsset(request, asset_obj[0], data)
                return HttpResponse('已审批资产已经更新')
            else:
                # 数据库中没有相应的sn号，判断为未审批资产，进入新资产待审批区，更新或者创建资产。
                obj = asset_handler.NewAsset(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
                
        else:
            return HttpResponse('数据必须要有sn')
            

def dashboard(request):
    total = models.Asset.objects.count()
    upline = models.Asset.objects.filter(status=0).count()
    offline = models.Asset.objects.filter(status=1).count()
    unknown = models.Asset.objects.filter(status=2).count()
    breaddown = models.Asset.objects.filter(status=3).count()
    backup = models.Asset.objects.filter(status=4).count()
    up_rate = round(upline/total*100)
    o_rate = round(offline/total*100)
    un_rate = round(unknown/total*100)
    bd_rate = round(breaddown/total*100)
    bu_rate = round(backup/total*100)
    server_number = models.Server.objects.count()
    networkdevice_number = models.NetworkDevice.objects.count()
    storagedevice_number = models.StorageDevice.objects.count()
    securitydevice_number = models.SecurityDevice.objects.count()
    software_number = models.Software.objects.count()
    return render(request, 'assets/dashboard.html', locals())
def index(request):
    asset = models.Asset.objects.all()
    return render(request, 'assets/index.html', locals())
def detail(request, asset_id):
    asset = get_object_or_404(models.Asset, id = asset_id)
    return render(request, 'assets/detail.html', locals())
