import logging

from config import Config


class AppLogger:

    def __init__(self, level: int, name: str) -> None:
        self.default_handler = logging.StreamHandler()
        self.default_handler.setFormatter(
            logging.Formatter("[%(asctime)s] %(levelname)s | %(module)s | %(message)s")
        )
        self.level = level
        self.name = name

    def create_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.name)

        if not self.has_level_handler(logger):
            logger.addHandler(self.default_handler)

        logger.setLevel(self.level)

        return logger

    def has_level_handler(self, logger: logging.Logger) -> bool:
        """Check if there is a handler in the logging chain that will handle the
        given logger's :meth:`effective level <~logging.Logger.getEffectiveLevel>`.
        """
        level = logger.getEffectiveLevel()
        current = logger

        while current:
            if any(handler.level <= level for handler in current.handlers):
                return True

            if not current.propagate:
                break

            current = current.parent  # type: ignore

        return False


logger = AppLogger(level=Config.LOG.LEVEL, name="Task App").create_logger()
