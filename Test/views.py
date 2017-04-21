from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser


import json
from bson import json_util,ObjectId
import pymongo

try:
    conn=pymongo.MongoClient()
    print "success"
except pymongo.errors.ConnectionFailure,e:
    print "error %s"%e


db=conn['Mmcalculator']
collection=db.my_collection

@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """

    if request.method=='GET':
        #id=data.get('id')
        return JsonResponse({"ok": 1})
    elif request.method == 'POST':
            data = JSONParser().parse(request)
            #print data
            user=data.get("usr")
            photourl=data.get("photourl")
            if photourl==None:
                print "none"
                data=list(collection.find({"usr":user}))
                print data
                return JsonResponse(json.dumps(data,default=json_util.default),safe=False,status=200)

            else:
                data = {"usr":user,"photourl":[{"url":photourl,"target":0}]}
                #abc = data.get("name")
                #print abc
                if (collection.find({"usr": user}).count()> 0):
                    if(collection.update({"usr":user},{"$addToSet":{"photourl":{"url":photourl,"target":0}}})):
                        return JsonResponse({"target":"sucess"})
                    else:
                        return JsonResponse({"target": "failed"}, status=400)
                #print data
                collection.insert(data)
                #s=collection.find({"photourl":photourl}).next()
                #if (collection.find({"photourl": {"url":photourl}}).count()== 0):

            return JsonResponse({"target": "success"},status=201)
            # return JsonResponse(json.dumps(data,default=json_util.default),safe=False,status=201)

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