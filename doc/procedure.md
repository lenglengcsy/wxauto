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

---

# 近期重要交互与数据库升级记录

1. 对chat_message表结构进行升级，去除receiver字段，新增msg_id、sender_remark、type、info等字段，结构如下：
   - id（主键）、msg_id（消息id）、sender（发送者）、sender_remark（备注名）、msg_time（时间）、window_name（窗口名）、type（消息类型）、content（内容）、info（原始消息信息）。
2. 同步升级db/crud.py和db/message_service.py，确保写入字段与表结构一致，info字段自动序列化为字符串。
3. 表初始化流程调整为：先DROP TABLE IF EXISTS chat_message，再CREATE，确保结构一致。
4. 遇到ModuleNotFoundError时，建议用python -m db.db_init方式在项目根目录下初始化表结构。
5. 遇到Unknown table 'CHAT_MESSAGE' in information_schema时，需注意表名大小写、数据库连接配置及表是否已成功创建。
