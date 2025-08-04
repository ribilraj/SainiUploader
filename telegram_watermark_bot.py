from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from PIL import Image, ImageDraw, ImageFont
import os
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your bot token
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        'Hello! Send me an image and I will add a watermark to it.\n'
        'You can set custom text with /watermark YourText'
    )
    # Default watermark text
    context.user_data['watermark_text'] = "Sample Watermark"

async def set_watermark_text(update: Update, context: CallbackContext) -> None:
    """Set custom watermark text."""
    if context.args:
        new_text = ' '.join(context.args)
        context.user_data['watermark_text'] = new_text
        await update.message.reply_text(f'Watermark text set to: {new_text}')
    else:
        await update.message.reply_text('Please provide watermark text after the command.')

async def add_watermark(update: Update, context: CallbackContext) -> None:
    """Add watermark to the received image."""
    if not update.message.photo:
        await update.message.reply_text("Please send an image.")
        return
    
    # Get watermark text from user data or use default
    watermark_text = context.user_data.get('watermark_text', 'Sample Watermark')
    
    # Get the highest resolution photo
    photo_file = await update.message.photo[-1].get_file()
    
    # Download the image
    input_path = f'input_image_{update.message.chat_id}.jpg'
    await photo_file.download_to_drive(input_path)
    
    # Process the image
    output_path = f'watermarked_image_{update.message.chat_id}.jpg'
    apply_watermark(input_path, output_path, watermark_text)
    
    # Send the watermarked image back
    with open(output_path, 'rb') as photo:
        await update.message.reply_photo(photo=photo)
    
    # Clean up
    try:
        os.remove(input_path)
        os.remove(output_path)
    except FileNotFoundError:
        pass

def apply_watermark(input_path, output_path, text, opacity=0.5):
    """Apply watermark to an image."""
    # Open the image
    base_image = Image.open(input_path).convert("RGBA")
    
    # Create a transparent layer for the watermark
    txt = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
    
    # Get a font (you may need to specify the path to a font file)
    try:
        # Try different common font paths
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/TTF/arial.ttf",
            "/System/Library/Fonts/Arial.ttf",
            "arial.ttf"
        ]
        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, 40)
                break
            except (OSError, IOError):
                continue
        
        if font is None:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()
    
    # Get drawing context
    d = ImageDraw.Draw(txt)
    
    # Calculate text size and position using textbbox (replaces deprecated textsize)
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = base_image.width - text_width - 10
    y = base_image.height - text_height - 10
    
    # Draw the text with opacity
    d.text((x, y), text, font=font, fill=(255, 255, 255, int(255 * opacity)))
    
    # Combine the images
    watermarked = Image.alpha_composite(base_image, txt)
    
    # Convert back to RGB for JPEG saving
    watermarked = watermarked.convert("RGB")
    watermarked.save(output_path, "JPEG", quality=95)

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
Available commands:
/start - Start the bot
/help - Show this help message
/watermark <text> - Set custom watermark text

Just send me an image and I'll add a watermark to it!
    """
    await update.message.reply_text(help_text)

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("watermark", set_watermark_text))
    application.add_handler(MessageHandler(filters.PHOTO, add_watermark))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()