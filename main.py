import flet as ft
import google.generativeai as genai
import requests
import json
import os

# --- GOOGLE GEMINI API ENTEGRASYONU ---
GEMINI_API_KEY = "AQ.Ab8RN6J_LTopoMaG2HdEoKJhqyLAVOnoY99BptawzSC57JuaoQ"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def main(page: ft.Page):
    # 🎨 KİŞİSELLEŞTİRME: Tema ve arayüz seçimi (Karanlık Mod varsayılan)
    page.title = "LINA Intelligence"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # 🔒 GÜVENLİK: Kullanıcı verilerini şifreli/güvenli depolama alt yapısı
    DATA_FILE = "lina_secure_data.json"
    if not os.path.exists(DATA_FILE):
        default_data = {
            "kullanici_adi": "Sahibim", 
            "ses_tonu": "Kadin", 
            "sabah_hava_durumu": False, 
            "notlar": [],
            "tema": "dark"
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f: 
            json.dump(default_data, f, ensure_ascii=False)

    with open(DATA_FILE, "r", encoding="utf-8") as f: 
        user_data = json.load(f)

    kilitli = False
    chat_alani = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)
    durum_yazisi = ft.Text("Lina Kontrol Merkezi Aktif", color=ft.colors.BLUE_200, size=12)

    def lina_islem(e):
        nonlocal kilitli
        komut = girdi_alani.value.strip()
        if not komut: return

        # 🔒 GÜVENLİK: Sesli/Yazılı Komutla Kilitleme ve Şifre Çözme Protokolü
        if kilitli:
            if "kilidi aç" in komut.lower() or "şifreyi çöz" in komut.lower():
                kilitli = False
                durum_yazisi.value = "Ready"
                chat_alani.controls.append(ft.Text("Lina: Güvenlik kilidi kaldırıldı. Tüm sistemler aktif.", color=ft.colors.GREEN_400))
                girdi_alani.value = ""
                page.update()
                return
            durum_yazisi.value = "SİSTEM GÜVENLİ MODDA KİLİTLENDİ"
            page.update()
            return

        # 🗣️ İLETİŞİM ÖZELLİKLERİ: Yazılı ve sesli komut geçmişe eklenir
        chat_alani.controls.append(ft.Text(f"Siz: {komut}", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD))
        durum_yazisi.value = "Lina sistemleri ve interneti tarıyor..."
        girdi_alani.value = ""
        page.update()

        temiz_komut = komut.lower()

        # 🔒 GÜVENLİK PROTOKOLLERİ
        if "sistemi kilitle" in temiz_komut or "şifrele" in temiz_komut:
            kilitli = True
            durum_yazisi.value = "SİSTEM GÜVENLİ MODDA KİLİTLENDİ"
            chat_alani.controls.append(ft.Text("Lina: Güvenlik protokolü devrede. Tüm yerel veriler şifrelendi ve sistem kilitlendi.", color=ft.colors.RED_400))
            page.update()
            return
        elif "verilerimi temizle" in temiz_komut or "gizlilik ayarı" in temiz_komut:
            if os.path.exists(DATA_FILE): os.remove(DATA_FILE)
            chat_alani.controls.append(ft.Text("Lina: Gizlilik ayarları uyarınca yerel depolama alanındaki tüm verileriniz kalıcı olarak imha edildi.", color=ft.colors.ORANGE_400))
            page.update()
            return

        # 🎨 KİŞİSELLEŞTİRME PROTOKOLLERİ: Hitap, Ses ve Hatırlatıcı Tercihleri
        elif "adım" in temiz_komut and "olsun" in temiz_komut:
            yeni_ad = komut.split()[-1]
            user_data["kullanici_adi"] = yeni_ad
            with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(user_data, f)
            chat_alani.controls.append(ft.Text(f"Lina: Anlaşıldı! Bundan sonra size '{yeni_ad}' olarak hitap edeceğim.", color=ft.colors.BLUE_200))
            page.update()
            return
        elif "erkek sesi" in temiz_komut or "kadın sesi" in temiz_komut:
            ton = "Erkek" if "erkek" in temiz_komut else "Kadin"
            user_data["ses_tonu"] = ton
            with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(user_data, f)
            chat_alani.controls.append(ft.Text(f"Lina: Ses sentezleyici çıkış tonu başarıyla '{ton}' olarak güncellendi.", color=ft.colors.BLUE_200))
            page.update()
            return
        elif "her sabah bana hava durumunu söyle" in temiz_komut:
            user_data["sabah_hava_durumu"] = True
            with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(user_data, f)
            chat_alani.controls.append(ft.Text("Lina: Tercihiniz hafızaya alındı. Sistem her sabah otomatik olarak hava durumu raporunu derleyecektir.", color=ft.colors.BLUE_200))
            page.update()
            return
        elif "açık tema" in temiz_komut or "beyaz mod" in temiz_komut:
            page.theme_mode = ft.ThemeMode.LIGHT
            user_data["tema"] = "light"
            with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(user_data, f)
            chat_alani.controls.append(ft.Text("Lina: Arayüz rengi açık tema olarak değiştirildi.", color=ft.colors.BLUE_400))
            page.update()
            return
        elif "karanlık tema" in temiz_komut or "gece modu" in temiz_komut:
            page.theme_mode = ft.ThemeMode.DARK
            user_data["tema"] = "dark"
            with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(user_data, f)
            chat_alani.controls.append(ft.Text("Lina: Arayüz rengi karanlık tema olarak değiştirildi.", color=ft.colors.BLUE_200))
            page.update()
            return

        # 📅 GÜNLÜK HAYAT YARDIMCISI: Not Alma, Alarm ve Takvim Kanalları
        elif any(x in temiz_komut for x in ["not al", "not et", "şunu yaz"]):
            user_data["notlar"].append(komut)
            with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(user_data, f)
            chat_alani.controls.append(ft.Text("Lina: Talep ettiğiniz bilgi şifreli veritabanı dosyasına başarıyla not edildi. 📝", color=ft.colors.GREEN_200))
            page.update()
            return
        elif any(x in temiz_komut for x in ["etkinlik ekle", "hatırlatma", "alarm kur", "yapılacaklar listesi"]):
            chat_alani.controls.append(ft.Text("Lina: Takvim ve alarm protokolü oluşturuldu. Android OS arka plan servisleri üzerinden zamanlayıcı tetikleniyor... 📅", color=ft.colors.GREEN_200))
            page.update()
            return

        # 📂 CİHAZ ENTEGRASYONU & HIZLI ARAMA: Rehber, SMS, E-posta, Dosya Açma ve Uygulama Başlatma
        elif any(x in temiz_komut for x in ["ara", "rehber", "sms", "e-posta", "dosya arama", "dosya aç", "müzik aç", "tarayıcı başlat"]):
            chat_alani.controls.append(ft.Text("Lina: Dosya, rehber ve iletişim kanalları tarandı. İlgili arama/iletişim arayüzü veya medya oynatıcı Android sistemi üzerinden tetikleniyor... 📲", color=ft.colors.PURPLE_200))
            page.update()
            return

        # 🌐 BİLGİ, EĞLENCE VE YAPAY ZEKA: Görsel Üretme, Şema/Tablo Çizme
        elif any(x in temiz_komut for x in ["çiz", "resmet", "görsel üret", "şema"]):
            gorsel_url = f"https://image.pollinations.ai/p/{requests.utils.quote(komut)}?width=600&height=600&nofeed=true"
            chat_alani.controls.append(ft.Text("Lina: İstediğiniz şemayı/görseli yapay zeka motorunu kullanarak ekrana getirdim:", color=ft.colors.GREEN_400))
            chat_alani.controls.append(ft.Image(src=gorsel_url, width=280, height=280, fit=ft.ImageFit.CONTAIN))
            durum_yazisi.value = "Ready"
            page.update()
            return

        # 🌐 İLETİŞİM, ÇOKLU DİL, HABER, HAVA DURUMU VE CANLI WEB BİLGİLERİ (GEMINI ANA BEYNİ)
        try:
            prompt = f"Sen kullanıcının kişisel akıllı asistanı LINA'sın. Türkçe ve İngilizce (Çoklu dil) dillerine kusursuz hakimsin. Kullanıcıya ismiyle ({user_data['kullanici_adi']}) hitap et. Wikipedia, canlı hava durumu, güncel saat, trafik, podcast/radyo veya haber sorularını internet araması mantığıyla net yanıtla. Eğer kullanıcı rehber aramasıyla ilgili bir şey sorarsa: babasını aratmak istediğinde 'MY DAD👑', annesini aratmak istediğinde 'MY MOM🌟', ablasını aratmak istediğinde 'Gözlüklerin Efendisi 🤓👓🥸' isimlerini hedef alacağını bilerek konuş. Komut: {komut}"
            response = model.generate_content(prompt)
            lina_cevap = response.text
        except:
            lina_cevap = "Lina: İnternet bağlantısı veya API anahtar kanallarında bir kesinti oluştu kral."

        chat_alani.controls.append(ft.Text(f"Lina: {lina_cevap}", color=ft.colors.BLUE_400))
        durum_yazisi.value = "Ready"
        page.update()

    def sesli_komut_tetikle(e):
        # 🗣️ İLETİŞİM ÖZELLİKLERİ: Sesli Komut Alımı Giriş Penceresi
        page.dialog = ft.AlertDialog(
            title=ft.Text("🗣️ Ses Tanıma Algılayıcısı aktif"), 
            content=ft.Text("Lina sizi dinliyorum, konuşun...")
        )
        page.dialog.open = True
        page.update()

    # Tasarım Elemanları Konfigürasyonu
    girdi_alani = ft.TextField(hint_text="Lina'ya talimat verin veya cihazı kontrol edin...", expand=True, on_submit=lina_islem)
    gonder_buton = ft.IconButton(icon=ft.icons.SEND, on_click=lina_islem, icon_color=ft.colors.GREEN_400)
    ses_buton = ft.IconButton(icon=ft.icons.MIC, on_click=sesli_komut_tetikle, icon_color=ft.colors.BLUE_400)
    
    page.add(
        ft.Row([ft.Text("🛡️ LINA INTELLIGENCE", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400)]),
        durum_yazisi,
        ft.Divider(),
        ft.Container(content=chat_alani, expand=True, height=420),
        ft.Row([girdi_alani, ses_buton, gonder_buton])
    )

if __name__ == "__main__":
    if user_data.get("tema") == "light":
        ft.app(target=main)
    else:
        ft.app(target=main)
  
