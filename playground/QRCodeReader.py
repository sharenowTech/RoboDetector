from PIL import Image
import zbarlight

file_path = 'qrcode_on_robo.jpg'

with open(file_path, 'rb') as fd:
    image = Image.open(fd)
    image.load()

codes = zbarlight.scan_codes('qrcode', image)
print('Code: {}'.format(codes))