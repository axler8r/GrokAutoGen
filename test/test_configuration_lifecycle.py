import pytest
from pathlib import Path
from grokautogen.invest.configuration import Configuration, APISpecification


@pytest.fixture
def default_config() -> Configuration:
    """Fixture to provide the default configuration."""
    return Configuration.default()


def test_configuration_lifecycle(tmp_path, default_config) -> None:
    """
    Test the full lifecycle of the configuration system:
    - Write the configuration to a temporary file.
    - Read the configuration back.
    - Update the configuration.
    - Validate the changes.
    """
    # Write the configuration to a temporary file
    config_path: Path = tmp_path / "config.json"
    default_config.write(config_path)
    assert config_path.exists()

    # Read the configuration back
    loaded_config: Configuration = Configuration.read(config_path)
    assert loaded_config.prompts == default_config.prompts
    assert loaded_config.keys == default_config.keys

    # Update the configuration
    loaded_config.keys["new_api"] = APISpecification(
        model="new-model",
        key="new-key",
        version="2025-04-07",
    )
    loaded_config.update(config_path)

    # Validate the updated configuration
    updated_config: Configuration = Configuration.read(config_path)
    assert "new_api" in updated_config.keys
    assert updated_config.keys["new_api"].model == "new-model"


def test_invalid_configuration_handling(tmp_path) -> None:
    """
    Test handling of invalid configuration scenarios:
    - Reading from a nonexistent file.
    - Writing to an invalid path.
    """
    # Test reading from a nonexistent file
    invalid_path: Path = tmp_path / "nonexistent.json"
    with pytest.raises(FileNotFoundError):
        Configuration.read(invalid_path)

    # Test writing to an invalid path
    invalid_write_path = Path("/invalid_path/config.json")
    config: Configuration = Configuration.default()
    with pytest.raises(IOError):
        config.write(invalid_write_path)
