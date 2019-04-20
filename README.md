# PDF电子发票信息提取
## 1. 字段说明
本程序通过两种方法从PDF电子发票提取信息。  
### 1.1 电子发票左上角的二维码
通过二维码直接读是确保能获取到的，且确保正确，包括以下信息：  
 - 发票代码  
 - 发票号码  
 - 开票日期  
 - 校验码  
 - 金额（不含税）  
 - 销售方纳税人识别号（或有）  

### 1.2 PDF文本
通过将PDF转化为文本并进行正则匹配。虽然在近百张发票上测试过，但是由于不同商家生成的电子发票格式千奇百怪，不保证能获取到。  
 - 开票地
 - 价税合计（小写）
 - 价税合计（大写）
 - 密码区
 - 购买方纳税人识别号

## 2. 安装说明
本程序仅在`MacOS`搭配`python3`上测试过。  
程序依赖包括`zbarlight`、`PyMuPDF`用于二维码识别法，`pdfminer.six`用于PDF文本正则法。然而这三个无法简单地通过`pip`安装。具体安装方法参见：  
 - `zbarlight`：[https://pypi.org/project/zbarlight/](https://pypi.org/project/zbarlight/)  
 - `PyMuPDF`：[https://pypi.org/project/PyMuPDF/](https://pypi.org/project/PyMuPDF/)  
 - `pdfminer`：[https://euske.github.io/pdfminer/index.html](https://euske.github.io/pdfminer/index.html)  
其他依赖通过`pip`安装即可： 

```
pip install pillow pandas
```

## 3. 使用说明
需要提供含PDF电子发票的文件夹路径和输出的excel文件名：

```
python3 main.py -i /path/to/pdf/invoice -o output.xlsx
```

## 4. 使用Docker
因为这个环境配置起来太麻烦，所以我创建了一个Docker方式。   
第一步：build环境 
```
docker image build -t mupdf .
```
第二步：执行本地程序
```
docker container run --rm -it  -v /Users/ron/Documents/docker_images:/code mupdf python3 main.py -i invoice -o output.xlsx
```