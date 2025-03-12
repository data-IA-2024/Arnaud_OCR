import ocr

def test_invoice1():
    invoice = ocr.ocr("invoice-OK.png")
    assert invoice['status']=="OK"

def test_invoice2():
    invoice = ocr.ocr("invoice-BAD.png")
    assert invoice['status']!="OK"