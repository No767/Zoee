# Zoee

A quick (and somewhat advanced) template for how a proper slash command bot should be for dpy. Hybrid command version coming soon.

Included:

- R. Danny styled Paginator that works with interactions
- Subclassed `discord.ui.View` with built-in `interaction_check` (more coming soon)
- Basic slash commands
- Ready-to-go asyncpg defaults
- uvloop for performance (only on linux/macos)
- Best practices and styles influenced by [Kumiko](https://github.com/No767/Kumiko), [Catherine-Chan](https://github.com/No767/Catherine-Chan) and most notably, [R. Danny](https://github.com/Rapptz/RoboDanny)

## Getting Started

Slash commands are commands that need to be sent to Discord.
discord.py handles this via a process called syncing. Now, syncing makes
an call to the API and people often automate this process, and **auto syncing is bad**.
So that's why this template manually handles it via an sync command (spefically, [Umbra's Sync Command](https://about.abstractumbra.dev/discord.py/2023/01/29/sync-command-example.html)). Read more on Umbra's sync command to understand how it works.

<details>
    <summary>If you want to know why auto syncing is bad</summary>

Auto-syncing, which is the practice of using `bot.tree.sync()` in a `setup_hook`,
is extremely bad practice. Why? Even single time you sync, you send an API request
to Discord. Within the dpy examples, it is done so in order to provide the slash 
commands in the ui for the user. It's done so folks starting out won't complain
about "why is my slash commands not showing up?" (and also btw the examples are
really good for basic slash command examples).

Now the implications of doing so is quite huge. There are two main points: 

1. **Auto-syncing incurs heavy ratelimits (429 errors).** Now usually for folks starting off,they will Ctrl+C their bot to reload extensions, and now that can lead to ratelimits. Do it too much and **expect to get IP banned by Discord**. Getting ratelimited isn't a good thing soit's best to do what you can do to prevent it from happening (dpy pretty much handles it for you). 

2. **Lack of control.**. Say I have my bot auto syncing, and then oops I accidently synced both globally and to my guild, resulting in duplicate commands. Now I want to get rid of them, but I basically can't because all of the syncing is done automatically. This is what auto-syncing leads to. Now let's say I added Umbra's sync command, and all I need to do to fix this is to run `z>sync ^` and boom, the duplicate commands are removed. Point is, there is an heavyopportunity cost that you have to take. Either auto sync + gain convenience or lose control over how you sync. The second option seems less risker in general.

Now you don't need to manually sync everysingle time you change your code, but the tdlr is todo it when you change or added command + option names and/or descriptions, change or added the type of the param, and when you add/modify permissions. (You can find more details about this in the [app command guide](https://github.com/Rapptz/discord.py/pull/9557) being written by Nanika, and the finer details can be also found in `?tag whensync` in the [offical discord.py server](https://discord.com/invite/r3sSKJJ). That's it.

~ Noelle
</details>

Essentially, this bot is a pure slash command bot expect two prefixed commands:
the syncing command and a extension reloader command, useful in production to 
avoid downtime and hot reload them. This template also includes an automatic extension
reloader written by me that is implemented on Kumiko, Catherine-Chan and Xelt.py.

### Instructions (for dev. prod is diff)

You must have these installed:

- Poetry
- Python
- Git
- PostgreSQL

In order to run pg in a docker container, spin up the docker compose file
located in the root of the repo (`sudo docker compose up -d`).

1. Clone the repo or use it as a template.
2. Copy over the ENV file template to the `bot` directory

    ```bash
    cp envs/dev.env bot/.env
    ```
3. Install the dependencies

    ```bash
    poetry install
    ```

4. Configure the settings in the ENV (note that configuring the postgres uri is required)
5. Run the migrations runner

    ```bash
    poetry run python migrations-runner.py
    ```

6. Run the bot
    
    ```bash
    poetry run python bot/zoeebot.py
    ```

7. Once your bot is running, sync the commands to your guild. You might have to wait a while because the syncing process usually takes some time. Once completed, you should now have the `CommandTree` synced to that guild. 

    ```
    # Replace 12345 with your guild id
    z>sync 12345 
    ```
8. Now go ahead and play around with the default commands. Add your own, delete some, do whatever you want now.
