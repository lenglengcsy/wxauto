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

# 企业微信API模块开发过程记录

1. 设计qywx/api目录结构，包含client.py、message.py、http_client.py等文件，client.py负责API封装，http_client.py统一处理http请求。
2. 实现http_client.py，封装http_get和http_post方法，所有API请求均通过该模块，便于统一异常处理和扩展。
3. 在client.py中实现QywxClient类，支持access_token获取、消息发送、成员userid查询、部门信息查询等功能。
4. 将原utils.py中的成员和部门查询方法合并到QywxClient类，接口更统一，易于维护。
5. 增加API调用的容错处理，遇到错误码时输出详细错误信息，避免程序崩溃。
6. 配置企业微信API可信IP白名单，确保API调用不会因IP限制报错（如60020），相关设置在企业微信管理后台"我的企业-企业可信IP"中完成。
7. 通过config.py集中管理corp_id、corp_secret、agentid等敏感信息，提升安全性和可维护性。
8. 编写test_qywx_send.py等测试脚本，验证API功能的正确性。

---

# 近期重要交互与数据库升级记录

1. 对chat_message表结构进行升级，去除receiver字段，新增msg_id、sender_remark、type、info等字段，结构如下：
   - id（主键）、msg_id（消息id）、sender（发送者）、sender_remark（备注名）、msg_time（时间）、window_name（窗口名）、type（消息类型）、content（内容）、info（原始消息信息）。
2. 同步升级db/crud.py和db/message_service.py，确保写入字段与表结构一致，info字段自动序列化为字符串。
3. 表初始化流程调整为：先DROP TABLE IF EXISTS chat_message，再CREATE，确保结构一致。
4. 遇到ModuleNotFoundError时，建议用python -m db.db_init方式在项目根目录下初始化表结构。
5. 遇到Unknown table 'CHAT_MESSAGE' in information_schema时，需注意表名大小写、数据库连接配置及表是否已成功创建。

---

# 聊天历史记录加载与内存缓存开发过程

1. 需求：程序启动时自动拉取wx/config.py中LISTEN_LIST配置的所有窗口的最近20条聊天记录，并存入内存，便于后续AI上下文拼接。
2. 初步实现：在run.py中实现load_recent_histories函数，遍历LISTEN_LIST，调用db.crud.get_chat_history_by_window_name获取历史消息，存入recent_histories字典。
3. 结构优化：根据项目规划，将历史聊天记录的加载与缓存逻辑迁移到wx/history.py，提供load_recent_histories和get_recent_history接口，内存缓存data为全局变量。
4. 主程序run.py中仅需调用wx.history.load_recent_histories(LISTEN_LIST)，并可通过wx.history.data或get_recent_history(window_name)获取历史消息。
5. 这样实现后，历史消息的加载、缓存、访问逻辑与监听、消息处理等业务解耦，结构更清晰，便于维护和扩展。
