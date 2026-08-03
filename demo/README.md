# İzole Demo Modu

Bu klasör, muhasebe programının paylaşılabilir örnek sürümüdür.

## Güvenlik garantileri

- Supabase veya başka bir bulut servisine bağlanmaz.
- `.env` okumaz.
- HTTP, socket veya harici API kullanmaz.
- Gerçek şirket verisi içermez.
- Tüm kayıtlar kurgusaldır.
- SQLite veritabanı yalnız RAM içinde (`:memory:`) oluşturulur.
- Uygulama kapandığında demo verileri tamamen silinir.
- Üretim uygulamasının veritabanına veya dosyalarına dokunmaz.

## Çalıştırma

Python 3.12 kurulu bir bilgisayarda repository kökünden:

```bash
python demo/demo_app.py
```

Windows'ta `demo/CALISTIR_DEMO.bat` dosyasına çift tıklanabilir.

> Bu demo yalnız arayüz ve temel cari/stok akışını göstermek içindir. Gerçek kullanıcı girişi, bulut senkronizasyonu, yedekleme ve üretim verisi bağlantıları bilerek bulunmaz.
