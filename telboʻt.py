import telebot
import os
import subprocess
import threading
import shutil

TOKEN = '8916070168:AAHbEOoLjRJl28zzxgNcy6re2tkRDaSDCO4'
bot = telebot.TeleBot(TOKEN)

# Bakka project-iin Android itti qophaa'u
BASE_DIR = 'android_project'
OUTPUT_DIR = 'dist'
os.makedirs(OUTPUT_DIR, exist_ok=True)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👑 Nagayaan dhuftan! Ani DarkTunnel APK Creator Bot dha.\n\n"
        "Faayilii Java (MainActivity.java) kee naaf ergi, anis Android Studio Project keessatti qindeessee APK qabatamaatti siif jijjiiree nan erga! 🚀"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        file_name = message.document.file_name
        
        if not (file_name.endswith('.java') or file_name.endswith('.txt')):
            bot.reply_to(message, "⚠️ Maaloo, faayilii qofaaf **.java** ykn **.txt** ta'e naaf ergi!")
            return

        bot.reply_to(message, "📥 Faayiliin kee fudhatameera... App-ii qopheessaa jirra, Mee xiqqoo na eegi ⏳")

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Bakka koodiin Java itti kuufamu (Fakkeenyaaf Android project keessatti bakki itti fe'amu)
        # Asitti iddoon appii kee jiru keessatti MainActivity.java bakka buufama
        target_java_path = os.path.join(BASE_DIR, 'app', 'src', 'main', 'java', 'com', 'darktunnel', 'app', 'MainActivity.java')
        
        # Yooディレクトリn hin jirre uumuu
        os.makedirs(os.path.dirname(target_java_path), exist_ok=True)
        
        with open(target_java_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Thread fayyadamuun bot akka hin qabamneef
        threading.Thread(target=compile_android_app, args=(message.chat.id,)).start()

    except Exception as e:
        bot.reply_to(message, f"❌ Rakkoon uumameera: {e}")

def compile_android_app(chat_id):
    try:
        bot.send_message(chat_id, "⚙️ Gradle Build fi APK qopheessuun eegalameera... Kun daqiiqaa muraasa fudhachuu danda'a ⏳")
        
        # Toora (Command) Gradle fayyadamuun APK ijaaruu (Build)
        # `./gradlew assembleDebug` Linux/VPS irratti hojjeta
        process = subprocess.run(
            ['./gradlew', 'assembleDebug'],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )
        
        if process.returncode == 0:
            bot.send_message(chat_id, "✅ Koodiin kee milkaa'inaan qindaa'eera! APK erguuf qophaa'aa jira...")
            
            # Bakka APK-n ijaaramee taa'u (Debug APK path)
            apk_path = os.path.join(BASE_DIR, 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk')
            
            if os.path.exists(apk_path):
                with open(apk_path, 'wb' if False else 'rb') as apk_file:
                    bot.send_document(chat_id, apk_file, caption="🎉 Kunoo App-iin (APK) kee qophaa'eera!")
            else:
                bot.send_message(chat_id, "❌ Faayiliin APK hin argamne, garuu build milkaa'eera jedhamee jira.")
        else:
            # Dogongora koodii keessatti argame erguuf
            error_msg = process.stderr[-1000:] if len(process.stderr) > 1000 else process.stderr
            bot.send_message(chat_id, f"❌ Koodii keessatti dogongorri (Syntax Error) argame:\n\n`{error_msg}`", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(chat_id, f"❌ Build gochuuf yeroo rakkoon uumame: {e}")

bot.polling()
