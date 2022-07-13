from django.http import HttpResponse
from django.shortcuts import render
from django.apps import AppConfig
from django.shortcuts import render
import json
from django.http import JsonResponse  #接口返回的是json，需要引入的信息
from django.views.decorators.csrf import csrf_exempt   #post接口需要引入的信息
import requests
import xlwt
@csrf_exempt

# def hello(request):
#     return HttpResponse("Hello world ! ")


def runoob(request):
    return render(request, 'runoob.html')


# '''POST接口'''
# def post(request):
#     if request.method == "GET": #获取判断请求方式
#         request_dict = request.body  #获取接口请求发送过来的信息
#         query = request_dict["query"] #获取接口请求发送过信息
#         '''
#         在这里可以写接口在发送请求后的一系列处理方法
#         '''
#         request_data = {"code":200,"message":"请求成功"}
#         return JsonResponse(request_data)
def get_packing(request):
    '此视图函数用于示意form表单的提交'
    if request.method == 'GET':
        # 返回表单
        return render(request, 'runoob.html')
    elif request.method == 'POST':
        # 返回表单提交内容的结果
        dic = dict(request.POST)
        print("提交的内容是:", dic)
        title = request.POST.getlist('title')[0]
        subTitle = request.POST.getlist('subTitle')[0]
        categoryId = request.POST.getlist('categoryId')[0]
        secondCategoryName = request.POST.getlist('secondCategoryName')[0]
        packagingType = request.POST.getlist('packagingType')[0]
        value = request.POST.getlist('value')[0]
        print(title)
        print(subTitle)
        print(categoryId)
        print(secondCategoryName)
        print(packagingType)
        print(value)
        # test_Preview('产品名称', '产品副标题', 12, '手撕面包', 1, '年轻时尚')
        test_Preview(title, subTitle, categoryId, secondCategoryName, packagingType, value)
        # html = request.POST.get("bunnyname", "") + "提交成功"
        return render(request, 'runoob.html')

def Url():
    # 测试环境
    # Url = 'https://test-api.smalld.cn/'
    # 正式环境
    Url = 'https://api.smalld.cn/'
    # 提案:生成包装V2接口
    DesignV2_url = Url + 'design-center/packaging/designV2'
    # 提案:包装预览接口
    Preview_url = Url + 'design-center/packaging/preview'
    return DesignV2_url, Preview_url

def Headers():
    Headers = {'Content-Type': 'application/json',
               'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHAiOiJ0YW9iYW8iLCJzb3VyY2UiOiJ0YW9iYW8iLCJjaGFubmVsIjoidGFvYmFvIiwidXNlcl9pZCI6MTQwOTU2OSwibW9iaWxlIjoiMTc2ODI0NDkzODgifQ.sgYHQp53ZaDElQy3PdRSKHCa21A-jGR_2UNrf3JBwWs'}
    return Headers

'''生成包装V2接口'''
def DesignV2(title, subTitle, categoryId, secondCategoryName, packagingType, value):
    url = Url()[0]
    headers = Headers()
    data = json.dumps(
        {
            "params": {
                "productType": 19,
                "productBaseInfo": {
                    "title": title,                       # 产品名称
                    "subTitle": subTitle,                 # 产品副标题
                    "categoryId": categoryId,             # 一级类目ID
                    "secondCategoryName": secondCategoryName,   # 二级类目名称
                    "customizedCategoryName": "",
                    "bagInfo": {
                        "packagingType": packagingType,   # 袋型信息
                        "transparencyType": 1,
                        "reqSetType": 1001,
                        "sizeInfo": {
                            "width": "150",
                            "height": "140",
                            "length": ""
                        }
                    },
                    "displayInfo": [{
                        "name": "产品本身",
                        "code": "secondCategoryName",
                        "attrText": secondCategoryName
                    }]
                },
                "logoInfo": {
                    "hasLogo": "true",
                    "logoName": "品牌名称品牌名称"
                },
                "version": "",
                "outstandingInfo": ["secondCategoryName"],
                "strategyParams": {
                    "composingStyle": {
                        "value": value,                     # 风格
                        "weight": 0
                    }
                },
                # "requestNo": "1534730122244915200"
            }
        }
    )
    run = requests.post(url=url, headers=headers, data=data)
    goodsId = run.json()['data']['list']
    # print(goodsId)
    for i in goodsId:
        print(i)
    return goodsId
    # for i in run.json()['data']['list']:
    #     print(i['goodsId'], i['composingId'])
    # return i['goodsId']

def test_DesignV22():
    DesignV2('产品名称名称', '产品副标题产品副标题', 12, '手撕面包', 1, '年轻时尚')
    # 呈现和呈现信息
    # goodsId = TestPacking.DesignV2(self, '产品名称名称', '产品副标题产品副标题', 12, '手撕面包', 1, '年轻时尚')
    # for i in goodsId:
    #     print(i)
    # return goodsId

def test_Preview(title, subTitle, categoryId, secondCategoryName, packagingType, value):
    '''将数据存入Excel表格'''
    # 创建excel表格类型文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 0表示不压缩
    # 在excel表格类型文件中建立一张sheet表单
    sheet = book.add_sheet('包装拉取的图片', cell_overwrite_ok=True)
    # 自定义列名
    col = ('goodsId', '板式ID', '正面图片链接', '反面图片链接')
    # 将列名写入菜单
    for r in range(4):
        sheet.write(0, r, col[r])
    lists = []
    for i in DesignV2(title, subTitle, categoryId, secondCategoryName, packagingType, value):
        goodsId = i['goodsId']
        composingId = i['composingId']
        # print(goodsId, composingId)
        url = Url()[1]
        headers = Headers()
        data = json.dumps(
            {
                "params": {
                    "goodsId": goodsId,
                    "productType": 19
                }
            }
        )
        run = requests.post(url=url, headers=headers, data=data)
        # print(run.json()['data'], composingId, len(Packing.test_DesignV2(self)))
        lista = [run.json()['data'], goodsId, composingId]
        # print('lista:', lista)

        # 将数据存入列表
        listb = []
        listb.append(lista[1])
        listb.append(lista[2])
        listb.append(lista[0]['frontImgUrl'])
        listb.append(lista[0]['backImgUrl'])
        # print('listb:', listb)
        lists.append(listb)
    # print(lists)
    for b in range(len(lists)):
        data = lists[b]
        for j in range(0, 4):
            sheet.write(b + 1, j, data[j])

    # 保存excel文件
    savepath = '/Users/yangwei/Desktop/包装拉取的图片.xls'
    book.save(savepath)