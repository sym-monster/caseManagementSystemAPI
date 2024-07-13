import pandas as pd
import pymysql

# 将 pymysql 设为 MySQLdb 的替代品
pymysql.install_as_MySQLdb()

# 然后创建你的 engine 和 connection
import sqlalchemy as sa

# 读取 CSV 文件
df = pd.read_csv('./cities.csv')

# 创建数据库连接（使用 SQLAlchemy）
engine = sa.create_engine('mysql://sym:100200@117.50.199.3:3306/case_management_system')

# 将 DataFrame 导入到数据库中
df.to_sql('regions', con=engine, if_exists='append', index=False)