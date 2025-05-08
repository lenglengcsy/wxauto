## Source Structure

### wx
通过wxauto库，监听指定用户或者群的消息，通过数据库模块，发送给云端的MySQL数据库

### llm
根据bot接收到的内容，调用大语言模型，并将结果返回给bot

#### prompt
这个目录下用于配置各种prompt

### db
MySQL数据库访问模块

```
db/
├── __init__.py
├── config.py         # 数据库配置文件（如连接参数等）
├── connection.py     # 数据库连接管理
├── db_init.py        # 数据库和表格初始化脚本
├── models.py         # 数据表结构定义（如ORM模型，可选）
├── crud.py           # 数据的增删改查操作封装
└── utils.py          # 其他数据库相关的工具函数
```

#### 数据库封装
封装基本的数据库访问功能，包括数据库配置填写，数据库连接，数据的增删改查等

### test
各个模块的测试用例会被放在这个文件夹内。

```
test/
└── db/
    └── test_connection.py   # 数据库连接相关测试用例
```

### doc
记录一些文档

- procedure.md  记录用户和cursor的简要交互过程
- proj.md       项目结构和说明






