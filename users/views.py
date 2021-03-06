from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.views.generic import View
from .modelForms import UserForm, CoderForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

class UserFormView(View):
    form_class1 = UserForm
    form_class2 = CoderForm
    template_name = 'users/reg_form.html'

    def get(self, request):
        form1 = self.form_class1(None)
        form2 = self.form_class2(None)
        return render(request, self.template_name,
                      {'form1' : form1, 'form2' : form2})

    def post(self, request):
        form1=self.form_class1(request.POST)
        form2 = self.form_class2(request.POST)

        if form1.is_valid():
            user = form1.save(commit=False)
            coder = form2.save(commit=False)
            username = form1.cleaned_data['username']
            password = form1.cleaned_data['password']
            user.set_password(password)
            user.save()
            coder.user = user
            coder.save()

            user = authenticate(username = username,password = password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('/')

        return render(request, self.template_name, {'form1': form1, 'form2': form2})

class MainPageView(View):
    template_name = 'main_page.html'
    def get(self, request):
        user = None
        if request.user.is_authenticated():
            user_id =request.user.id
            user = User.objects.get(id=user_id)
        return render(request, self.template_name, {'user': user})

class LoginPageView(View):

    template_name = 'users/login_page.html'

    def get(self,request):
        return render(request,self.template_name)

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                return redirect('/')

        return render(request,self.template_name)

class LogoutPageView(View):

    template_name = 'main_page.html'

    def post(self, request):
        logout(request)
        return redirect('/')
