# SubnetPingProject

# Subnet Ping Uygulaması

Uygulamadan girilen IP ve Subnet mask bilgisine göre subnet altındaki tüm IP değerlerini bulan ilgili adrese ping atıp sonuçları API ile listeleyip ilgili log kayıtlarını veritabanına kaydeden servis uygulamasıdır.
Kullanılan Teknolojiler:
Python
Django Restful Framework
PostqreSQL
Docker
Redis
Celery
# Kurulum Başlatma:
Django pip install django python manage.py starapp app_name 
Restful Framework : Oluşturduğumuz django projesi içinde settings.py dosyasında gerekli düzenlemeler yapılmalı serializers.py dosyası oluştutulmalı.
PostqreSQL: Veritabanı (settting.py dosyası ayarları)
Docker :
DockerFile dosyası oluşturma:
Docker-compose.yml dosyası oluşturma
Requirements.py dosyası oluşturma
Redis : Settings.py dosyasında gerekli redis ayarları eklenmeli dockerfile dosyası ve docker-compose.yml ve requirements.py dosyası redis için düzenlenmeli
Celery : Asenkron çalışması için (pip install celery[redis]) Docker dosylarında gerekli düzenlemeler ve settting.py dosyamda düzenlemeler yapılmalı ve tasks.py dosyası oluşturulmalı bu dosyada celery tarafından çalıştırılacak görevler tanımlanmalı ve views.py dosyasında celery kullanarak tasks.py dosyasında görevi çağırmalıyız.
# API Görünümü – IP Kontrol – Ping İşlemi:
Views.py (API Görünümü );
Gelen isteği işler ve içeri alır:
İstekteki IP adresini ve alt ağ maskesini alarak, bir IP ağı (network) oluşturup,
İstekte girilen IP adresi ve alt ağı maskesininin;
 Geçerli bir IP adresi olup olmaığını doğrulamak için validate_ip_adress
Geçerli bir IPv4 veya IPv6 subnet maskesi olup olmaığını doğrulamak için validate_subnet_mask4 ve validate_subnet_mask6 
İstekte gönderilen IP adresinin sürümü için get_ip_version
Belirtilen IP adresine ping atması için ping_and_log
IP adresinin durumu için cache_ip_status
fonksiyonları hazırlandı.
ping_and_log işlevini kullanarak belirtilen IP adresine ping atması sağlandı ve sonucu kaydedildi.
Celery workerlarının çalışması için tasks.py dosyasında loglara ping sonuçlarını ve status durumunu gönderip veritabanına kaydetme görevi tanımlanmalı.
Subnet masklerin bulunup gereki kontrollerin sağlanıp ping atma işleminin gerçekleşmesi senkron bir şekilde işletiliyorken Ip ve ping durumu veritabanına kaydetme süreci asenkron şekilde celery workerları ile sağlanmıştır. Bu şekilde Apinin cevap dönmesi için veritabanına kaydetme işleminin beklenmesine gerek kalmamıştır. Celery workerı tetiklendikten sonra başka bir metod ile ilgili ip ve status değeri redis cache 10 dk süre ile tutulacak şekilde kaydedilmiştir.

# Veritabanı İşlemleri:
IP adresi IPv4 ve IPv6 destekli (GenericIPAdress(both) 
Aktiflik durumu (is_active- boolean ) 
Zaman bilgisini tutan bir tablo oluşturdum
Tablomu oluşturutan sonra veya veritabanında bir değişiklik yapıldıktan sonra 
--python manage.py migrate
--python manage.py migrations
Komutları çalıştırılmalı.
Docker- Redis- Celery:
Projemde gerekli isteği işleyip kontrolleri tamamlayıp localde test ettiktan sonra;
Docker desktop engine uygulamasını indirilmeli.
Projemi docker da ayağa kaldırmak için;
Docker-compose.yml dosyası oluşturdum ve version ve docker-compose ağını, gerekli servis (web, db, redis, celery) servislerinin birbirlerine bağımlılıklarını tanımladım. 
DockerFile dosyası için çalışma dizinimi path bilgimi ve proje kullandığım dil ve teknolojilerin sürüm bilgilerini içeren requirements.py dosyamı projeyi çalıştırma komutumu (sanal ortam için:venv içerisnde) indirmesi gereken celery paketini.. vs  tanımlayarak düzenlenmelidir.
# Kullanılan teknolojilerin sürüm bilgileri:
Python : 3.9
Django :3.2.9
Django RestFramework :3.13.1
Django-Redis :5.0.0
Celery :5.2.3
PostgreSQl :16


# PROJEYİ BAŞLATMAK İÇİN KOMUTLAR

1) cd C:\Users\numan\OneDrive\Desktop\subnet_project
2) docker-compose up --build

# REDIS CONTAINERINDA CACHED VERİLERİ GÖRMEK İÇİN KOMUTLAR

1) docker exec -it redis bash
2) redis-cli -u redis://redis:6379/1
3) KEYS *                   --> tüm keyleri bul
4) GET <KEY_NAME>           --> bulduğun keylerden birinin valuesuna bak

# POSTGRE CONTAINERINDA VERİLERİ GÖRMEK İÇİN KOMUTLAR

1) docker exec -it db psql -U postgres  --> postgre container'a bağlan
2) \l                                   --> db leri listele
3) \c subnetPing                        --> db ye bağlan
4) \dt                                  --> tabloları listele
5) SELECT * FROM public."PingResult";   --> verileri listele

# CELERY CONTAINERI KUYRUKLANMIŞ TASKLERİ GÖRMEK İÇİN KOMUTLAR

1) docker exec -it celery sh                   --> celery container'a bağlan
2) celery -A mycelery inspect registered       --> taskleri bul 
(NOT : sadece register olmuş taskler görünür kuyruklanmış taskler hızlı işlendiği için anlık kuyruklar görüntülenemiyor)