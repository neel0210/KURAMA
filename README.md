# 🦊 Kurama Userbot (V.1.0) — S-Rank Arsenal

![Status](https://img.shields.io/badge/Status-Active-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge)
![OS](https://img.shields.io/badge/Platform-Termux%20|%20Linux%20|%20Windows-green?style=for-the-badge)

**Kurama** is a high-performance, modular Telegram Userbot inspired by the Nine-Tails. Built on the **Telethon** library, it is designed for speed, visual flair, and seamless automation across all platforms.

---

## 🏮 Core Features (The 14 Jutsu)

| Jutsu | Description |
| :--- | :--- |
| **.rbg** | **Eraser Style:** Removes backgrounds from images instantly. |
| **.update** | **Reincarnation:** Checks GitHub for new code with visual stickers. |
| **.q** | **Mirror Style:** Transforms messages into elegant stickers (QuotLy). |
| **.dl** | **Extraction:** Downloads media/audio from YouTube and social links. |
| **.tr** | **Universal Tongue:** Translates any text into your target language. |
| **.barcode** | **Digital Vision:** Generates barcodes and QR codes from text. |
| **.purge** | **Battlefield Clear:** Mass-deletes messages in a chat. |
| **.kang** | **Sealing Art:** Steals/Adds stickers to your private collection. |
| **.status** | **Sensing:** Displays system RAM, CPU, and Uptime. |

---

## 🚀 Installation

### 1. Clone the Scroll
git clone [https://github.com/neel0210/kurama.git](https://github.com/neel0210/kurama.git)
cd kurama

### 2. Run the Universal Setup
Our setup.sh handles OS detection, global dependency installation, and .env configuration automatically.
chmod +x setup.sh
./setup.sh

### 3. Required Chakra (.env)
The setup script will prompt you for these variables:
* **API_ID / API_HASH**: Obtain from my.telegram.org.
* **CHAT_ID**: The group ID where Kurama announces his arrival.
* **GIT**: Your GitHub Personal Access Token (for the .update Jutsu).

---

## 🌀 Reincarnation Logic (.update)

Kurama uses a dedicated visual feedback system for updates:

* **.update**: Senses the GitHub repository. If an update is found, Kurama sends the **New Scrolls Detected** sticker.
* **.update install**: Pulls the new code, kills the old process, and restarts the bot instantly.

---

## 🛠️ Mobile Hosting (24/7 Termux)

If running on a spare Android device:
1. Run **termux-wake-lock** in the terminal to prevent sleep.
2. Disable **Battery Optimization** for Termux in Android Settings.
3. Enable **Stay Awake** in Developer Options while charging.

---

## 🤝 Contributing

The Nine-Tails' power grows with its host. To add new modules:
1. Fork the repository.
2. Create your script in the **modules/** folder.
3. Ensure you include a **register(client)** function for Telethon.

---

## ⚖️ Disclaimer

This project is for educational purposes. Use it responsibly. Avoid spamming to keep your account safe from the Telegram **Sealing Jutsu** (Account Ban).

---

**Developed with 🔥 by Neel**
*"The Nine-Tails has been unsealed."*
