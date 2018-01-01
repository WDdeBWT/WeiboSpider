# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/12/12"

from aip import AipOcr

# """ 你的 APPID AK SK """
APP_ID = '10492378'
API_KEY = 'PeclifhsWLy991bIxA3OC5ab'
SECRET_KEY = '0DdKiWzikvFylgvg5kQqLnZwHVCnU2r9'
FILE_PATH = "F:\\105_aig_1.jpg"

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 定义参数变量
options = {
  'detect_direction': 'true',
  'language_type': 'CHN_ENG',
}

# 调用通用文字识别接口
result = client.basicGeneral(get_file_content(FILE_PATH), options)
print(result)
print("-----")