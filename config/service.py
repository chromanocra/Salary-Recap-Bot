# config/service.py
import re

def format_rupiah(angka):
    """Mengubah angka menjadi format ribuan dengan titik"""
    return f"{angka:,}".replace(',', '.')

def scrape_dan_buat_rekap(bill_text, client_name, link_payment):
    # 1. Scrape Nama Talent (Mencari teks di antara 'and' dan 'is prepared')
    talent_match = re.search(r"and\s+(.+?)\s+is prepared", bill_text, re.IGNORECASE)
    talent_raw = talent_match.group(1).strip().title() if talent_match else "Unknown Talent"
    
    # Mengambil 2 kata pertama dari nama talent (Contoh: KIER JORELL PEARCE -> Kier Jorell)
    talent_words = talent_raw.split()
    talent_name = f"{talent_words[0]} {talent_words[1]}" if len(talent_words) > 1 else talent_raw

    # 2. Scrape Session Type (Mencari teks setelah 'Session Type:')
    session_match = re.search(r"Session\s+Type:\s*(.+)", bill_text, re.IGNORECASE)
    session_type = session_match.group(1).strip() if session_match else "-"

    # 3. Scrape FEEQ (Mencari angka setelah 'FEEQ:')
    feeq_match = re.search(r"FEEQ:\s*([\d.]+)", bill_text, re.IGNORECASE)
    feeq = int(feeq_match.group(1).replace('.', '')) if feeq_match else 500

    # 4. Scrape Rincian Item (Mendukung berbagai jenis simbol strip/bullet)
    items = re.findall(r"[-–—•*]\s*(.*?)\s*:\s*([\d.]+)", bill_text)
    
    total_harga = 0
    details_text_rekap = ""
    
    for item_name, item_price in items:
        # Abaikan jika baris tersebut adalah FEEQ (biar tidak double hitung)
        if "feeq" in item_name.lower():
            continue
        harga = int(item_price.replace('.', ''))
        total_harga += harga
        details_text_rekap += f"     #. {item_name.strip()} : {format_rupiah(harga)}\n"

    # 5. Hitung Potongan Gaji (15%)
    potongan_persen = 15
    potongan_agensi = int(total_harga * (potongan_persen / 100))
    gaji_talent = total_harga - potongan_agensi

    # 6. Susun jadi format Rekap Akhir
    rekap_text = (
        f"SALARY. {potongan_persen}%.\n\n"
        f"Talent's Name : {talent_name}\n"
        f"1. Client's Name: {client_name}\n"
        f"2. Session Type: {session_type}\n"
        f"3. Detail Payment:\n"
        f"{details_text_rekap}"
        f"     #. FEEQ : {format_rupiah(feeq)}\n"
        f"4. Total Received:\n"
        f"     Talent’s Income.\n"
        f"      {format_rupiah(total_harga)} - {potongan_persen}% = {format_rupiah(gaji_talent)} IDR\n"
        f"     Agency Income =  {format_rupiah(potongan_agensi)} IDR\n"
        f"5. Link payment = {link_payment}"
    )
    
    return rekap_text