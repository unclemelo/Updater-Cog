import pytest
import discord
from discord.ext import commands
from updater import Updater


@pytest.fixture
def bot():
    """Creates a test bot instance."""
    return commands.Bot(command_prefix="!")


@pytest.fixture
async def cog(bot):
    """Loads the Updater cog into the test bot."""
    cog = Updater(bot)
    await bot.add_cog(cog)
    return cog


def test_run_command():
    """Tests if run_command executes a simple shell command."""
    output = Updater.run_command(["echo", "Hello"])
    assert "Hello" in output


def test_update_code(mocker, cog):
    """Tests the update_code function with mocked subprocess calls."""
    mocker.patch.object(Updater, "run_command", return_value="Already up to date.")
    
    update_results = cog.update_code()
    
    assert "git_pull" in update_results
    assert "pip_install" in update_results
    assert "Already up to date." in update_results["git_pull"]


@pytest.mark.asyncio
async def test_restart_command(mocker, cog, bot):
    """Tests the restart command without actually rebooting."""
    interaction = mocker.MagicMock()
    interaction.user.id = 1234567890  # Replace with a valid developer ID
    interaction.response.send_message = mocker.AsyncMock()

    mocker.patch.object(cog, "update_code", return_value={"git_pull": "Already up to date."})
    mocker.patch.object(cog, "restart_bot")

    await cog.restart_cmd(cog, interaction)

    interaction.response.send_message.assert_called()
    cog.restart_bot.assert_not_called()


@pytest.mark.asyncio
async def test_notify_updates(mocker, cog, bot):
    """Tests sending an update notification message."""
    mock_channel = mocker.MagicMock()
    mock_channel.send = mocker.AsyncMock()

    mocker.patch.object(bot, "get_channel", return_value=mock_channel)

    update_results = {"git_pull": "Updated"}
    await cog.notify_updates(update_results)

    mock_channel.send.assert_called()


if __name__ == "__main__":
    pytest.main()
