from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse


# Create your views here.

class DefaultView(TemplateView):

    def get(self, request):
        return render(request, 'dummy.html')

    @method_decorator(csrf_exempt)
    def post(self, request):
        query = request.POST['query']
        originalQuery = query
        queryList = query.split()
        queryList = [q for q in queryList if query != '']
        # print(queryList)
        fromIndex = queryList.index('FROM')
        innerIndex = queryList.index('INNER')
        joinIndex = queryList.index('JOIN')
        onIndex = queryList.index('ON')
        whereIndex = queryList.index('WHERE')
        # print(fromIndex, innerIndex, joinIndex, onIndex)
        t1, t1_alias = queryList[fromIndex + 1:innerIndex]
        t2, t2_alias = queryList[joinIndex + 1:onIndex]
        c1 = queryList[onIndex + 1:whereIndex]
        c2 = queryList[whereIndex + 1:]
        print(t1)
        print(t2)
        print(c1)
        print(c2)
        return HttpResponse('Success')
