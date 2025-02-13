import os
from typing import Any


def get_current_environment(
    scope: Any, env_var: str = "dev", default: str = "development"
) -> str:
    """
    Get the value of the environment from the context of the stack
        :param scope: The instance of some construct or an app
        :param env_var: The default environment variable name
        :param default: The default value to return if the context is not found
    """
    environment = os.getenv("ENV", env_var)
    env_key = scope.node.try_get_context(environment)

    return env_key.get("environment") if env_key else default
