# Telegram Watermark Bot

A Telegram bot that adds watermarks to images sent by users.

## Features

- Add custom watermarks to images
- Set custom watermark text using commands
- Automatic image processing and return
- Clean file management (temporary files are removed)

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get a Telegram Bot Token:**
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Use `/newbot` command to create a new bot
   - Follow the instructions to get your bot token

3. **Configure the bot:**
   - Open `telegram_watermark_bot.py`
   - Replace `"YOUR_TELEGRAM_BOT_TOKEN"` with your actual bot token

4. **Run the bot:**
   ```bash
   python telegram_watermark_bot.py
   ```

## Usage

1. **Start the bot:** Send `/start` to your bot
2. **Set watermark text:** Use `/watermark Your Custom Text` to set custom watermark text
3. **Send an image:** Simply send any image to the bot
4. **Get watermarked image:** The bot will process and return the image with watermark

## Commands

- `/start` - Initialize the bot and get welcome message
- `/help` - Show available commands
- `/watermark <text>` - Set custom watermark text

## Notes

- The watermark is placed in the bottom-right corner of the image
- Default watermark text is "Sample Watermark"
- The bot supports common image formats (JPEG, PNG, etc.)
- Images are temporarily downloaded, processed, and cleaned up automatically

## Requirements

- Python 3.7+
- python-telegram-bot >= 20.0
- Pillow >= 9.0.0
