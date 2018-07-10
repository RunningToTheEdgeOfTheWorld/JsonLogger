# JsonLogger
一个使用起来非常简单的logger, 支持python原生接口
## Required
python3
## Usage
    import logging
    from json_logger import get_json_logger, JsonFormatter

    logger = get_json_logger('JsonLogger')
##### 使用和原生logger相同, 添加一个hanlder
    handler = logging.StreamHandler()
    # 添加一个JsonFormatter
    handler.formatter = JsonFormatter(
        {
           'asctime': '%(asctime)s',
           'level': '%(levelname)s',
           'message':'%(message)s'
        }
    )
    handler.setLevel(logging.INFO)

    logger.addHandler(handler)
##### case 1

    >>> logger.info('HelloWorld')
    {"asctime": "2018-07-10 22:39:36,070", "level": "INFO", "message": {"msg": "HelloWorld"}}

##### case 2
    class Score:
        def __str__(self):
            return 'score: 100'

    player = {
        "name": "Rick",
        "male": True,
        "score_type": [int, float, object],
        "score": Score(),
    }

    >>> logger.info(player)
    {"sctime": "2018-07-10 22:37:04,471", "level": "INFO", "message": {"msg": {"name": "Rick", "male": true, "score_type": ["<class 'int'>", "<class 'float'>", "<class 'object'>"], "score": "score: 100"}}}

##### case 3
    >>> logger.info(man=player)
    {"asctime": "2018-07-10 22:48:36,575", "level": "INFO", "message": {"man": {"name": "Rick", "male": true, "score_type": ["<class 'int'>", "<class 'float'>", "<class 'object'>"], "score": "score: 100"}}}

##### case 4
    try:
        raise RuntimeError()
    except:
        logger.exception() # add key traceback
    {"asctime": "2018-07-10 22:37:44,652", "level": "ERROR", "message": {"traceback": ["Traceback (most recent call last):", "  File \"<stdin>\", line 3, in <module>", "RuntimeError"]}}
