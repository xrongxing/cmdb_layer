# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . import models, asset_handle

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
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
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
                pass
                return HttpResponse('已审批资产已经更新')
            else:
                # 数据库中没有相应的sn号，判断为未审批资产，进入新资产待审批区，更新或者创建资产。
                obj = asset_handle.NewAsset(request, data)
                response = obj.add_to_new_assets_zone()
                return HttpResponse(response)
                
        else:
            return HttpResponse('数据必须要有sn')
            
