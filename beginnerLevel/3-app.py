import streamlit as st
import pandas as pd

if 'kisi_listesi' not in st.session_state:
    st.session_state.kisi_listesi = []
if 'tum_gruplar' not in st.session_state:
    st.session_state.tum_gruplar = set()
if 'sonraki_id' not in st.session_state:
    st.session_state.sonraki_id = 1

# Örnek verileri yükleme fonksiyonu
def ornek_veriler_yukle():
    st.session_state.kisi_listesi = [
        {
            "id": 1,
            "isim": "Ahmet Yılmaz",
            "iletisim_bilgisi": ("555-123-4567", "ahmet@ornek.com"),
            "gruplar": {"aile", "arkadaş"}
        },
        {
            "id": 2,
            "isim": "Ayşe Demir",
            "iletisim_bilgisi": ("555-234-5678", "ayse@ornek.com"),
            "gruplar": {"iş", "arkadaş"}
        },
        {
            "id": 3,
            "isim": "Mehmet Kaya",
            "iletisim_bilgisi": ("555-345-6789", "mehmet@ornek.com"),
            "gruplar": {"iş"}
        }
    ]
    
    # Grupları ve sonraki ID'yi güncelle
    st.session_state.tum_gruplar = set()
    for kisi in st.session_state.kisi_listesi:
        st.session_state.tum_gruplar.update(kisi["gruplar"])
    
    st.session_state.sonraki_id = max([kisi["id"] for kisi in st.session_state.kisi_listesi]) + 1
    
    st.success(f"Örnek veriler yüklendi: {len(st.session_state.kisi_listesi)} kişi ve {len(st.session_state.tum_gruplar)} grup")

# Kişi ekleme fonksiyonu
def kisi_ekle(isim, telefon, email, gruplar_str):
    if not isim:
        st.error("İsim gereklidir")
        return False
    
    gruplar = {grup.strip() for grup in gruplar_str.split(",")} if gruplar_str else set()
    
    # Yeni kişi oluştur
    yeni_kisi = {
        "id": st.session_state.sonraki_id,
        "isim": isim,
        "iletisim_bilgisi": (telefon, email),
        "gruplar": gruplar
    }
    
    st.session_state.kisi_listesi.append(yeni_kisi)
    st.session_state.tum_gruplar.update(gruplar)
    st.session_state.sonraki_id += 1
    
    return True

# Kişi silme fonksiyonu
def kisi_sil(kisi_id):
    for i, kisi in enumerate(st.session_state.kisi_listesi):
        if kisi["id"] == kisi_id:
            del st.session_state.kisi_listesi[i]
            
            # Kalan kişilerin ID'lerini yeniden numaralandır
            for j, k in enumerate(st.session_state.kisi_listesi):
                k["id"] = j + 1
            
            # Grupları yeniden hesapla
            st.session_state.tum_gruplar = set()
            for k in st.session_state.kisi_listesi:
                st.session_state.tum_gruplar.update(k["gruplar"])
            
            # Sonraki ID'yi güncelle
            st.session_state.sonraki_id = len(st.session_state.kisi_listesi) + 1
            
            return True
    return False

# Kişi güncelleme fonksiyonu
def kisi_guncelle(kisi_id, isim, telefon, email, gruplar_str):
    for i, kisi in enumerate(st.session_state.kisi_listesi):
        if kisi["id"] == kisi_id:
            # Sadece değer sağlandıysa güncelle
            if isim:
                st.session_state.kisi_listesi[i]["isim"] = isim
            
            # İletişim bilgisi tuple'ını güncelle
            mevcut_telefon, mevcut_email = kisi["iletisim_bilgisi"]
            yeni_telefon = telefon if telefon else mevcut_telefon
            yeni_email = email if email else mevcut_email
            st.session_state.kisi_listesi[i]["iletisim_bilgisi"] = (yeni_telefon, yeni_email)
            
            # Gruplar sağlandıysa güncelle
            if gruplar_str:
                gruplar = {grup.strip() for grup in gruplar_str.split(",")}
                st.session_state.kisi_listesi[i]["gruplar"] = gruplar
                
                # Tüm grupları yeniden hesapla
                st.session_state.tum_gruplar = set()
                for k in st.session_state.kisi_listesi:
                    st.session_state.tum_gruplar.update(k["gruplar"])
            
            return True
    return False

# Kişileri tablo olarak gösterme fonksiyonu
def kisileri_goster(gosterilecek_kisiler=None):
    if gosterilecek_kisiler is None:
        gosterilecek_kisiler = st.session_state.kisi_listesi
    
    if not gosterilecek_kisiler:
        st.info("Gösterilecek kişi yok")
        return
    
    
    veri = []
    for kisi in gosterilecek_kisiler:
        veri.append({
            "ID": kisi["id"],
            "İsim": kisi["isim"],
            "Telefon": kisi["iletisim_bilgisi"][0],
            "E-posta": kisi["iletisim_bilgisi"][1],
            "Gruplar": ", ".join(kisi["gruplar"])
        })
    
    df = pd.DataFrame(veri)
    st.dataframe(df, use_container_width=True)

