from rest_framework.response import Response
from rest_framework.decorators import api_view
import subprocess
from django.http import JsonResponse
from .models import PingResult
import ipaddress
from subnetPing.tasks import process_subnet_ips
from subnetPing.tasks import process_subnet_ips_caching
from django.core.cache import cache
# from subnetPing import tasks

@api_view(['GET'])
def hello_world(request):
    print("Logging test")
    return Response({"message": "Hello World!"})


@cache
@api_view(['POST'])
def get_subnet_ips(request):
    print("geldi mi1")
    try:
        ip_address = request.data.get('ip_address')
        subnet_mask = request.data.get('subnet_mask')
        print("geldi mi")
        network = ipaddress.ip_network(f"{ip_address}/{subnet_mask}", strict=False)

        response_result_array = []
        for ip in network.hosts():
            ping_result = ping_and_log(str(ip))
            print ("tttttttttt")
            response_result_object = {'Subnet Ip': str(ip), 'Ping Result': ping_result.get('is_active', False)}
            update_ip_status(str(ip), ping_result.get('is_active', False))
            response_result_array.append(response_result_object)

        return Response({'Response Result': response_result_array})

        # Celery görevini başlatın ve parametreleri ile birlikte gönderelim


        # Görev başarıyla başlatıldı, sonucunu beklemek istersek
        # result = result.get()

        #return Response({'message': 'Görev başlatıldı. Sonucu bekleyin...'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

def validate_ip_address(ip_address):
    # Girilen IP adresini kontrol edin
    try:
        ip = ipaddress.ip_address(ip_address)
        return True
    except ValueError:
       return False

def get_ip_version(ip_address):
    try:
        ip = ipaddress.ip_address(ip_address)
        if isinstance(ip, ipaddress.IPv4Address):
            return "IPv4"
        elif isinstance(ip, ipaddress.IPv6Address):
            return "IPv6"
        else:
            return "Geçersiz IP"
    except ValueError:
        return "Geçersiz IP"


def is_largest_subnet_mask_v6(ip_address_str, subnet_mask_str):
    print("yyy")
    try:
        print("3333")
        print(ip_address_str)
        print(type(subnet_mask_str))
        # Verilen IPv6 adresini ve subnet maskesini oluşturun
        ip = ipaddress.IPv6Network(f"{ip_address_str}{'/' + subnet_mask_str}", strict=False)

        print("--777-ip--")
        print(ip)
        # Oluşturulan subnet maskesinin uzunluğunu alın
        subnet_mask_length = ip.prefixlen
        if subnet_mask_length > 64:
            return False
        else:
            # En büyük IPv6 subnet maskesi 64 ise True döndürün
            return subnet_mask_length <= 64
    except Exception as e:
        print(str(e))
        return False
    # except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
    #
    #     # Geçersiz IPv6 adresi veya subnet maskesi verilmişse False döndürün
    #     return False


def is_largest_subnet_mask_v4(ip_address_str, subnet_mask_str):
    try:
        # Verilen IPv4 adresini ve subnet maskesini oluşturun
        ip = ipaddress.IPv4Network(f"{ip_address_str}/{subnet_mask_str}", strict=False)

        # Oluşturulan subnet maskesinin uzunluğunu alın
        subnet_mask_length = ip.prefixlen
        if subnet_mask_length > 24:
            return False
        else:
            # En büyük subnet maskesi 24 (255.255.255.0) ise True döndürün
            return subnet_mask_length == 24

    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
        # Geçersiz IP adresi veya subnet maskesi verilmişse False döndürün
        return False

def validate_subnet_mask4(subnet_mask):
    # Subnet maskesini doğrulama işlemi
    try:
        subnet = ipaddress.IPv4Network(f"0.0.0.0/{subnet_mask}", strict=False)
        return True
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
        return False

def validate_subnet_mask6(subnet_mask):
    # Subnet maskesini doğrulama işlemi
    try:
        print ("sekseksek")
        subnet = ipaddress.IPv6Network("2001:db8::/64", strict=False)
        print("sekseksek444")
        return True
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
        return False


def ping_and_log(ip_address):
    try:
        print ("geldimi")

        # Ping işlemi
        print (ip_address)
        result = subprocess.run(['ping', '-c', '1', ip_address], capture_output=True, text=True, timeout=5)
        print ("ping atti")
        # Ping sonucuna göre aktiflik durumunu belirlelim
        is_active = result.returncode == 0
        # is_active = True
        print ("is_active")
        print(is_active)
        # print("CELERY_BROKER_URL: ", CELERY_BROKER_URL)
        process_subnet_ips.delay(ip_address, is_active)

        return JsonResponse({'message': 'Ping başarılı', 'is_active': is_active})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def update_ip_status(ip_address, status):
    print("************** CACHING ***************")
    key = f'ip_status_{ip_address}'
    print("KEY: ", key)
    cache.set(key, status, timeout=None)  # timeout=None, süresiz saklama anlamına gelir
    print("************ CACHED *******************")
   # process_subnet_ips_caching.delay(ip_address, status)
    return True

#
# return_code = result.returncode
#
#         if return_code == 0:
#             print("Ping başarılı")
#         else:
#             print("Ping başarısız. Çıkış Kodu:", return_code)
#
#         except subprocess.CalledProcessError as e:
#         print("Hata Oluştu:", e)
#     except subprocess.TimeoutExpired:
#         print("İşlem Zaman Aşımına Uğradı")
#     except FileNotFoundError:
#         print("Ping komutu bulunamadı")
#     except Exception as e:
#         print("Bilinmeyen Bir Hata Oluştu:", e)