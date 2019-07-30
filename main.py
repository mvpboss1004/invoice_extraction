#coding: utf-8
from invoice_extraction import InvoiceExtraction
import sys
import os
from optparse import OptionParser
import pandas as pd
from progressbar import progressbar

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='input', help='输入文件夹，含pdf电子发票', default='./')
    parser.add_option('-o', '--output', dest='output', help='输出各发票字段表格', default='output.xlsx')
    parser.add_option('-r', '--recursive', dest='recursive', help='是否递归查找子文件夹中的发票', action='store_true')
    parser.add_option('-n', '--normalize', dest='normalize', help='是否重命名发票，格式：[发票号码]_[价税合计（小写）].pdf', action='store_true')
    opts, args = parser.parse_args()
    ie = InvoiceExtraction()

    df = []
    for root, folders, files in os.walk(opts.input):
        for file_name in progressbar(files):
            if file_name.endswith('.pdf'):
                src_pdf = os.path.join(root, file_name)
                ret = ie.extract(src_pdf)
                if opts.normalize and '发票号码' in ret and '价税合计(小写)' in ret:
                    ret['文件名'] = '%s_%s.pdf'%(ret['发票号码'], ret['价税合计(小写)'])
                    dst_pdf = os.path.join(root, ret['文件名'])
                    os.rename(src_pdf, dst_pdf)
                df.append(ret)
        if not opts.recursive:
            break
    pd.DataFrame(df).to_excel(opts.output, index=False)