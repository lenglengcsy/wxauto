# coze平台配置文件
# 请根据实际情况填写API Key、Bot ID等参数

COZE_API_KEY = "pat_ZkcWZVF8qgXtgs4T8WZzqYeEcXx5t5z6iNS89O5ZFfyevfe5QxMg75TSlzi1wbKR"
COZE_BOT_ID = "7500830770844942351"
COZE_API_BASE_URL = "https://api.coze.cn"

# pat_ZkcWZVF8qgXtgs4T8WZzqYeEcXx5t5z6iNS89O5ZFfyevfe5QxMg75TSlzi1wbKR

def get_coze_config():
    """获取coze平台配置信息"""
    return {
        "api_key": COZE_API_KEY,
        "bot_id": COZE_BOT_ID,
        "base_url": COZE_API_BASE_URL,
    }
