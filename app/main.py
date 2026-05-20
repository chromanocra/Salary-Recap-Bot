# app/main.py
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import sys
from dotenv import load_dotenv

# Memaksa Python membaca folder utama agar tidak error ModuleNotFound
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import service

load_dotenv()

async def rekap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. Pastikan wajib melakukan reply pesan
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Silakan gunakan perintah ini dengan cara MEMBALAS (reply) pada pesan Bill.")
        return

    # 2. Logika BARU: Jika tidak ada nama client setelah /rekap, otomatis diisi "-"
    if context.args:
        client_name = ' '.join(context.args).strip()
    else:
        client_name = "-" # Kamu bisa ganti dengan "Archer" atau "(Isi Manual)" sesuai selera

    bill_text = update.message.reply_to_message.text
    chat_id = update.message.chat.id
    msg_id = update.message.reply_to_message.message_id
    
    # 3. Format Link Payment Otomatis
    if str(chat_id).startswith("-100"):
        clean_chat_id = str(chat_id)[4:]
        link_payment = f"https://t.me/c/{clean_chat_id}/{msg_id}"
    else:
        link_payment = f"https://t.me/c/{chat_id}/{msg_id}"

    try:
        # Lempar ke service untuk di-scrape
        hasil_rekap = service.scrape_dan_buat_rekap(bill_text, client_name, link_payment)
        await update.message.reply_text(hasil_rekap)
        
    except Exception as e:
        await update.message.reply_text("❌ Gagal men-scrape data. Pastikan teks bill sesuai dengan format asli.")
        print(f"Error detail: {e}")

def main():
    TOKEN = os.getenv("BOT_TOKEN") # Mengambil token dari file .env
    if not TOKEN:
        TOKEN = "BOT_TOKEN" # Backup jika tidak pakai .env
        
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("rekap", rekap))
    
    print("Bot sedang berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()