import re

def format_rupiah(angka):
    """Mengubah angka menjadi format ribuan dengan titik"""
    return f"{angka:,}".replace(',', '.')

def scrape_dan_buat_rekap(bill_text, client_name, link_payment):
    talent_match = re.search(r"(?:and\s+)?([A-Za-z\s]+?)\s+is prepared", bill_text, re.IGNORECASE)
    talent_raw = talent_match.group(1).strip().title() if talent_match else "Unknown Talent"
    
    talent_words = talent_raw.split()
    talent_name = f"{talent_words[0]} {talent_words[1]}" if len(talent_words) > 1 else talent_raw

    session_match = re.search(r"Session\s+Type:\s*(.+)", bill_text, re.IGNORECASE)
    session_type = session_match.group(1).strip() if session_match else "-"

    feeq_match = re.search(r"FEEQ:\s*([\d.]+)", bill_text, re.IGNORECASE)
    feeq = int(feeq_match.group(1).replace('.', '')) if feeq_match else 500

    items = re.findall(r"(?:[-–—•*]\s*)?([^:\n]+?)\s*:\s*([\d.]+)", bill_text)
    
    total_harga = 0
    details_text_rekap = ""
    
    for item_name, item_price in items:
        item_name_clean = item_name.strip().lower()
        
        if "session type" in item_name_clean or "feeq" in item_name_clean or "prepared" in item_name_clean:
            continue
            
        try:
            harga = int(item_price.replace('.', ''))
            total_harga += harga
            details_text_rekap += f"     #. {item_name.strip()} : {format_rupiah(harga)}\n"
        except ValueError:
            continue

    if total_harga < 10000:
        potongan_persen = 10
    elif total_harga < 30000:
        potongan_persen = 12
    else:
        potongan_persen = 15
        
    potongan_agensi = int(total_harga * (potongan_persen / 100))
    gaji_talent = total_harga - potongan_agensi


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