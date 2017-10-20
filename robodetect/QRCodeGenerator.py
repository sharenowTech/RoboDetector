import qrcode.image.svg
import numpy as np
from robodetect.Constants import ROBO_NUM

for i in range(ROBO_NUM):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=15,
        border=4
    )
    qr.add_data(np.int8(i))
    qr.make(fit=True)
    img = qr.make_image(qrcode.image.svg.SvgPathImage)
    img.save('../qrcodes/qrcode_{}.svg'.format(i))

