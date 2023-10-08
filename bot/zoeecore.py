import logging
import signal
from pathlib import Path

import asyncpg
import discord
from aiohttp import ClientSession
from cogs import EXTENSIONS, VERSION
from discord.ext import commands

_fsw = True
try:
    from watchfiles import awatch
except ImportError:
    _fsw = False


class Zoee(commands.Bot):
    """Zoeeeee"""

    def __init__(
        self,
        intents: discord.Intents,
        session: ClientSession,
        pool: asyncpg.Pool,
        dev_mode: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="for some eggs to hatch!"
            ),
            command_prefix="z>",
            help_command=None,
            intents=intents,
            *args,
            **kwargs,
        )
        self.logger = logging.getLogger("zoee")
        self.session = session
        self.pool = pool
        self.version = str(VERSION)
        self._dev_mode = dev_mode

        # Pulled from Kumiko and Catherine-Chan

    async def fs_watcher(self) -> None:
        cogs_path = Path(__file__).parent.joinpath("cogs")
        async for changes in awatch(cogs_path):
            changes_list = list(changes)[0]
            if changes_list[0].modified == 2:
                reload_file = Path(changes_list[1])
                self.logger.info(f"Reloading extension: {reload_file.name[:-3]}")
                await self.reload_extension(f"cogs.{reload_file.name[:-3]}")

    async def setup_hook(self) -> None:
        def stop():
            self.loop.create_task(self.close())

        self.loop.add_signal_handler(signal.SIGTERM, stop)
        self.loop.add_signal_handler(signal.SIGINT, stop)

        for extension in EXTENSIONS:
            await self.load_extension(extension)

        if self._dev_mode is True and _fsw is True:
            self.logger.info("Dev mode is enabled. Loading Jishaku and FSWatcher")
            await self.load_extension("jishaku")
            self.loop.create_task(self.fs_watcher())

    async def on_ready(self):
        if not hasattr(self, "uptime"):
            self.uptime = discord.utils.utcnow()

        curr_user = None if self.user is None else self.user.name
        self.logger.info(f"{curr_user} is fully ready!")
