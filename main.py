#coding: utf-8
from invoice_extraction import InvoiceExtraction
import sys
import os
from optparse import OptionParser
import pandas as pd

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='input', help='输入文件夹，含pdf电子发票', default='./')
    parser.add_option('-o', '--output', dest='output', help='输出各发票字段表格', default='output.xlsx')
    parser.add_option('-r', '--recursive', dest='recursive', help='是否递归查找子文件夹中的发票', action='store_true')
    opts, args = parser.parse_args()
    ie = InvoiceExtraction()

    df = []
    for root, folders, files in os.walk(opts.input):
        for file_name in files:
            if file_name.endswith('.pdf'):
                ret = ie.extract_qrcode_info(os.path.join(root,file_name))
                ret['文件名'] = file_name
                df.append(ret)
        if not opts.recursive:
            break
    pd.DataFrame(df).to_excel(opts.output, index=False)