# Blog-System
基于 Django + Bootstrap 的个人博客系统
## 关于python版本
建议使用3.10版本，如果不幸使用了3.14以上版本请按照以下流程重新建立一个虚拟环境
退出旧环境（如果当前还激活着）
```
deactivate
```
用 3.10 显式创建新虚拟环境
```
# 把旧环境改名备份（可选）
mv D:\workspace\django22\.venv D:\workspace\django22\.venv.bak
# 找到系统里的 3.10 可执行文件
# 大多数机器上叫 py -3.10，如果提示找不到，把路径写全也行：
# C:\Users\<你>\AppData\Local\Programs\Python\Python310\python.exe
py -3.10 -m venv D:\workspace\django22\.venv
```
激活新环境
```
D:\workspace\django22\.venv\Scripts\Activate.ps1
```
升级 pip
```
python -m pip install -U pip
```
装 mysqlclient
```
pip install mysqlclient==2.2.0
```
把项目其余依赖一次性补回来
```
pip install django pymysql -i https://pypi.tuna.tsinghua.edu.cn/simple
# 如果原来有 requirements.txt，直接
# pip install -r requirements.txt
```
验证驱动
```
python -c "import MySQLdb; print('mysqlclient OK')"
```
继续迁移
```
python manage.py makemigrations
python manage.py migrate
```
