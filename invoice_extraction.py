#coding: utf-8
import fitz
from zbarlight import scan_codes
from io import BytesIO, StringIO
from PIL import Image
from datetime import datetime
from tempfile import NamedTemporaryFile
from pygrok import Grok
import os
import re
class InvoiceExtraction:
    qrcode_keys = [
        ['f0', 'f1', '发票代码', '发票号码', '金额', '开票日期', '校验码', 'f6'],
        ['f0', 'f1', '发票代码', '发票号码', '销售方纳税人识别号', '金额', '开票日期', '校验码'],
    ]

    grok_element = {
        'PASSWD_ZONE': r'(([0-9/+\-\<\>\*]\s?){27}[0-9/+\-\<\>\*]\n){4}',
        'CHECKSUM_KEY': r'校\s*验\s*码:',
        'CHECKSUM': r'(\d{5}\s*){3}\d{5}',
        'DATE_KEY': r'开票日期:',
        'CN_DATE': r'201\d[\s年]*((0[1-9])|(1[0-2]))[\s月]*((0[1-9])|([1-2][0-9])|(3[0-1]))[\s日]*',
        'ORGID_KEY': r'纳税人识别号:',
        'ORGID': r'\w{18}',
        'UPPER_KEY': r'价税合计[（\(]大写[）\)]',
        'UPPER_NUMBER': r'[零壹贰叁肆伍陆柒捌玖拾佰仟万亿整元圆角分\s]+',
        'LOWER_KEY': r'[（\(]小写[）\)]',
        'ADDRTEL_KEY': r'地\s*址\s*、\n?\s*电\s*话:',
        'NAME_KEY': r'名\s*称:',
        'BANKACCOUNT_KEY': r'开户行及账号:',
        'RECEIVER_KEY': r'收\s*款\s*人:',
        'VALIDATOR_KEY': r'复\s*核:',
        'PRINTER_KEY': r'开\s*票\s*人:',
        'LID_KEY': r'发票单号：',
        'LID': r'\w{16}',
        'OID_KEY': r'订单号',
        'OID': r'\w{23}',
    }

    key_field_map = {
        'passwd_zone': '密码区',
        'total_upper': '价税合计(大写)',
        'total_lower': '价税合计(小写)',
        'seller_name': '购买方名称',
        'seller_id': '销售方纳税人识别号',
        'seller_addr_tel': '销售方地址、电话',
        'seller_bank_account': '销售方开户行及账号',
        'receiver': '收款人',
        'validator': '复核',
        'printer': '开票人',
    }

    regex_element = {
        '开票地': '(?P<field>.*增值税电子((普通)|(专用))发票)',
        '价税合计(小写)': '[（\(]小写[）\)](.*\n)*[¥￥](?P<field>\d+\.\d+)',
        '密码区': '密码区(.*\n)*(?P<field>(([0-9/+\-\<\>\*]\s?){27}[0-9/+\-\<\>\*]\n){4})'
    }

    def __init__(self):
        f = NamedTemporaryFile(delete=False)
        self._tmp_txt = f.name
        f.close()

        self._patterns = {}
        for key in self.regex_element:
            self._patterns[key] = re.compile(self.regex_element[key], re.M)

    def extract_qrcode_info(self, file_path):
        try:
            doc = fitz.open(file_path)
            png = doc[0].getPixmap(matrix=fitz.Matrix(2,2), alpha=False).getPNGdata()
            img = Image.open(BytesIO(png))
            values = filter(None, scan_codes(['qrcode'], img)[0].decode().split(','))
            for keys in self.qrcode_keys:
                ret = dict(zip(keys, values))
                try:
                    ret['金额'] = eval(ret['金额'])
                    ret['开票日期'] = datetime.strptime(ret['开票日期'], '%Y%m%d').date()
                    break
                except:
                    pass
            return ret
        except Exception as e:
            print(e)
            return {}
    
    def extract_pdf_info(self, file_path):
        os.system("pdf2txt.py '%s' -o '%s'"%(file_path, self._tmp_txt))
        with open(self._tmp_txt) as f:
            text = '\n'.join(list(filter(None, [line.strip() for line in f.read().split('\n')])))

        ret = {}
        for key in self._patterns:
            mt = self._patterns[key].match(text)
            if mt:
                ret[key] = mt.groupdict()['field']
        return ret