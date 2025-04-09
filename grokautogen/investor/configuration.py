"""
Configuration Management Module

This module provides functionality for managing application configurations,
including reading, writing, updating, and converting configurations to JSON format.

Classes:
    - PromptSpecification: Represents the configuration for a prompt specification.
    - APISpecification: Defines the configuration for an API.
    - Configuration: Manages application settings, including prompts and API keys.

Usage:
    This module is designed to handle configuration files for the application, ensuring
    they are validated and serialized correctly. It supports merging new configurations
    with existing ones and provides a default configuration for initialization.

Example:
    from pathlib import Path
    from configuration import Configuration

    # Load a configuration
    config = Configuration.read(Path("config.json"))

    # Update the configuration
    new_config = Configuration.default()
    new_config.update(Path("config.json"))

    # Convert configuration to JSON
    json_output = new_config.to_json()
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional, Dict
from pathlib import Path
from json import dumps

type Name = str
type AgentName = Name
type Version = str
type Prompt = str
type Version = str
type URL = str
type Key = str


class PromptSpecification(BaseSettings):
    """
    Represents the configuration for a prompt specification.

    Attributes:
        version (Version): The version of the prompt specification.
        prompt (Prompt): The prompt details associated with the specification.
    """

    version: Version
    prompt: Prompt


class APISpecification(BaseSettings):
    """
    APISpecification defines the configuration for an API.

    Attributes:
        model (Name): The name of the model to be used in the API.
        key (Key): The authentication key required to access the API.
        version (Optional[Version]): The version of the API. This is optional.
        deployment (Optional[Name]): The deployment name or environment for the API. This is optional.
        endpoint (Optional[URL]): The URL endpoint of the API. This is optional.
    """

    model: Name
    key: Key
    version: Optional[Version] = None
    deployment: Optional[Name] = None
    endpoint: Optional[URL] = None


class Configuration(BaseSettings):
    """
    Configuration class for managing application settings.

    Attributes:
        prompts (Optional[Dict[AgentName, PromptSpecification]]):
            A dictionary mapping agent names to their respective
            prompt specifications. Defaults to an empty dictionary.
        keys (Dict[Name, APISpecification]):
            A dictionary mapping names to API specifications. Defaults
            to an empty dictionary.
    """

    prompts: Optional[Dict[AgentName, PromptSpecification]] = Field(
        default_factory=dict
    )
    keys: Dict[Name, APISpecification] = Field(default_factory=dict)

    @classmethod
    def read(cls, path: Path) -> "Configuration":
        """
        Reads and validates a configuration file from the specified path.

        Args:
            path (Path): The file path to the configuration file.

        Returns:
            Configuration: The validated configuration object.

        Raises:
            FileNotFoundError: If the configuration file is not found at
                the specified path.
            RuntimeError: If there is an error while reading or validating
                the configuration file.
        """
        try:
            with path.open("r") as file:
                configuration = file.read()
            return cls.model_validate_json(configuration)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found at {path}")
        except Exception as e:
            raise RuntimeError(f"Failed to read configuration file: {e}") from e

    def write(self, path: Path) -> None:
        """
        Writes the configuration to the specified file path in JSON format.

        Args:
            path (Path): The file path where the configuration will be written.

        Raises:
            ValueError: If the configuration object is invalid.
            IOError: If there is an error writing to the file.
        """
        try:
            self.model_validate(obj=self)
            if not path.parent.exists():
                path.parent.mkdir(parents=True, exist_ok=True)
            if not path.suffix == ".json":
                raise ValueError(
                    f"Invalid file extension: {path.suffix}. Expected .json"
                )
            path.write_text(self.model_dump_json(indent=4))
        except ValueError as e:
            raise ValueError(f"Invalid configuration: {e}") from e
        except IOError as e:
            raise IOError(f"Failed to write configuration to {path}: {e}") from e

    def update(self, path: Path) -> None:
        """
        Updates the configuration file at the given path by merging it with
        the current configuration object.

        Args:
            path (Path): The file path to the configuration file.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If the existing or new configuration is invalid.
            IOError: If there is an error reading or writing to the file.
        """
        try:
            if not path.exists():
                raise FileNotFoundError(f"Configuration file not found at {path}")

            existing_config: Configuration = self.read(path)
            updated_config: Configuration = existing_config.model_copy(
                update=self.model_dump()
            )
            updated_config.model_validate(obj=updated_config)
            updated_config.write(path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Configuration file not found: {e}") from e
        except ValueError as e:
            raise ValueError(f"Invalid configuration: {e}") from e
        except IOError as e:
            raise IOError(f"Failed to update configuration at {path}: {e}") from e

    @classmethod
    def default(cls) -> "Configuration":
        """
        Return the default configuration.
        """
        return cls(
            prompts={
                "investment_advisor": PromptSpecification(
                    version="2025-04-06",
                    prompt="""You are the face of the investment team.

You look for investment opportunities based on a client's requirements.
You make seven recommendations. Your recommendations must contain
relevant tickers. You depend on the Portfolio Manager to cut down the
investments to four.""",
                ),
                "portfolio_helper": PromptSpecification(
                    version="2025-04-06",
                    prompt="""You are the investment team's back office support.

You help the Portfolio Manager understand what the client's investment
profile looks like.""",
                ),
                "portfolio_manager": PromptSpecification(
                    version="2025-04-06",
                    prompt="""You are the Portfolio Manager.

You verify that a client's investments fit in with their investment
profile. You make investment recommendations based on the input of the
Investment Advisor and Portfolio Helper. You respond with 'APPROVE' if
the investment is suitable for the client's portfolio.""",
                ),
            },
            keys={
                "openai": APISpecification(
                    model="gpt-4",
                    key="<OPENAI_API_KEY>",
                    version="2025-04-06",
                    deployment=None,
                    endpoint=None,
                ),
            },
        )

    def to_json(self, indent: int = 4) -> str:
        """
        Convert the configuration to JSON format.

        Args:
            indent (int): The number of spaces to use for indentation in
                the JSON output. Defaults to 4.

        Returns:
            str: The JSON representation of the configuration.

        Raises:
            ValueError: If the configuration object is invalid or cannot
                be serialized.
        """
        try:
            self.model_validate(obj=self)
            return dumps(self.model_dump(), indent=indent)
        except ValueError as e:
            raise ValueError(f"Invalid configuration: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to convert configuration to JSON: {e}") from e


# if __name__ == "__main__":
#     config: Configuration = Configuration.default()
#     print(config.to_json())
#     print(config.prompts["investment_advisor"].prompt)
