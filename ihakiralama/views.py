from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, UAV, Rent
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.utils import timezone


#View Functions:

#Index & Global:
def index(request):
    context = {
        'title': 'IHA Kiralama - Ana Sayfa',
    }
    return render(request, 'index.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')  # Kullanıcı giriş yapmışsa ana sayfaya yönlendir
    else:
        if request.method == 'POST':
            email = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                error_message = 'E-posta veya parola hatalı!'
                return render(request, 'account/login.html', {'error_message': error_message})
        else:
            return render(request, 'account/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')  # Kullanıcı giriş yapmışsa ana sayfaya yönlendir
    else:
        if request.method == 'POST':
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            email = request.POST.get('username')
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            password_retype = request.POST.get('password_retype')

            # Parolaların eşleşip eşleşmediğini kontrol et
            if password != password_retype:
                error_message = 'Parolalar eşleşmiyor!'
                return render(request, 'account/register.html', {'error_message': error_message})

            # E-posta veya telefon numarasının kullanımda olup olmadığını kontrol et
            if CustomUser.objects.filter(username=email).exists() or CustomUser.objects.filter(phone=phone).exists():
                error_message = 'Bu e-posta veya telefon numarası zaten kullanımda!'
                return render(request, 'account/register.html', {'error_message': error_message})

            # Kullanıcıyı oluştur ve kaydet
            user = CustomUser.objects.create_user(username=email, password=password)
            user.first_name = name
            user.last_name = surname
            user.phone = phone
            user.email = email
            user.save()

            # Kullanıcı kaydı başarılı, başarılı mesajını göster ve /login sayfasına yönlendir
            messages.success(request, 'Üyeliğiniz başarıyla kaydedildi! Lütfen giriş yapın.')
            return redirect('/login')

        else:
            return render(request, 'account/register.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')

#Admin:
@login_required(login_url='/login')  # Oturum açmamış kullanıcıları ana sayfaya yönlendir
def createUav(request):
    if request.method == 'POST':
        uav_name = request.POST.get('uav_name')
        uav_brand = request.POST.get('uav_brand')
        uav_model = request.POST.get('uav_model')
        uav_weight = request.POST.get('uav_weight')
        uav_range = request.POST.get('uav_range')
        uav_quantity = request.POST.get('uav_quantity')
        daily_rental_fee = request.POST.get('daily_rental_fee')

        # IHA'yı oluştur ve kaydet
        iha = UAV.objects.create(uav_name= uav_name,
                                 uav_brand=uav_brand,
                                 uav_model=uav_model,
                                 uav_weight=uav_weight,
                                 uav_range=uav_range,
                                 uav_quantity=uav_quantity,
                                 daily_rental_fee=daily_rental_fee)
        iha.save()

        # IHA kaydı başarılı, başarılı mesajını göster
        messages.success(request, 'IHA başarıyla kaydedildi!')
        return render(request, 'account/admin/create-uav.html')
    else:
        return render(request, 'account/admin/create-uav.html')

@login_required(login_url='/login')  # Oturum açmamış kullanıcıları ana sayfaya yönlendir
def editUav(request, uav_id):
    try:
        uav = UAV.objects.get(id=uav_id)
    except UAV.DoesNotExist:
        return render(request, 'error.html', {'error_message': 'Belirtilen UAV kaydı bulunamadı'})

    return render(request, 'account/admin/edit-uav.html', {'uav': uav})

@login_required(login_url='/login')  # Oturum açmamış kullanıcıları ana sayfaya yönlendir
def listUavs(request):
    return render(request, 'account/admin/list-uavs.html')

