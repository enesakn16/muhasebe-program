# Güvenlik Politikası

## Desteklenen sürüm

Güvenlik düzeltmeleri yalnızca `main` dalındaki en güncel sürüm için hazırlanır. Eski ZIP paketleri ve önceki sürümler güvenlik güncellemesi almaz.

## Güvenlik açığı bildirimi

Bir güvenlik açığı bulursanız herkese açık issue açmayın. Repository sahibine GitHub üzerinden özel olarak ulaşın ve aşağıdaki bilgileri paylaşın:

- Etkilenen sürüm veya commit
- Açığın tekrar üretim adımları
- Beklenen ve gerçekleşen davranış
- Varsa ekran görüntüsü, log veya örnek veri
- Olası etki ve önerilen çözüm

Bildirime gerçek müşteri verisi, parola, Supabase anahtarı, `.env` içeriği veya kişisel veri eklemeyin.

## Sırlar ve yapılandırma

- Gerçek `.env` dosyaları commit edilmemelidir.
- Masaüstü istemcisinde yalnız Supabase publishable/anon key kullanılmalıdır.
- `service_role` anahtarı, veritabanı parolası ve yönetici sırları istemciye gömülmemelidir.
- Log, yedek, dışa aktarma ve ekran görüntülerindeki kişisel veriler paylaşılmadan önce maskelenmelidir.
- Yanlışlıkla bir sır commit edilirse dosyayı silmek yeterli değildir; ilgili anahtar hemen iptal edilmeli ve yenilenmelidir.

## Kapsam dışı

Yalnızca eski ve desteklenmeyen paketlerde bulunan sorunlar, sosyal mühendislik ve gerçek veri üzerinde izinsiz testler kapsam dışıdır.
