# DarkTunnel Pulder

Project kana keessatti:

- `android_project/` = Android Studio/Gradle project
- `telbot.py` = Telegram bot
- `requirements.txt` = Python dependency

## 1. Android Studio

`android_project` Android Studio keessatti bani.

## 2. Telegram bot

Python 3.10+ irratti:

```bash
pip install -r requirements.txt
```

Token kee environment variable keessa kaa'i:

```bash
export BOT_TOKEN="TOKEN_HAARAA_KEE"
python telbot.py
```

Windows PowerShell:

```powershell
$env:BOT_TOKEN="TOKEN_HAARAA_KEE"
python telbot.py
```

## 3. Build environment

Botichi `gradle assembleDebug` waama. Kanaaf machine irratti:

- JDK 17
- Android SDK
- Android SDK Platform 35
- Gradle

qophaa'uu qabu.

> Token Telegram kee GitHub irratti hin galchin.
> Botichi upload godhamu `MainActivity.java` qofa bakka buusa; Gradle/build files hin jijjiiru.
