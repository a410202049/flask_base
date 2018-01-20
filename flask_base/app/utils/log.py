# coding=utf-8
from colorlog import ColoredFormatter
import logging
import logging.handlers

class FinalLogger(object):

    logger = None

    levels = {"n" : logging.NOTSET,
              "d" : logging.DEBUG,
              "i" : logging.INFO,
              "w" : logging.WARN,
              "e" : logging.ERROR,
              "c" : logging.CRITICAL}

    CONFIG = dict(
        LOG_LEVEL='d',
        LOG_FILE = 'running.log',
        LOG_FILE_MAX_SIZE = 10 * 1024 * 1024,
        LOG_FILE_NUM_BACKUPS = 5,

        ADMINS_EMAIL = None,
        MAIL_USERNAME = None,
        MAIL_SERVER = None,
        MAIL_PASSWORD = None,
        MAIL_PORT = 25,
        EMAIL_ERROR_SUBJECT = 'YourApplication Failed'
    )

    def __init__(self,app):
        if app:
            for k in self.CONFIG.keys():
                if k in app.config:
                    self.CONFIG[k] = app.config[k]

    @staticmethod
    def getLogger():
        if FinalLogger.logger is not None:
            return FinalLogger.logger

        FinalLogger.logger = logging.getLogger()

        #   把log信息输入到文件中
        log_file_handler = logging.handlers.RotatingFileHandler(
            filename = FinalLogger.CONFIG['LOG_FILE'],
            maxBytes = FinalLogger.CONFIG['LOG_FILE_MAX_SIZE'],
            backupCount = FinalLogger.CONFIG['LOG_FILE_NUM_BACKUPS']
        )

        #   在控制台输出log信息
        log_console_handler = logging.StreamHandler()

        #   定义邮件handler
        mail_handler = logging.handlers.SMTPHandler(
            (
                FinalLogger.CONFIG['MAIL_SERVER'],
                FinalLogger.CONFIG['MAIL_PORT']
            ),
            FinalLogger.CONFIG['MAIL_USERNAME'],
            FinalLogger.CONFIG['ADMINS_EMAIL'],
            FinalLogger.CONFIG['EMAIL_ERROR_SUBJECT'],
            (
                FinalLogger.CONFIG['MAIL_USERNAME'],
                FinalLogger.CONFIG['MAIL_PASSWORD']
            )
        )
        mail_handler.setLevel(logging.ERROR)

        # 输出的格式
        formater = logging.Formatter("[%(asctime)s]-[%(filename)s]-[%(funcName)s]-[line %(lineno)d]-[%(levelname)s]-%(message)s")

        # 流文件带颜色输出
        color_formatter = ColoredFormatter(
            "%(log_color)s%(levelname)-8s%(reset)s %(white)s%(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red',
            }
        )

        log_file_handler.setFormatter(formater)
        mail_handler.setFormatter(formater)
        log_console_handler.setFormatter(color_formatter)

        #   添加handler到logger中
        FinalLogger.logger.addHandler(log_file_handler)
        FinalLogger.logger.addHandler(log_console_handler)
        FinalLogger.logger.addHandler(mail_handler)

        #   设置log的级别，默认为debug
        FinalLogger.logger.setLevel(FinalLogger.levels.get(FinalLogger.CONFIG['LOG_LEVEL']))

        #   返回一个logger对象
        return FinalLogger.logger

if __name__ == "__main__":
    logger = FinalLogger.getLogger()
    # debug:debug级输出
    # info：info级输出，重要信息
    # warning：warning级输出，与warn相同，警告信息
    # error：error级输出，错误信息
    # critical ：critical级输出，严重错误信息
    logger.debug("this is a debug msg!")
    logger.info("this is a info msg!")
    logger.warn("this is a warn msg!")
    logger.error("this is a error msg!")
    logger.critical("this is a critical msg!")





