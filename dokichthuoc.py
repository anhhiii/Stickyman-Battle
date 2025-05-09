from PIL import Image

# Đường dẫn tới file sprite
image_path = r"D:\UTE\NAM II\HKII\AI\STICK BATTLE PROJECT\Stickyman-Battle\assets\sprites\knight files\knight png\Block\0.png"


# Mở ảnh và lấy kích thước
img = Image.open(image_path)
width, height = img.size

print(f"Kích thước sprite: {width} x {height} pixel")
