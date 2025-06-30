from PIL import Image, ImageDraw, ImageFont

def create_basic_icon(filename='app_icon.png', size=256, bg_color='#2e2e2e', fg_color='white', text='CFG'):
    # Create a square image with background color
    img = Image.new('RGBA', (size, size), bg_color)
    draw = ImageDraw.Draw(img)

    # Load a truetype or opentype font file, or use default
    try:
        font = ImageFont.truetype("arial.ttf", int(size / 2))
    except IOError:
        font = ImageFont.load_default()

    # Calculate text size and position
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size - text_width) / 2, (size - text_height) / 2)

    # Draw the text
    draw.text(position, text, font=font, fill=fg_color)

    # Save the image
    img.save(filename)
    print(f"Icon saved as {filename}")

if __name__ == "__main__":
    create_basic_icon()
