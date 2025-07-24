import logging


def init_log():  # 初始化日志
    logging.basicConfig(
        level=logging.INFO,  # 设置日志级别（低于此级别的日志将被忽略）
        format="%(asctime)s - %(levelname)s - %(message)s - %(filename)s - %(lineno)d",  # 日志格式
        filemode="a"  # 写入模式：'w'（覆盖）或 'a'（追加）
    )
    return logging
