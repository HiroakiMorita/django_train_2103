from django.contrib.admin.options import InlineModelAdmin
from django.core import paginator
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from .models import Friend, Message
from .forms import FriendForm, MessageForm
# from .forms import HelloForm
from django.db.models import QuerySet
from django.views.generic import ListView
from django.views.generic import DetailView
from .forms import FindForm
from django.db.models import Q
from django.db.models import Count, Sum, Avg, Min, Max # aggregateメソッドで使う
from .forms import CheckForm
from django.core.paginator import Paginator



class FriendList(ListView):
    model = Friend

class FriendDetail(DetailView):
    model = Friend


def index(request, num=1):
    data = Friend.objects.all()
    page = Paginator(data, 3)
    # re1 = Friend.objects.aggregate(Count('age'))
    # re2 = Friend.objects.aggregate(Sum('age'))
    # re3 = Friend.objects.aggregate(Avg('age'))
    # re4 = Friend.objects.aggregate(Min('age'))
    # re5 = Friend.objects.aggregate(Max('age'))
    # msg = 'count:' + str(re1['age__count']) \
    #             + 'Sum:' + str(re2['age__sum']) \
    #             + 'Average:' + str(re3['age__avg']) \
    #             + 'Min:' + str(re4['age__min']) \
    #             + 'Max:' + str(re5['age__max']) \
    # data = Friend.objects.all().order_by('age').reverse() # 年齢逆順に表示
    # data = Friend.objects.all().order_by('age') # 年齢順に表示
    params = {
        'title': 'Hello',
        'message': '',
        'data': page.get_page(num),
    }
    return render(request, 'hello/index.html', params)


# create model
def create(request):
    if (request.method == 'POST'):
        obj = Friend()
        friend = FriendForm(request.POST, instance=obj)
        friend.save()
        return redirect(to='/hello')
    params = {
        'title': 'Hello',
        'form': FriendForm(),
    }
    return render(request, 'hello/create.html', params)

# edit
def edit(request, num):
    obj = Friend.objects.get(id=num)
    if (request.method == 'POST'):
        friend = FriendForm(request.POST, instance=obj)
        friend.save()
        return redirect(to='/hello')
    params = {
        'title': 'Hello',
        'id': num,
        'form': FriendForm(instance=obj),
    }
    return render(request, 'hello/edit.html', params)

# delete
def delete(request, num):
    friend = Friend.objects.get(id=num)
    if (request.method == 'POST'):
        friend.delete()
        return redirect(to='/hello')
    params = {
        'title': 'Hello',
        'id': num,
        'obj': friend,
    }
    return render(request, 'hello/delete.html', params)


def find(request):
    if (request.method == 'POST'):
        msg = request.POST['find']
        form = FindForm(request.POST)
        sql = 'select * from hello_friend'
        if (msg != ''):
            sql += ' where ' + msg
        data = Friend.objects.raw(sql)
        msg = sql
    else:
        msg = 'search words...'
        form = FindForm()
        data = Friend.objects.all()
    params = {
        'title': 'Hello',
        'message': msg,
        'form': form,
        'data': data,
    }
    return render(request, 'hello/find.html', params)


def check(request):
    params = {
        'title': 'Hello',
        'message': 'check validation',
        'form': FriendForm(),
    }
    if (request.method == 'POST'):
        obj = Friend()
        form = FriendForm(request.POST, instance=obj)
        params['form'] = form
        if (form.is_valid()):
            params['message'] = 'OK!'
        else:
            params['message'] = 'no good.'
    return render(request, 'hello/check.html', params)


