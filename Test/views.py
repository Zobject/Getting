from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from  django.shortcuts import render
from urllib import unquote
import datetime
import boto3
import base64
import json
from bson import json_util,ObjectId
import pymongo

try:
    conn=pymongo.MongoClient()
    print "success"
except pymongo.errors.ConnectionFailure,e:
    print "error %s"%e

db=conn['Mmcalculator']

@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    collection = db.my_collection
    if request.method=='GET':
        #id=data.get('id')
        return JsonResponse({"ok": 1})
    elif request.method == 'POST':
            data = JSONParser().parse(request)
            #print data
            user=data.get("usr")
            photourl=data.get("photourl")
            photosize=data.get("size")
            if photourl==None:
                print "none"
                data=list(collection.find({"deviceid":user}))
                print data
                return HttpResponse(json.dumps(data, default=json_util.default), status=200,
                                    content_type="application/json")

            else:
                data = {"deviceid":user,"photoslist":[{"name":photourl,"target":0,"size":photosize}]}
                #abc = data.get("name")
                #print abc
                if (collection.find({"deviceid": user}).count()> 0):
                    if(collection.update({"deviceid":user},{"$addToSet":{"photoslist":{"name":photourl,"target":0,"size":photosize}}})):
                        return JsonResponse({"target":"sucess"})
                    else:
                        return JsonResponse({"target": "failed"}, status=400)
                #print data
                collection.insert(data)
                #s=collection.find({"photourl":photourl}).next()
                #if (collection.find({"photourl": {"url":photourl}}).count()== 0):

            return JsonResponse({"target": "success"},status=201)
    elif request.method=='PUT':
        data=JSONParser().parse(request)
        user=data.get("usr")
        img=data.get("photourl")
        imgdcode=base64.b64decode(img)
        usercode=base64.b64decode(user)
        client=boto3.client("s3")
        if(client.delete_object(Bucket='mmcalculator1',
                             Key=usercode+"/"+imgdcode)):
            collection.update({"deviceid":user},{"$pull":{"photoslist":{"name":img}}})
            return JsonResponse({"target":"success"})
        return  JsonResponse({"false":1})
           # return JsonResponse(json.dumps(data,default=json_util.default),safe=False,status=201)

@csrf_exempt
def Userfeedback(request):
    collection = db.Userfeedback
    if request.method=='POST':
        data=JSONParser().parse(request)
        deviceid=data.get("deviceid")
        content=data.get("content")
        doc={"deviceid":deviceid,"contentlist":[{"content":content,"createtime":datetime.datetime.now()}]}
        if(collection.find({"deviceid":deviceid}).count()>0):
            collection.update({"deviceid":deviceid},{"$addToSet":{"contentlist":{"content":content,"createtime":datetime.datetime.now()}}})
            return  JsonResponse({"target":"succcess"},status=200)
        collection.insert(doc)
    return JsonResponse({"target":"success"},status=201)



@csrf_exempt
def UserInfo(request):
    collection=db.UserInfo
    if request.method=="POST":
        data=JSONParser().parse(request)
        head=data.get("head")
        nikename=data.get("nikename")
        deviceid=data.get("deviceid")
        doc={'deviceid':deviceid,"head":head,"nikename":nikename,"DBsize":"1024M",'Praise':0}
        collection.insert(doc)
        return  JsonResponse({"target":"success"})
    elif request.method=="PUT":
        data=JSONParser().parse(request)
        deviceid=data.get("deviceid")
        nikename=data.get("nikename")
        Praise=data.get("Praise")
        head=data.get("head")
        if nikename!=None:
            collection.update({'deviceid':deviceid},{"nikename":nikename})
        elif Praise!=None:
            collection.update({'deviceid':deviceid},{'Praise':Praise},{"DBsize":"2048M"})
        elif head!=None:
            collection.update({'deviceid':deviceid},{"head":head})
        return  JsonResponse({"target":"success"})







feeddata="xx"
def feedback(request):
    collection=db.Userfeedback
    global feeddata
    collection.find()
    for d in collection.find():
        feeddata=list(collection.find())
    return render(request,"feedback.html",{"data":feeddata})

    # elif request.method =='DELETE':
    #     data=JSONParser().parse(request)
    #     id=data.get('id')
    #     print id
    #     collection.remove({"_id":ObjectId(id)})
    #     if(collection.find({"_id":ObjectId(id)}).count()>0):
    #         return JsonResponse({"target":"romove failed"})
    #     return JsonResponse({"target":"remove success"})
    # return  JsonResponse({"OK":1})
# @csrf_exempt
# def snippet_detail(request,id):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = list(collection.find({"id":id}))
#     except snippet.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#
#         return JsonResponse(json.dumps(snippet,default=json_util.default),safe=False)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         print "++++++++"
#         print data
#         id=data.get("id")
#         name=collection.find({"_id":ObjectId(id)})
#         data1=json.dumps(name.next(),default=json_util.default)
#         #_id=data1.get("_id")
#         #print str(_id)
#         #print json.dumps({""})
#
#         return JsonResponse(data1,safe=False)
#
#     elif request.method == 'DELETE':
#         data=JSONParser.parse(request)
#         info=data.get('id')
#         collection.remove({"id":info})
#         return HttpResponse(status=204)