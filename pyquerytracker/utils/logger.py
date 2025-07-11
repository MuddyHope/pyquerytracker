import logging


class QueryLogger:
    @staticmethod
    def get_logger(name: str = "pyquerytracker") -> logging.Logger:
        logger = logging.getLogger(name)

        if not logger.handlers:
            handler = logging.StreamHandler()
            fmt = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(fmt)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

        return logger
