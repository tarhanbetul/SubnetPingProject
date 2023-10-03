# tasks.py 
from celery import Celery

app = Celery('subnetPing')  
from celery import shared_task

@shared_task
def process_subnet_ips(ip_address, subnet_mask):
    try:
        network = ipaddress.ip_network(f"{ip_address}/{subnet_mask}", strict=False)

        response_result_array = []
        for ip in network.hosts():
            ping_result = ping_and_log(str(ip))

            response_result_object = {'Subnet Ip' : str(ip), 'Ping Result': ping_result.get('is_active', False)}
            update_ip_status(str(ip) , ping_result.get('is_active', False))
            response_result_array.append(response_result_object)

        return response_result_array
    except Exception as e:
        raise e- 