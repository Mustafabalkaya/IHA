from .models import CustomUser, UAV, Rent
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from django.db.models import Sum, ExpressionWrapper, F
from django.db.models import Count



def get_uavs(request):
    uavs = UAV.objects.all()

    # Arama
    search_value = request.POST.get('search[value]', None)
    if search_value:
        uavs = uavs.filter(
            Q(uav_name__icontains=search_value) |
            Q(uav_brand__icontains=search_value) |
            Q(uav_model__icontains=search_value) |
            Q(uav_weight__icontains=search_value) |
            Q(uav_range__icontains=search_value) |
            Q(uav_quantity__icontains=search_value) |
            Q(daily_rental_fee__icontains=search_value)
        )

    # Sıralama
    uavs = uavs.order_by('id')

    # Sayfalama
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))
    paginator = Paginator(uavs, length)
    page_number = start // length + 1
    uavs = paginator.page(page_number)

    data = []
    for uav in uavs:
        data.append({
            'id': uav.id,
            'uav_name': uav.uav_name,
            'uav_brand': uav.uav_brand,
            'uav_model': uav.uav_model,
            'uav_weight': str(uav.uav_weight),
            'uav_range': str(uav.uav_range),
            'uav_quantity': uav.uav_quantity,
            'daily_rental_fee': str(uav.daily_rental_fee),
        })
    return JsonResponse({
        'draw': int(request.POST.get('draw', 1)),
        'recordsTotal': UAV.objects.count(),
        'recordsFiltered': paginator.count,
        'data': data
    })

def getUavDetails(request):
    if request.method == 'GET':
        uav_id = request.GET.get('uav_id') # URL'den UAV ID'sini al
        try:
            uav = UAV.objects.get(pk=uav_id) # Belirli bir UAV kaydını al
            # UAV kaydının detaylarını bir sözlük olarak oluştur
            uav_data = {
                'uav_name': uav.uav_name,
                'uav_brand': uav.uav_brand,
                'uav_model': uav.uav_model,
                'uav_weight': uav.uav_weight,
                'uav_range': uav.uav_range,
                'uav_quantity': uav.uav_quantity,
                'daily_rental_fee': uav.daily_rental_fee,
            }
            return JsonResponse({'uav_data': uav_data}) # JSON formatında verileri döndür
        except UAV.DoesNotExist:
            return JsonResponse({'error': 'UAV not found'}, status=404) # UAV bulunamazsa 404 hatası döndür
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_users(request):
    users = CustomUser.objects.all()

    # Arama
    search_value = request.POST.get('search[value]', None)
    if search_value:
        users = users.filter(
            Q(first_name__icontains=search_value) |
            Q(last_name__icontains=search_value) |
            Q(username__icontains=search_value) |
            Q(phone__icontains=search_value)
        )

    # Sıralama
    users = users.order_by('id')

    # Sayfalama
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))
    paginator = Paginator(users, length)
    page_number = start // length + 1
    users = paginator.page(page_number)

    data = []
    for user in users:
        if user.is_staff == True:
            userRole = "Yönetici"
        else:
            userRole = "Kullanıcı"
        data.append({
            'id': user.id,
            'user_name': user.first_name + ' ' + user.last_name,
            'user_email': user.username,
            'user_phone': user.phone,
            'user_date_joined': timezone.localtime(user.date_joined).strftime("%d-%m-%Y"),
            'user_last_login': timezone.localtime(user.last_login).strftime("%d-%m-%Y"),
            'user_role': userRole,
        })
    return JsonResponse({
        'draw': int(request.POST.get('draw', 1)),
        'recordsTotal': CustomUser.objects.count(),
        'recordsFiltered': paginator.count,
        'data': data
    })

def get_uav_brands(request):
    brands = UAV.objects.values_list('uav_brand', flat=True).distinct()
    return JsonResponse({'brands': list(brands)})

def get_uav_models(request):
    if request.method == 'POST':
        brand = request.POST.get('brand')
        models = UAV.objects.filter(uav_brand=brand).values_list('uav_model', flat=True).distinct()
        return JsonResponse({'models': list(models)})
    return JsonResponse({'error': 'GET request is not allowed'})

