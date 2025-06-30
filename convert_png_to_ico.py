from PIL import Image

def convert_png_to_ico(png_filename='app_icon.png', ico_filename='app_icon.ico', sizes=[(256,256), (128,128), (64,64), (32,32), (16,16)]):
    img = Image.open(png_filename)
    img.save(ico_filename, format='ICO', sizes=sizes)
    print(f"Arquivo ICO salvo como {ico_filename}")

if __name__ == "__main__":
    convert_png_to_ico()
