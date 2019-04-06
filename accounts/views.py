from django.shortcuts import render, redirect, get_object_or_404
from .forms import Register, UserProfileForm
from django.contrib.auth import authenticate, login
from .models import UserProfile
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def UserRegister(request):

    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate (username = username, password = password)
            login(request, user)
            return redirect('accounts:user_edit_profile')
    else:
        form = Register()
    context = {'form':form}

    return render(request, 'accounts/register.html', context)


def edituserProfile(request):
    user = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save(commit = False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.address = form.cleaned_data['address']
            user.additional_info = form.cleaned_data['additional_info']
            user.phone = form.cleaned_data['phone']
            user.phone2 = form.cleaned_data['phone2']
            user.city = form.cleaned_data['city']
            user.save()
            form.save()
            return redirect('shop:product_list')
    else:
        form = UserProfileForm(instance=user)
    context = {'form':form}
    return render(request, 'accounts/profile.html', context)

@login_required
def newUserProfile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, initial={'user':request.user})
        if form.is_valid():
            form.save()
            # print(request.user)
            # user.user = request.user
            # user.first_name = form.cleaned_data['first_name']
            # user.last_name = form.cleaned_data['last_name']
            # user.address = form.cleaned_data['address']
            # user.additional_info = form.cleaned_data['additional_info']
            # user.phone = form.cleaned_data['phone']
            # user.phone2 = form.cleaned_data['phone2']
            # user.city = form.cleaned_data['city']
            # user.save()
            # form.save()
            return redirect('shop:product_list')
    else:
        form = UserProfileForm(initial={'user':request.user})
    context = {'form':form}
    return render(request, 'accounts/profile.html', context)


# class UserProfileListView(ListView):
#     model = UserProfile
#     template_name = 
#     context_obj_name = 'profile'

def userProfile(request):
    profile = UserProfile.objects.all()
    context = {'profile':profile}
    return render(request, "accounts/user_profile_list.html", context)


@login_required
def defaultAddress(request, profile_id):
    user_profile = UserProfile.objects.filter(user=request.user).filter(default_address=True).first()
    new_default = get_object_or_404(UserProfile, id=profile_id)
    user_profile.removeDefault()
    new_default.defaultAddress()
    return redirect('account:profile_list')

    