def search_uavs(request):
    if request.method == 'POST':
        selected_brand = request.POST.get('brand')
        selected_model = request.POST.get('model')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Rent tablosundan kıyaslama yap
        # Belirli bir marka ve modele ait, belirli bir tarih aralığında kiralanmış olan toplam miktarı bul
        rented_quantity = Rent.objects.filter(uav__uav_brand=selected_brand,
                                              uav__uav_model=selected_model,
                                              date_start__lte=end_date,
                                              date_end__gte=start_date).count()

        # Belirli bir marka ve modele ait toplam miktarı bul
        uav_quantity = UAV.objects.filter(uav_brand=selected_brand, uav_model=selected_model).values_list(
            'uav_quantity', flat=True).first() or 0

        # Kiralanmış miktar, toplam miktarı aşmıyorsa, bu UAV'yi mevcut olarak kabul et
        if rented_quantity < uav_quantity:
            uavs = UAV.objects.filter(uav_brand=selected_brand, uav_model=selected_model)
            uav_data = [{'id': uav.id,
                     'uav_name': uav.uav_name,
                     'uav_brand': uav.uav_brand,
                     'uav_model': uav.uav_model,
                     'uav_weight': uav.uav_weight,
                     'uav_range': uav.uav_range,
                     'uav_quantity': uav.uav_quantity,
                     'daily_rental_fee': uav.daily_rental_fee,
                     'total_fee': calculate_total_fee(uav.daily_rental_fee, start_date, end_date)} for uav in uavs]
            return JsonResponse({'uavs': uav_data})
        else:
            return JsonResponse({'error': 'Seçilen tarihler arasında kiralanmış UAV bulunmaktadır.'}, status=400)
    return JsonResponse({'error': 'Bad request'}, status=400)


def calculate_total_fee(daily_fee, start_date, end_date):
    # Tarih formatını dönüştür
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Kiralama süresini hesapla
    rental_days = (end_date - start_date).days + 1

    # Toplam ücreti hesapla (günlük ücret x kiralama günü)
    total_fee = daily_fee * rental_days

    return total_fee

def rent_uav(request):
    if request.method == 'POST':
        uav_id = request.POST.get('uav_id')
        date_start = request.POST.get('date_start')
        date_end = request.POST.get('date_end')
        uav = UAV.objects.get(pk=uav_id)
        totalFee = calculate_total_fee(uav.daily_rental_fee, date_start, date_end)
        try:
            Rent.objects.create(user=request.user, uav_id=uav_id, date_start=date_start, date_end=date_end, total_fee=totalFee)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'error': 'Bad request'}, status=400)

def get_rents(request):
    rents = Rent.objects.filter(user_id=request.user)

    # Arama
    search_value = request.POST.get('search[value]', None)
    if search_value:
        rents = rents.filter(
            Q(date_start__icontains=search_value) |
            Q(date_end__icontains=search_value)
        )

    # Sıralama
    rents = rents.order_by('id')

    # Sayfalama
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))
    paginator = Paginator(rents, length)
    page_number = start // length + 1
    rents = paginator.page(page_number)

    data = []
    for rent in rents:
        uav = UAV.objects.get(pk=rent.uav_id)
        totalFee = calculate_total_fee(uav.daily_rental_fee, rent.date_start, rent.date_end)
        data.append({
            'id': rent.id,
            'uav_brand': uav.uav_brand,
            'uav_model': uav.uav_model,
            'uav_weight': uav.uav_weight,
            'uav_range': uav.uav_range,
            'rent_dates': rent.date_start.strftime("%d-%m-%Y") + ' / ' + rent.date_end.strftime("%d-%m-%Y"),
            'rent_total_fee': totalFee,
        })
    return JsonResponse({
        'draw': int(request.POST.get('draw', 1)),
        'recordsTotal': Rent.objects.filter(user_id=request.user).count(),
        'recordsFiltered': paginator.count,
        'data': data
    })

def get_all_rents(request):
    rents = Rent.objects.all()

    # Arama
    search_value = request.POST.get('search[value]', None)
    if search_value:
        rents = rents.filter(
            Q(date_start__icontains=search_value) |
            Q(date_end__icontains=search_value)
        )

    # Sıralama
    rents = rents.order_by('id')

    # Sayfalama
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))
    paginator = Paginator(rents, length)
    page_number = start // length + 1
    rents = paginator.page(page_number)

    data = []
    for rent in rents:
        uav = UAV.objects.get(pk=rent.uav_id)
        user = CustomUser.objects.get(pk=rent.user_id)
        totalFee = calculate_total_fee(uav.daily_rental_fee, rent.date_start, rent.date_end)
        data.append({
            'id': rent.id,
            'user_name': user.first_name + ' ' + user.last_name,
            'uav_brand': uav.uav_brand,
            'uav_model': uav.uav_model,
            'rent_dates': rent.date_start.strftime("%d-%m-%Y") + ' / ' + rent.date_end.strftime("%d-%m-%Y"),
            'rent_total_fee': totalFee,
        })
    return JsonResponse({
        'draw': int(request.POST.get('draw', 1)),
        'recordsTotal': Rent.objects.count(),
        'recordsFiltered': paginator.count,
        'data': data
    })