def message(request, page=1):
    if (request.method == 'POST'):
        obj = Message()
        form = MessageForm(request.POST, instance=obj)
        form.save()
    data = Message.objects.all().reverse()
    paginator = Paginator(data, 5)
    params = {
        'title': 'Message',
        'form': MessageForm(),
        'data': paginator.get_page(page),
    }
    return render(request, 'hello/message.html', params)



        
        # data = Friend.objects.all()[int(list[0]):int(list[1])] # 1番目と2番目入力
        # data = Friend.objects.filter(name__in=list) # 検索に含むもの全て表示
        # data = Friend.objects.filter(Q(name__contains=find)|Q(mail__contains=find)) # OR検索、名前かメールどちらか含む検索
        # data = Friend.objects.filter(age__gte=val[0], age__lte=val[1]) # 例：何歳以上〜何歳未満
    #     msg = 'search result: ' + str(data.count()) # 検索数表示



        # name = request.POST['name']
        # mail = request.POST['mail']
        # gender = 'gender' in request.POST
        # age = int(request.POST['age'])
        # birth = request.POST['birthday']
        # friend = Friend(name=name, mail=mail, gender=gender, \
        #       age=age, birthday=birth)
        # friend.save()
        # return redirect(to='/hello')



# def __new_str__(self):
#     result = ''
#     for item in self:
#         result += '<tr>'
#         for k in item:
#             result += '<td>' + str(k) + '=' + str(item[k]) + '</td>'
#         result += '</tr>'
#     return result

# QuerySet.__str__ = __new_str__


# class HelloView(TemplateView):
    
#     def __init__(self):
#         self.params = {
#             'title': 'Hello',
#             'form': HelloForm(),
#             'result': None
#         }
    
#     def get(self, request):
#         return render(request, 'hello/index.html', self.params)

#     def post(self, request):
#         ch = request.POST.getlist('choice')
#         result = '<ol class="list-group"><b>selected:</b>'
#         for item in ch:
#             result += '<li class="list-group-item">' + item + '</li>'
#         result += '</ol>'
#         self.params['result'] = result
#         self.params['form'] = HelloForm(request.POST)
#         return render(request, 'hello/index.html', self.params)


    # def post(self, request):
    #     ch = request.POST.getlist('choice')
    #     self.params['result'] = 'selected: "' + str(ch) + '".'  # エラーが出てchをstrにする必要があった
    #     self.params['form'] = HelloForm(request.POST)
    #     return render(request, 'hello/index.html', self.params)



    # def post(self, request):
    #     ch = request.POST.get('choice')
    #     self.params['result'] = 'selected: "' + str(ch) + '".'  # エラーが出てchをstrにする必要があった
    #     self.params['form'] = HelloForm(request.POST)
    #     return render(request, 'hello/index.html', self.params)

        # chk = request.POST['check']
        # self.params['result'] = 'you selected: " ' + chk + ' ".'
        # self.params['form'] = HelloForm(request.POST)
        # return render(request, 'hello/index.html', self.params)

        # if ('check' in request.POST):
        #     self.params['result'] = 'Checked!!'
        # else:
        #     self.params['result'] = 'not checked...'
        # self.params['form'] = HelloForm(request.POST)
        # return render(request, 'hello/index.html', self.params)



        # msg = 'あなたは、<b>' + request.POST['name'] + \
        #     '(' + request.POST['age'] + \
        #     ') </b>さんです。 <br>メールアドレスは<b>' + request.POST['mail'] + \
        #     '</b> ですね。 '
        # self.params['message'] = msg
        # self.params['form'] = HelloForm(request.POST)
        # return render(request, 'hello/index.html', self.params)


# def index(request):
#     params = {
#         'title': 'Hello',
#         'msg': 'your data:',
#         'form': HelloForm()
#     }
#     if (request.method == 'POST'):
#         params['message'] = '名前:' + request.POST['name'] + \
#             '<br>メール:' + request.POST['mail'] + \
#             '<br>年齢:' + request.POST['age']
#         params['form'] = HelloForm(request.POST)
#     return render(request, 'hello/index.html', params)

# def form(request):
#     msg = request.POST['msg']
#     params = {
#         'title': 'formページ',
#         'msg': 'こんにちは' + msg + 'さん。',
#     }
#     return render(request, 'hello/index.html', params)