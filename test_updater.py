import pytest
import discord
from discord.ext import commands
from updater import Updater
from unittest.mock import AsyncMock, MagicMock, patch

@pytest.fixture
def bot():
    return commands.Bot(command_prefix="!")

@pytest.fixture
def cog(bot):
    return Updater(bot)

@pytest.mark.asyncio
async def test_restart_cmd(cog):
    """Test the /update command."""
    interaction = AsyncMock()
    interaction.user.id = next(iter(cog.devs))  # Use a valid developer ID
    interaction.response.send_message = AsyncMock()
    interaction.followup.send = AsyncMock()

    with patch.object(cog, "update_code", return_value={"git_pull": "Already up to date."}), \
         patch.object(cog, "restart_bot") as mock_restart:
        
        await cog.restart_cmd(cog, interaction)
        interaction.response.send_message.assert_called_once()
        interaction.followup.send.assert_called_once()
        mock_restart.assert_not_called()

@pytest.mark.asyncio
async def test_restart_cmd_with_update(cog):
    """Test the /update command when updates are found."""
    interaction = AsyncMock()
    interaction.user.id = next(iter(cog.devs))  # Use a valid developer ID
    interaction.response.send_message = AsyncMock()
    interaction.followup.send = AsyncMock()

    with patch.object(cog, "update_code", return_value={"git_pull": "Updated files."}), \
         patch.object(cog, "restart_bot") as mock_restart:

        await cog.restart_cmd(cog, interaction)
        interaction.response.send_message.assert_called_once()
        interaction.followup.send.assert_called_once()
        mock_restart.assert_called_once()

def test_run_command(cog):
    """Test shell command execution."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="success", returncode=0)
        result = cog.run_command(["echo", "test"])
        assert result == "success"

def test_get_update_channel(cog):
    """Ensure update channel retrieval works correctly."""
    mock_channel = MagicMock()
    cog.bot.get_channel = MagicMock(return_value=mock_channel)
    assert cog.get_update_channel() == mock_channel

@pytest.mark.asyncio
async def test_notify_updates(cog):
    """Test update notifications are sent to the designated channel."""
    mock_channel = AsyncMock()
    cog.bot.get_channel = MagicMock(return_value=mock_channel)

    await cog.notify_updates({"git_pull": "Updated files."})
    mock_channel.send.assert_called_once()
