from django.db import models
import ipaddress

class Subnet(models.Model):
    ip_address = models.GenericIPAddressField(protocol='both')  # Hem IPv4 hem de IPv6 adreslerini destekler
    subnet_mask = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ip_address}/{self.subnet_mask}"

    class Meta:
        db_table = 'Subnet'

    def get_subnet_addresses(self):
        try:
            network = ipaddress.ip_network(f"{self.ip_address}/{self.subnet_mask}", strict=False)
            addresses = [str(ip) for ip in network.hosts()]
            return addresses
        except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
            return []



class PingResult(models.Model):
    ip_address = models.GenericIPAddressField()
    is_active = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {'Aktif' if self.is_active else 'Aktif Değil'}"

    class Meta:
        db_table = 'PingResult'
