from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # ⚠️ desativa proteção de tamanho de arquivo

img = Image.open("imagem_aleatoria_1gb.ppm")
print(img.size)
img.show()