# 数据库模块开发过程记录

1. 设计db模块目录结构，包含config.py、connection.py、models.py、crud.py、utils.py等文件。
2. 首先实现config.py，定义MySQL数据库连接参数。
3. 实现connection.py，封装获取和关闭数据库连接的函数。
4. 实现utils.py，添加数据库操作异常处理装饰器。
5. 将数据库连接库由pymysql更换为mysqlclient（MySQLdb），并适配相关代码。
6. 在test/db目录下新建test_connection.py，添加数据库连接的单元测试用例。

---

# 聊天监听模块开发过程记录

1. 设计wx模块监听消息的整体思路，明确使用wxautox库，接口风格参考wxauto。
2. 实现wx/listener.py，封装MessageListener类，支持添加监听对象、获取新消息、持续监听。
3. 优化run.py，作为项目入口，调用MessageListener并通过回调处理消息。
4. 将监听对象配置从run.py迁移到wx/config.py，提升可维护性和优雅性。
5. 在test目录下新建wx子文件夹，为后续wx相关功能编写测试用例做准备。
