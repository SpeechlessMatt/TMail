# 临时邮箱注册 TMail
本项目引用chacuo.net的接口编写python库，包含loguru库用于日志记录

## :books: 使用方法

### 下载库
```bash
git clone 
```
### 引用方法
`from TMail import TMail`
对于临时收件箱，该库主要有以下方法：
- **get_account()**: 连接邮箱服务器，申请临时邮箱地址
- **get_inbox()**: 获取收件箱，返回一个列表/字典
 - arg: 
  - （可选）detail=**bool** False则返回一个列表，仅包含列表，否则返回包含status_code,num的字典

- **read_mail()**: 读取邮件
 - arg:
  - MID=**(str)** 从get_inbox()返回值中获得MID，通过MID读取邮件详细信息
 - return:
  - turple(状态码，邮件简介，邮件正文) // turple(str,str,str)

- **delete_mail()**: 删除邮件，功能暂未完善...
 - arg:
  - MID=**(str)** 参考read_mail()
 - return:
  - bool 删除是否成功

> **注意：**
> 本库使用[**loguru**](https://github.com/Delgan/loguru/blob/main)日志处理库，可以在主程序头部增加如下代码以获得日志输出
```python
import sys
from loguru import logger
logger.remove()
# 日志级别详情参考loguru库 这里最低级别为INFO
logger.add(sys.stderr, level="DEBUG") 
```

### 简单实例
```python
from TMail import TMail
import time
if __name__ == '__main__':
    tm = TMail()
    name = tm.get_account()
    print(name)
    while True:
        email_list = tm.get_email_list()
        print(email_list)
        if len(email_list) != 0:
            a = input("MID:")
            print(tm.read_mail(a))
        for i in range(0, 10):
            print(f"\r                                {10-i}秒后自动刷新...", end="", flush=True)
            time.sleep(1)
        print("\r                              \n")
```
## 目前阶段
暂未上传到pip