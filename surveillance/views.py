from django.shortcuts import render,redirect

from django.views import View



#TIPS:LoginRequiredMixinはリクエストしたユーザーがログインしているかどうかをチェックすることができる。
#TIPS:もし、ログインしていない場合、ログインページへリダイレクトする。使い方はビュークラスの第一引数として指定する。
from django.contrib.auth.mixins import LoginRequiredMixin



from .models import Information
from .forms import InformationForm


#TIPS:これでSurveillanceViewはログインしていないユーザーは全てのメソッドでトップページへリダイレクトされる。
class SurveillanceView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):

        informations  = Information.objects.all()
        context = { "informations":informations }    
        return render(request,"surveillance/index.html",context)

    def post(self, request, *args, **kwargs):

        """
        posted  = Information( url = request.POST["url"],email = request.POST["email"] )
        posted.save()
        """
        
        #forms.pyを使ったほうが、フィールドが増えてもビューの書き換えは発生しないし、バリデーション(入力値のチェック)までできる
        form    = InformationForm(request.POST)

        if form.is_valid():
            print("バリデーションOK")
            form.save()

        else:
            print("バリデーションNG")

        return redirect("surveillance:index")

index   = SurveillanceView.as_view()


#レコードを削除する専用のビュー
class SurveillanceDeleteView(LoginRequiredMixin,View):

    def post(self, request, pk, *args, **kwargs):

        #主キーが合致するものを検索、対象を削除する。
        #TIPS:urls.pyにて、入力値のチェックは行っているのであえてforms.pyにてクラスを定義してバリデーションをする必要はない。
        informations  = Information.objects.filter(id=pk)

        #レコードが存在する場合、削除する。
        if informations:
            informations.delete()
        else:
            print("指定されたデータがありません")
        
        return redirect("surveillance:index")

delete  = SurveillanceDeleteView.as_view()

