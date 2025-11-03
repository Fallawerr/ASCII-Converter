import os
import sys
from PIL import Image

#u can add charaters if u want
CHARS = " .:-=+*#%@"

def resize_image(image, new_width=100):
    """Resize keeping aspect ratio (0.55 compensates for console font)."""
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio * 0.55)
    return image.resize((new_width, new_height))

def grayscale(image):
    return image.convert("L")

def pixels_to_ascii_gray(image):
    """Map grayscale values to characters."""
    pixels = list(image.getdata())
    return "".join(CHARS[pixel // 32] for pixel in pixels)

def pixels_to_ascii_color(image_rgb, image_gray):
    """Build HTML with per-character RGB colors."""
    pixels_rgb = list(image_rgb.getdata())
    pixels_gray = list(image_gray.getdata())
    width, _ = image_rgb.size
    html = '<pre style="font-size:8px;line-height:8px;letter-spacing:0;font-family:monospace;">\n'
    for i, (r, g, b) in enumerate(pixels_rgb):
        gray = pixels_gray[i]
        char = CHARS[gray // 32]
        html += f'<span style="color:rgb({r},{g},{b})">{char}</span>'
        if (i + 1) % width == 0:
            html += '\n'
    html += '</pre>'
    return html

def save_txt(ascii_art, filename="ascii_art.txt"):
    """Write monochrome ASCII-art."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(ascii_art)
    return filename

def save_html(html_content, filename="ascii_art_color.html"):
    """Wrap HTML in a complete page."""
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ASCII-Art: {os.path.basename(filename)}</title>
    <style>
        body {{ background:#000; color:#fff; text-align:center; padding:20px; }}
        pre {{ display:inline-block; margin:0; }}
    </style>
</head>
<body>
    {html_content}
    <br><small>Created with ASCII-Converter by Fallawerr_</small>
</body>
</html>"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(full_html)
    return filename

def main(path=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "═" * 56)
    print("     PHOTO → ASCII-ART (Pro)".center(56))
    print("═" * 56 + "\n")

    
    if not path:
        try:
            path = input("Drag & drop an image here and press Enter:\n> ").strip().strip('"')
        except Exception:
            path = input("Paste full image path:\n> ").strip().strip('"')

    if not os.path.exists(path):
        print("ERROR: File not found!")
        input("\nPress Enter to exit...")
        return

    
    try:
        image = Image.open(path).convert("RGB")
    except Exception as e:
        print(f"Cannot open image: {e}")
        input("\nPress Enter...")
        return

    
    new_width = 120
    image_resized = resize_image(image, new_width)
    image_gray = grayscale(image_resized)

    
    print("Generating monochrome version (txt)...")
    ascii_gray = pixels_to_ascii_gray(image_gray)
    ascii_gray_lines = "\n".join(
        ascii_gray[i:i + new_width] for i in range(0, len(ascii_gray), new_width)
    )

    
    print("Generating color version (html)...")
    html_content = pixels_to_ascii_color(image_resized, image_gray)

    
    txt_file = save_txt(ascii_gray_lines, "ascii_art.txt")
    html_file = save_html(html_content, "ascii_art_color.html")

   
    print("\nPREVIEW (monochrome):\n")
    preview = ascii_gray_lines[:800]
    print(preview)
    if len(ascii_gray_lines) > 800:
        print("...\n")

    
    print("DONE! Two files have been created:")
    print("─" * 56)
    print(f"1. {os.path.basename(txt_file)}")
    print("   → Monochrome ASCII-art")
    print("   → Open with Notepad, Word, any text editor")
    print("   → Easy to copy-paste into chats")
    print()
    print(f"2. {os.path.basename(html_file)}")
    print("   → Full-color ASCII-art")
    print("   → Open in any web browser (Chrome, Edge, Firefox…)")
    print("   → Preserves original photo colors")
    print("   → Perfect for sharing on the web")
    print("─" * 56)

    
    if os.name == 'nt':
        os.startfile(txt_file)
        os.startfile(html_file)
    else:
        os.system(f"xdg-open '{txt_file}'")
        os.system(f"xdg-open '{html_file}'")

    print(f"\nFiles saved in:\n{os.getcwd()}")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()