@login_required(login_url='/login')  # Oturum açmamış kullanıcıları ana sayfaya yönlendir
def createUser(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('username')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password_retype = request.POST.get('password_retype')
        is_staff = request.POST.get('is_staff')

        if is_staff == "True":
            isStaff = True
        else:
            isStaff = False

        # Parolaların eşleşip eşleşmediğini kontrol et
        if password != password_retype:
            error_message = 'Parolalar eşleşmiyor!'
            return render(request, 'account/admin/create-user.html', {'error_message': error_message})

        # E-posta veya telefon numarasının kullanımda olup olmadığını kontrol et
        if CustomUser.objects.filter(username=email).exists() or CustomUser.objects.filter(phone=phone).exists():
            error_message = 'Bu e-posta veya telefon numarası zaten kullanımda!'
            return render(request, 'account/admin/create-user.html', {'error_message': error_message})

        # Kullanıcıyı oluştur ve kaydet
        user = CustomUser.objects.create_user(username=email, password=password)
        user.first_name = name
        user.last_name = surname
        user.phone = phone
        user.email = email
        user.is_staff = isStaff
        user.save()

        # Kullanıcı kaydı başarılı, başarılı mesajını göster
        messages.success(request, 'Üyelik başarıyla oluşturuldu!')
        return render(request, 'account/admin/create-user.html')
    else:
        return render(request, 'account/admin/create-user.html')

@login_required(login_url='/login')  # Oturum açmamış kullanıcıları ana sayfaya yönlendir
def editUser(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return render(request, 'error.html', {'error_message': 'Belirtilen Kullanıcı kaydı bulunamadı'})

    return render(request, 'account/admin/edit-user.html', {'user': user})
@login_required(login_url='/login')  # Oturum açmamış kullanıcıları ana sayfaya yönlendir
def listUsers(request):
    return render(request, 'account/admin/list-users.html')

@login_required(login_url='/login')  # Oturum açmamış kullanıcıları ana sayfaya yönlendir
def rents(request):
    return render(request, 'account/admin/rents.html')

#User:
@login_required(login_url='/login')  # Oturum açmamış kullanıcıları ana sayfaya yönlendir
def rentaUav(request):
    return render(request, 'account/user/rent-a-uav.html')

@login_required(login_url='/login')  # Oturum açmamış kullanıcıları ana sayfaya yönlendir
def myRents(request):
    return render(request, 'account/user/my-rents.html')


#DB Functions:
def deleteUav(request, uav_id):
    uav = UAV.objects.get(pk=uav_id)
    uav.delete()
    return HttpResponse(f'UAV {uav.uav_name} deleted successfully!')
def saveUav(request, uav_id):
    if request.method == 'POST':
        # Formdan gelen verileri al
        uav_name = request.POST.get('uav_name')
        uav_brand = request.POST.get('uav_brand')
        uav_model = request.POST.get('uav_model')
        uav_weight = request.POST.get('uav_weight')
        uav_range = request.POST.get('uav_range')
        uav_quantity = request.POST.get('uav_quantity')
        daily_rental_fee = request.POST.get('daily_rental_fee')

        try:
            # Veritabanında ilgili UAV kaydını bul
            uav = UAV.objects.get(id=uav_id)

            # Bulunan kaydın verilerini güncelle
            uav.uav_name = uav_name
            uav.uav_brand = uav_brand
            uav.uav_model = uav_model
            uav.uav_weight = uav_weight
            uav.uav_range = uav_range
            uav.uav_quantity = uav_quantity
            uav.daily_rental_fee = daily_rental_fee

            # Kaydı veritabanına kaydet
            uav.save()

            # Başarılı bir şekilde güncellendiğine dair mesaj göster
            messages.success(request, 'UAV başarıyla güncellendi.')

            # Düzenleme sayfasına yönlendir
            return redirect('edit-uav', uav_id=uav_id)
        except UAV.DoesNotExist:
            # Eğer verilen ID'ye sahip bir UAV kaydı bulunamazsa hata mesajı göster
            messages.error(request, 'Belirtilen UAV kaydı bulunamadı.')

    # Kaydetme işlemi GET isteğiyle yapılmışsa veya hata durumunda, düzenleme sayfasına geri dön
    return redirect('edit-uav', uav_id=uav_id)

def deleteUser(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    user.delete()
    return HttpResponse(f'USER {user.first_name} deleted successfully!')

def saveUser(request, user_id):
    if request.method == 'POST':
        # Formdan gelen verileri al
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('username')
        phone = request.POST.get('phone')
        is_staff = request.POST.get('is_staff')

        password = request.POST.get('password')
        password_retype = request.POST.get('password_retype')

        if is_staff == "True":
            isStaff = True
        else:
            isStaff = False

        try:
            # Veritabanında ilgili Kullanıcı kaydını bul
            user = CustomUser.objects.get(id=user_id)

            # Bulunan kaydın verilerini güncelle
            user.first_name = name
            user.last_name = surname
            user.email = email
            user.phone = phone
            user.is_staff = isStaff

            if password != '' and password_retype != '':
                # Parolaların eşleşip eşleşmediğini kontrol et
                if password != password_retype:
                    error_message = 'Parolalar eşleşmiyor!'
                    return redirect('edit-user', user_id=user_id)
                else:
                    user.password = password

            # Kaydı veritabanına kaydet
            user.save()

            # Başarılı bir şekilde güncellendiğine dair mesaj göster
            messages.success(request, 'Kullanıcı başarıyla güncellendi.')

            # Düzenleme sayfasına yönlendir
            return redirect('edit-user', user_id=user_id)
        except UAV.DoesNotExist:
            # Eğer verilen ID'ye sahip bir UAV kaydı bulunamazsa hata mesajı göster
            messages.error(request, 'Belirtilen Kullanıcı kaydı bulunamadı.')

    # Kaydetme işlemi GET isteğiyle yapılmışsa veya hata durumunda, düzenleme sayfasına geri dön
    return redirect('edit-user', user_id=user_id)

def deleteRent(request, rent_id):
    rent = Rent.objects.get(pk=rent_id)
    rent.delete()
    return HttpResponse(f'USER {rent.id} deleted successfully!')
