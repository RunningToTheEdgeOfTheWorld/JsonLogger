# !/usr/bin/env python
__author__ = 'RunningToTheEdgeOfTheWorld'
__time__ = '2018/7/10'

import sys
import logging
import simplejson as json
import traceback


class JsonLogger(logging.Logger):
    def __init__(self, *args, **kwargs):
        self.__formatter = None
        super().__init__(*args, **kwargs)
        self.propagate = False

    def debug(self, msg=None, **kwargs):
        msg, _args, _kwargs = self._parse_arge(msg, **kwargs)
        return super().debug(msg, *_args, **_kwargs)

    def info(self, msg=None, **kwargs):
        msg, _args, _kwargs = self._parse_arge(msg, **kwargs)
        return super().info(msg, *_args, **_kwargs)

    def warning(self, msg=None, **kwargs):
        msg, _args, _kwargs = self._parse_arge(msg, **kwargs)
        return super().warning(msg, *_args, **_kwargs)

    def error(self, msg=None, **kwargs):
        msg, _args, _kwargs = self._parse_arge(msg, **kwargs)
        return super().error(msg, *_args, **_kwargs)

    def exception(self, msg=None, **kwargs):
        # traceback.print_exc()
        kwargs['traceback'] = traceback.format_exc().splitlines()
        msg, _args, _kwargs = self._parse_arge(msg, **kwargs)
        return super().error(msg, *_args, **_kwargs)

    def critical(self, msg=None, **kwargs):
        msg, _args, _kwargs = self._parse_arge(msg, **kwargs)
        return super().critical(msg, *_args, **_kwargs)

    @staticmethod
    def _parse_arge(msg, **kwargs):
        if 'msg' in kwargs:
            raise ValueError('msg is not allowed in kwargs')
        _args = kwargs.pop('_args', [])
        _kwargs = kwargs.pop('_kwargs', {})
        if msg is not None:
            kwargs['msg'] = msg
        msg = format_msg(kwargs)
        return msg, _args, _kwargs

    def addHandler(self, hdlr):
        if hasattr(self, 'formatter') and not isinstance(hdlr.formatter, JsonFormatter):
            raise ValueError('Please use JsonFormatter!')
        super().addHandler(hdlr)


logger = JsonLogger("root")
json_manager = logging.Manager(logger)
json_manager.loggerClass = JsonLogger

JsonLogger.manager = json_manager
JsonLogger.root = logger


def get_json_logger(name=None, default=True):
    if default:
        logger.name = name
        return logger
    else:
        return JsonLogger.manager.getLogger(name)


def format_msg(msg):
    """
    transfor msg dict jsonable dict
    :param: msg
    :return: json
    """
    def _format_msg(_m):
        if isinstance(_m, (str, int, float)):
            return _m
        elif isinstance(_m, bytes):
            return _m.decode()
        elif isinstance(_m, dict):
            return {_format_msg(k): _format_msg(v) for k, v in _m.items()}
        elif isinstance(_m, (tuple, list)):
            return [_format_msg(i) for i in _m]
        else:
            try:
                return str(_m)
            except:
                raise ValueError("Not allowed object, object must have __str__ method!")

    return json.dumps(_format_msg(msg), ensure_ascii=False)


class JsonFormatter(logging.Formatter):
    def __init__(self, fmt_dict: dict=None, datefmt=None, style='%'):
        if not fmt_dict:
            fmt_dict = {
                'logger': '%(name)s',
                'asctime': '%(asctime)s',
                'level': '%(levelname)s',
                'message': '%(message)s',
            }
        if not isinstance(fmt_dict, dict):
            raise ValueError('fmt_dict must be a dict')

        fmt = format_msg(fmt_dict).replace('"%(message)s"', '%(message)s')
        super().__init__(fmt, datefmt, style)


_default_handler = logging.StreamHandler(stream=sys.stdout)
_default_handler.formatter = JsonFormatter()
logger.addHandler(_default_handler)
logger.setLevel(logging.INFO)
