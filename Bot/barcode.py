import barcode
from barcode.writer import ImageWriter

list_barcodes = ['ean13', 'ean8', 'isbn10', 'isbn13', 'issn', 'pzn', 'upc', 'upca']

def gen(num : int, code : str): 
    """
    Генерирует штрихкод на основе списка штрихкодов и сохраняет его в PNG.
    """
    bar = barcode.get(list_barcodes[num], str(code), ImageWriter('PNG'))
    bar.save(f'code{list_barcodes[num]}')
