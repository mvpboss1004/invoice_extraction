from invoice_extraction import InvoiceExtraction
import sys
import os
from optparse import OptionParser
import pandas as pd

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='input', help='输入文件夹，含pdf电子发票', default='./')
    parser.add_option('-o', '--output', dest='output', help='输出各发票字段表格', default='output.xlsx')
    opts, args = parser.parse_args()
    ie = InvoiceExtraction()

    def dirlist(path, allfile): 
        filelist = os.listdir(path) 
        for filename in filelist: 
            filepath = os.path.join(path, filename) 
            if os.path.isdir(filepath): 
                dirlist(filepath, allfile) 
            else: 
                allfile.append(filepath) 
        return allfile 
    files = dirlist(opts.input,[])

    
    df = []
    for file_name in files:
        if file_name.endswith('.pdf'):
            ret = ie.extract_qrcode_info(file_name)
            ret['文件名'] = file_name
            df.append(ret)
    
    pd.DataFrame(df).to_excel(opts.output, index=False)