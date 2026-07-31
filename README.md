# Türkmopet Bulut Cari, Ürün ve Satış Takibi — v1.4.2

Windows masaüstü uygulaması. İnegöl ve Yenişehir bilgisayarları aynı Supabase bulutuna bağlanır.

## v1.4.2 hızlı müşteri satışı

- Satış ekranı varsayılan olarak **Perakende** seçili açılır.
- Ürün sepete eklenirken toptan/perakende sorusu gösterilmez.
- Ürün adı yanındaki `...` düğmesi ürün listesini açar.
- `...` kullanılmadan ürün adı, miktar ve fiyat yazılırsa manuel satış satırı oluşturulur.
- Barkod okutulan ürün otomatik aranır; bulunmazsa manuel girişe devam edilir.
- Sol alttaki **Toptan / Perakende** düğmeleriyle sepet fiyat türü değiştirilebilir.
- Perakende manuel girişte toptan fiyatı otomatik %10 aşağı hesaplanır.
- Doğrudan toptan girilen satır perakendeye karıştırılmaz.
- Satış tablosu Barkod, Ürün Adı, Miktar, Birim, Fiyat ve Tutar sütunlarına sadeleştirildi.
- Hazır güncelleme paketi: `releases/turkmopet_borc_takip_v1.4.2_hizli_satis_hotfix.zip`

## Sürüm paketini doğrulama

Dağıtım ZIP'i kurulmadan veya paylaşılmadan önce doğrulanmalıdır:

```bat
py -3.12 tools\verify_release.py releases\turkmopet_borc_takip_v1.4.2_hizli_satis_hotfix.zip --version-file VERSION.txt
```

Doğrulayıcı şu risklerde işlemi hatayla durdurur:

- ZIP bozulması veya CRC hatası
- Dizin dışına yazmaya çalışan `../` veya mutlak yollar
- Sembolik bağlantılar
- `.env`, `secrets.json` ve service-role anahtarı gibi hassas dosyalar
- Eksik ya da uyumsuz `VERSION.txt`
- 250 MB sınırını aşan açılmış paket boyutu

Aynı kontroller her pull request'te GitHub Actions tarafından otomatik çalıştırılır.

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

## v1.4.0 özellikleri

- Uyarı Merkezi
- Cari ekstre ve mutabakat PDF
- Kullanıcı ve yetki sistemi
- Manuel/haftalık yedekleme ve geri yükleme

## Çalıştırma

Python 3.12 kurulu Windows bilgisayarda:

```bat
run.bat
```

İlk açılışta gerekli paketler kurulur. `.env` dosyası `run.bat` ile aynı klasörde olmalıdır.

## Güvenlik

Gerçek `.env`, Supabase anahtarları, kullanıcı şifreleri ve yedek dosyaları repository'ye eklenmez. Masaüstü uygulamasında yalnız publishable/anon key kullanılır.
