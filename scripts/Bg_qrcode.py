import qrcode
from PIL import Image
import base64
from io import BytesIO
from qrcode.image.styledpil import StyledPilImage  # Import for styled QR code generation
from qrcode.image.styles.colormasks import ImageColorMask  # Import for color masking

def generate_qr_code(url, logo_path=None, qr_color=(0, 0, 0), background_color=(255, 255, 255)):
    # Create QR Code object
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    # Check if the background image (logo) is provided
    if logo_path:
        bg = Image.open(logo_path)
        qr_img = qr.make_image(
            image_factory=StyledPilImage,
            color_mask=ImageColorMask(
                back_color=background_color,
                color_mask_image=bg
            )
        ).convert('RGB')
    else:
        qr_img = qr.make_image(fill_color=qr_color, back_color=background_color).convert('RGB')

    # Save QR code to memory
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)

    # Return base64-encoded image
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"
