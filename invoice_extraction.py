import fitz
from zbarlight import scan_codes
from io import BytesIO
from PIL import Image
from datetime import datetime

class InvoiceExtraction:
    qrcode_keys = [
        ['f0', 'f1', '发票代码', '发票号码', '价税合计（小写）', '开票日期', '校验码', 'f6'],
        ['f0', 'f1', '发票代码', '发票号码', '销售方纳税人识别号', '价税合计（小写）', '开票日期', '校验码'],
    ]

    def extract_qrcode_info(self, file_path):
        try:
            doc = fitz.open(file_path)
            png = doc[0].getPixmap(matrix=fitz.Matrix(2,2), alpha=False).getPNGdata()
            img = Image.open(BytesIO(png))
            values = scan_codes(['qrcode'], img)[0].decode().split(',')
            for keys in self.qrcode_keys:
                ret = dict(zip(keys, values))
                try:
                    ret['价税合计（小写）'] = eval(ret['价税合计（小写）'])
                    ret['开票日期'] = datetime.strptime(ret['开票日期'], '%Y%m%d').date()
                    break
                except:
                    pass
            return ret
        except Exception as e:
            print(e)
            return {}