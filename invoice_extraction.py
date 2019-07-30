#coding: utf-8
import fitz
from zbarlight import scan_codes
from io import BytesIO
from PIL import Image
from datetime import datetime
import os
import re
from subprocess import check_output

class InvoiceExtraction:
    qrcode_keys = [
        ['f0', 'f1', '发票代码', '发票号码', '金额', '开票日期', '校验码', 'f6'],
        ['f0', 'f1', '发票代码', '发票号码', '销售方纳税人识别号', '金额', '开票日期', '密码区'],
    ]

    regex_element = {
        '开票地': re.compile(r'(?P<field>.*(增值税)?电子((普通)|(专用))发票)'),
        '价税合计(小写)': re.compile(r'[\(（]小写[\)）](.*\n)*?[¥￥]?\s?(?P<field>\d+\.\d+)', re.M),
        '密码区': re.compile(r'(?P<field>((([0-9/+\-\<\>\*]\s?){26,27}[0-9/+\-\<\>\*]\n){4})|((([0-9A-Za-z]\s?){21}([0-9A-Za-z]\s?)\n){3}))', re.M),
        '价税合计(大写)': re.compile(r'(?P<field>[壹贰叁肆伍陆柒捌玖拾]\s?[零壹贰叁肆伍陆柒捌玖拾佰仟万亿整元圆角分\s]+[整元圆角分])'),
        '购买方纳税人识别号': re.compile(r'纳税人识别号:\n(.*\n)*?(?P<field>[0-9a-zA-Z]{18})', re.M)
    }

    def extract_qrcode_info(self, file_path):
        for zoom in range(1,5):
            try:
                doc = fitz.open(file_path)
                png = doc[0].getPixmap(matrix=fitz.Matrix(1<<zoom,1<<zoom), alpha=False).getPNGdata()
                img = Image.open(BytesIO(png))
                values = list(filter(None, scan_codes(['qrcode'], img)[0].decode().split(',')))
                for keys in self.qrcode_keys:
                    ret = dict(zip(keys, values))
                    try:
                        ret['金额'] = eval(ret['金额'])
                        ret['开票日期'] = datetime.strptime(ret['开票日期'], '%Y%m%d').date()
                    except:
                        pass
                    else:
                        break
                for key in ['f0', 'f1', 'f6']:
                    ret.pop(key, None)
            except:
                pass
            else:
                break
        else:
            print('Read QRcode failed')
            ret = {}
        return ret
    
    def extract_pdf_info(self, file_path):
        try:
            text = check_output(['pdf2txt.py', file_path]).decode('utf-8').replace('\n\n','\n').strip()
            ret = {}
            for key in self.regex_element:
                mt = self.regex_element[key].search(text)
                if mt:
                    ret[key] = mt.groupdict()['field']
            ret['价税合计(小写)'] = eval(ret.get('价税合计(小写)','None'))
            ret['密码区'] = ret.get('密码区','').replace(' ','').replace('\n','')
            ret['价税合计(大写)'] = ret.get('价税合计(大写)','').replace(' ','')
            return ret
        except Exception as e:
            print(e)
            return {}

    def extract(self, file_path):
        ret = dict(self.extract_pdf_info(file_path), **self.extract_qrcode_info(file_path))
        ret['文件名'] = os.path.split(file_path)[1]
        return ret