# Türkmopet Bulut Cari, Ürün ve Satış Takibi — v1.4.1

Windows masaüstü uygulaması. İnegöl ve Yenişehir bilgisayarları aynı Supabase bulutuna bağlanır.

## Kaynak paketini açma

Bu repository, güvenlik kontrolünden geçirilmiş **v1.4.1 tam kaynak paketini** içerir. GitHub bağlantısındaki otomatik iş akışı kaynak klasörlerini açmadığı için paket `.bootstrap` altında sıkıştırılmış olarak saklanmaktadır.

Windows'ta repository'yi indirdikten veya klonladıktan sonra:

```bat
KAYNAGI_CIKAR.bat
```

Dosyasına çift tıkla. Python 3.12 ile kaynak dosyaları repository köküne çıkarılır. Komut satırından çalıştırmak için:

```bat
py -3.12 KAYNAGI_CIKAR.py
```

Ardından normal Git işlemleriyle çıkarılan dosyaları yazabilirsin:

```bat
git add -A
git commit -m "feat: add v1.4.1 source"
git push
```

> Gerçek `.env` dosyası, Supabase anahtarı, kullanıcı şifresi, yedek ZIP'leri ve geçici çalışma dosyaları repository'ye eklenmemiştir.

## Temel yapı

- Tedarikçiler ve tedarikçi borçları iki şubede ortaktır.
- Ürün kataloğu ve fiyatlar ortaktır.
- Müşteriler, müşteri satışları ve tahsilatlar şube bazlıdır.
- TL, USD, EUR ve GBP cari hareketleri desteklenir.
- Vadeli/vadesiz borç, ödeme, alacak ve tahsilat tutulur.
- Yıllık bağlantı, taksit, avans, alınan mal ve kalan taahhüt ayrı izlenir.
- PDF/Excel fiş, fatura, katalog ve sözleşmeler bulutta saklanır.

## v1.4.1 arayüz düzenlemesi

- Sol menü 304 px genişliğe çıkarıldı.
- Menü; Genel, Müşteri, Tedarikçi, Ürün ve Sistem gruplarına ayrıldı.
- Menü bölümü kaydırılabilir yapıldı; küçük ekranlarda öğeler artık üst üste binmez.
- Şube seçici büyütüldü ve ayrı bir kart içine alındı.
- Kullanıcı adı/rolü ayrı profil kartında gösterilir.
- Menü öğelerine ikon eklendi.
- Şimdi Yenile ve Oturumu Kapat, sayfa menüsünden ayrılarak sabit alt aksiyonlara dönüştürüldü.
- Bu sürüm veritabanı değişikliği içermez; v1.4.0 SQL'i daha önce çalıştıysa tekrar SQL çalıştırılmaz.

## v1.4.0 özellikleri

### Uyarı Merkezi

- Gecikmiş tedarikçi vadeleri
- Bugünkü ödemeler
- Önümüzdeki 7 gün içindeki vadeler
- Yıllık bağlantı taksitleri
- Gecikmiş/yaklaşan müşteri tahsilatları
- Program açılışında tek seferlik özet

### Cari ekstre ve mutabakat PDF

- Müşteri ve tedarikçi için tarih aralıklı ekstre
- Dönem başı/dönem sonu bakiyesi
- İşlem, vade, belge ve açıklama ayrıntıları
- Müşteri satışlarında ürün özeti
- Mutabakat metni ve imza bölümü

### Kullanıcı ve yetkiler

- Yönetici
- Muhasebe
- Veri giriş personeli
- Sadece görüntüleme
- Özel yetki

Yetkiler tedarikçi, müşteri, ürün, bağlantı, silme, rapor, yedek ve kullanıcı yönetimi olarak ayrı verilir. Denetim geçmişinde işlemi yapan kullanıcı ve bilgisayar görünür.

### Yedekleme

- Manuel tam ZIP yedeği
- Haftalık otomatik yedek
- Bulut tabloları ve belgeler
- ID bazlı birleştirerek geri yükleme

## Çalıştırma

Kaynak paketi çıkarıldıktan sonra Python 3.12 kurulu Windows bilgisayarda:

```bat
run.bat
```

İlk açılışta gerekli paketler kurulur. `.env` dosyası `run.bat` ile aynı klasörde olmalıdır.

## Güvenlik

Masaüstü uygulamasına yalnız Supabase publishable/anon key yazılır. Service-role veya secret key kesinlikle kullanılmaz. Gerçek yapılandırma için kaynak paketteki `.env.example` dosyası kopyalanarak `.env` oluşturulmalıdır.
