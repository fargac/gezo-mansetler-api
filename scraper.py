import json
import requests
from bs4 import BeautifulSoup

GAZETELER = [
    {"id": "manset_hurriyet", "name": "Hürriyet", "slug": "hurriyet", "link": "https://www.hurriyet.com.tr"},
    {"id": "manset_sabah", "name": "Sabah", "slug": "sabah", "link": "https://www.sabah.com.tr"},
    {"id": "manset_milliyet", "name": "Milliyet", "slug": "milliyet", "link": "https://www.milliyet.com.tr"},
    {"id": "manset_turkiye", "name": "Türkiye", "slug": "turkiye", "link": "https://www.turkiyegazetesi.com.tr"},
    {"id": "manset_aksam", "name": "Akşam", "slug": "aksam", "link": "https://www.aksam.com.tr"},
    {"id": "manset_yeni_safak", "name": "Yeni Şafak", "slug": "yeni-safak", "link": "https://www.yenisafak.com"},
    {"id": "manset_yeni_akit", "name": "Yeni Akit", "slug": "yeni-akit", "link": "https://www.yeniakit.com.tr"},
    {"id": "manset_dirilis_postasi", "name": "Diriliş P.", "slug": "dirilis-postasi", "link": "https://www.dirilispostasi.com"},
    {"id": "manset_milat", "name": "Milat", "slug": "milat", "link": "https://www.milatgazetesi.com"},
    {"id": "manset_turkgun", "name": "Türkgün", "slug": "turkgun", "link": "https://www.turkgun.com"},
    {"id": "manset_yeni_birlik", "name": "Yeni Birlik", "slug": "yeni-birlik", "link": "https://www.gazetebirlik.com"},
    {"id": "manset_milli_gazete", "name": "Milli Gazete", "slug": "milli-gazete", "link": "https://www.milligazete.com.tr"},
    {"id": "manset_dunya", "name": "Dünya", "slug": "dunya", "link": "https://www.dunya.com"},
    {"id": "manset_yeni_cag", "name": "Yeniçağ", "slug": "yenicag", "link": "https://www.yenicaggazetesi.com.tr"},
    {"id": "manset_yeni_soz", "name": "Yenisöz", "slug": "yenisoz", "link": "https://www.yenisoz.com.tr"},
    {"id": "manset_aydinlik", "name": "Aydınlık", "slug": "aydinlik", "link": "https://www.aydinlik.com.tr"},
    {"id": "manset_dogru-haber", "name": "Doğru Haber", "slug": "dogru-haber", "link": "https://dogruhaber.com.tr"},
    {"id": "manset_takvim", "name": "Takvim", "slug": "takvim-gazetesi", "link": "https://www.takvim.com.tr"},
    {"id": "manset_fanatik", "name": "Fanatik", "slug": "fanatik", "link": "https://www.fanatik.com.tr"},
    {"id": "manset_fotomac", "name": "Fotomaç", "slug": "fotomac", "link": "https://www.fotomac.com.tr"}
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

def akilli_cek():
    print("Sadece 1 gazeteye gidip günün şifresi aranıyor...")
    
    # 1. Sadece Hürriyet'in (veya herhangi birinin) sayfasına git
    url = "https://www.haber7.com/gazete-mansetleri/hurriyet"
    res = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(res.content, "html.parser")
    img_tag = soup.find("img", class_="big")
    
    if img_tag and img_tag.has_attr("src"):
        ornek_src = img_tag["src"]
        
        # 2. Linkin en sonundaki "big_270326_0630.jpg?v=270326_0630" kısmını kesip al
        # Örnek url: https://i13.haber7.net/haber7/gazete/hurriyet/big_270326_0630.jpg?v=270326_0630
        günün_sifresi = ornek_src.split("/")[-1] 
        print(f"Günün Şifresi Bulundu: {günün_sifresi}")
        
        # 3. Şifreyi tüm gazetelere kopyala yapıştır!
        sonuclar = []
        for gazete in GAZETELER:
            guncel_url = f"https://i13.haber7.net/haber7/gazete/{gazete['slug']}/{günün_sifresi}"
            sonuclar.append({
                "id": gazete["id"],
                "name": gazete["name"],
                "todayUrl": guncel_url,
                "webAdresi": gazete["link"]
            })
            
        # 4. JSON'ı Kaydet
        with open("mansetler.json", "w", encoding="utf-8") as f:
            json.dump(sonuclar, f, ensure_ascii=False, indent=4)
            
        print("İşlem ışık hızında tamamlandı!")
    else:
        print("Hata: Örnek gazete resmi bulunamadı!")

if __name__ == "__main__":
    akilli_cek()
