# url的格式為：數據庫的協議：//用戶名：密碼@ip地址：端口號（默認可以不寫）/數據庫名
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:joe94113@127.0.0.1:3306/flask"
# 動態追踪數據庫的修改. 性能不好. 且未來版本中會移除. 目前只是為了解決控制台的提示才寫的
SQLALCHEMY_TRACK_MODIFICATIONS = False