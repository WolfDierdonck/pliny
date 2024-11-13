from datetime import datetime
from enum import Enum
from typing import Literal

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class Colors:
    LIGHT_BLUE = "\033[96m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    PURPLE = "\033[95m"
    RESET = "\033[0m"


class Component(Enum):
    DATABASE = (Colors.GREEN, "Database")
    DATASOURCE = (Colors.CYAN, "Datasource")
    CORE = (Colors.PURPLE, "Core")


class Logger:
    def __init__(self, name: str = "app") -> None:
        self.name = name

    def _log(self, level: LogLevel, message: str, component: Component) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        color = component.value[0]
        component_name = component.value[1]

        print(f"{color}{timestamp} [{component_name}] {level}:{Colors.RESET} {message}")

    def debug(self, message: str, component: Component) -> None:
        self._log("DEBUG", message, component)

    def info(self, message: str, component: Component) -> None:
        self._log("INFO", message, component)

    def warning(self, message: str, component: Component) -> None:
        self._log("WARNING", message, component)

    def error(self, message: str, component: Component) -> None:
        self._log("ERROR", message, component)
