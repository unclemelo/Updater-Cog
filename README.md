# Updater-Cog

A Discord bot cog for updating and restarting the bot via slash commands. This cog allows developers to pull updates from GitHub, update dependencies, and restart the bot seamlessly.

## Features
- **GitHub Auto-Update**: Pulls the latest code from GitHub.
- **Dependency Management**: Automatically updates Python dependencies.
- **Restart Functionality**: Restarts the bot after applying updates.
- **Developer-Only Access**: Restricts update commands to specified developers.
- **Error Handling**: Provides detailed error messages for failed updates.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- `discord.py` library
- A bot set up with Discord API
- Git installed

### Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/unclemelo/Updater-Cog
   cd Updater-Cog
   ```
2. Install dependencies:
   ```sh
   python3 -m pip install -r requirements.txt
   ```
3. Add the cog to your bot's main file:
   ```python
   import discord
   from discord.ext import commands
   
   bot = commands.Bot(command_prefix="!")
   
   async def setup():
       await bot.load_extension("updater")
   
   bot.run("YOUR_BOT_TOKEN")
   ```

4. Replace the following placeholders in `updater.py`:
   - **Developer IDs** (`devs = {0}`) → Add your bot admin Discord IDs.
   - **Update Channel ID** (`UPDATE_CHANNEL_ID = 0`) → Replace with the Discord channel ID for update logs.
   - **GitHub Repo Link** in `notify_updates()`.

## Usage

### Commands
| Command  | Description |
|----------|-------------|
| `/update` | Pulls the latest updates from GitHub, updates dependencies, and restarts the bot (Dev-only). |

### Example Workflow
1. Developer executes `/update`.
2. The bot fetches updates from GitHub.
3. Dependencies are updated.
4. The bot announces the update in the specified channel.
5. If updates are found, the bot restarts.

## Contributing
Contributions are welcome! Feel free to submit pull requests to improve this cog, fix issues, or add new features. You can also create other versions of this updater in different languages, such as `updater.js`, `updater.cs`, etc., and submit them to the repository.

## License
This project is licensed under the MIT License.