# İstatistikleri gösterme fonksiyonu
def istatistikleri_goster():
    if not st.session_state.kisi_listesi:
        st.info("Kişi listesi boş, istatistik hesaplanamıyor.")
        return
    
    kisi_sayisi = len(st.session_state.kisi_listesi)
    
    # Grup istatistikleri
    grup_istatistik = {}
    for grup in st.session_state.tum_gruplar:
        grup_istatistik[grup] = 0
    
    for kisi in st.session_state.kisi_listesi:
        for grup in kisi["gruplar"]:
            grup_istatistik[grup] += 1
    
    # İstatistik hesapla
    toplam_grup_uyelik = sum(len(kisi["gruplar"]) for kisi in st.session_state.kisi_listesi)
    ort_grup = toplam_grup_uyelik / kisi_sayisi if kisi_sayisi > 0 else 0
    
    # İstatistikleri göster
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Toplam Kişi", kisi_sayisi)
        st.metric("Toplam Grup", len(st.session_state.tum_gruplar))
    
    with col2:
        st.metric("Kişi Başına Ort. Grup", f"{ort_grup:.2f}")
        if grup_istatistik:
            en_buyuk_grup = max(grup_istatistik.items(), key=lambda x: x[1])
            st.metric("En Büyük Grup", f"{en_buyuk_grup[0]} ({en_buyuk_grup[1]})")
    
    # Grup dağılımı
    if grup_istatistik:
        st.subheader("Grup Dağılımı")
        
       
        grafik_veri = pd.DataFrame({
            'Grup': list(grup_istatistik.keys()),
            'Sayı': list(grup_istatistik.values()),
            'Yüzde': [f"%{count/kisi_sayisi*100:.1f}" for count in grup_istatistik.values()]
        })
        
        st.dataframe(grafik_veri, use_container_width=True)
        
        
        st.bar_chart(grafik_veri.set_index('Grup')['Sayı'])

# Ana uygulama
def main():
    st.title("Kişi Rehberi")
    
    # Kenar çubuğu navigasyonu
    st.sidebar.title("Menü")
    sayfa = st.sidebar.radio("Git", ["Kişileri Görüntüle", "Kişi Ekle", "Kişi Güncelle", "Kişi Sil", "İstatistikler"])
    
    if st.sidebar.button("Örnek Verileri Yükle"):
        ornek_veriler_yukle()
    
    # Sayfa içeriği
    if sayfa == "Kişileri Görüntüle":
        st.header("Tüm Kişiler")
        kisileri_goster()
    
    elif sayfa == "Kişi Ekle":
        st.header("Yeni Kişi Ekle")
        
        isim = st.text_input("İsim")
        telefon = st.text_input("Telefon")
        email = st.text_input("E-posta")
        gruplar = st.text_input("Gruplar (virgülle ayırın)")
        
        if st.button("Kişi Ekle"):
            if kisi_ekle(isim, telefon, email, gruplar):
                st.success(f"'{isim}' başarıyla eklendi!")
    
    elif sayfa == "Kişi Güncelle":
        st.header("Kişi Güncelle")
        
        
        kisileri_goster()
        
        # Güncelleme formu
        st.subheader("Güncellenecek Bilgileri Girin")
        kisi_id = st.number_input("Güncellenecek Kişi ID", min_value=1, step=1)
        
        # Mevcut kişiyi bul
        mevcut_kisi = None
        for kisi in st.session_state.kisi_listesi:
            if kisi["id"] == kisi_id:
                mevcut_kisi = kisi
                break
        
        if mevcut_kisi:
            st.info(f"Güncelleniyor: {mevcut_kisi['isim']}")
            isim = st.text_input("Yeni İsim (değiştirmek istemiyorsanız boş bırakın)")
            telefon = st.text_input("Yeni Telefon (değiştirmek istemiyorsanız boş bırakın)")
            email = st.text_input("Yeni E-posta (değiştirmek istemiyorsanız boş bırakın)")
            gruplar = st.text_input("Yeni Gruplar (virgülle ayırın, değiştirmek istemiyorsanız boş bırakın)")
            
            if st.button("Kişiyi Güncelle"):
                if kisi_guncelle(kisi_id, isim, telefon, email, gruplar):
                    st.success("Kişi başarıyla güncellendi!")
        else:
            st.warning(f"ID {kisi_id} olan kişi bulunamadı.")
    
    elif sayfa == "Kişi Sil":
        st.header("Kişi Sil")
        
        
        kisileri_goster()
        
        # Silme formu
        kisi_id = st.number_input("Silinecek Kişi ID", min_value=1, step=1)
        
        if st.button("Kişiyi Sil"):
            if kisi_sil(kisi_id):
                st.success(f"ID {kisi_id} olan kişi silindi!")
            else:
                st.error(f"ID {kisi_id} olan kişi bulunamadı.")
    
    elif sayfa == "İstatistikler":
        st.header("Kişi İstatistikleri")
        istatistikleri_goster()

if __name__ == "__main__":
    main()