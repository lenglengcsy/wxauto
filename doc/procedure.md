# 数据库模块开发过程记录

1. 设计db模块目录结构，包含config.py、connection.py、models.py、crud.py、utils.py等文件。
2. 首先实现config.py，定义MySQL数据库连接参数。
3. 实现connection.py，封装获取和关闭数据库连接的函数。
4. 实现utils.py，添加数据库操作异常处理装饰器。
5. 将数据库连接库由pymysql更换为mysqlclient（MySQLdb），并适配相关代码。
6. 在test/db目录下新建test_connection.py，添加数据库连接的单元测试用例。
