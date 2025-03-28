import segno

def qr(text: str):
    """
    Генерирует qr код из текста
    """
    segno.make(text).save('qr.png', scale=8 )
