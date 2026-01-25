# Discord Reminder Bot

This is a discord bot which you (or your friends) can set reminders. You can specify a reason why you set the reminder and the time you wanted to reminded at (via seconds, hours, weeks, etc.)
After the reminder time has been reached, you will recieve a DM with the reminder, as can be seen in the screenshots.

# Sreenshots
<img width="746" height="86" alt="image" src="https://github.com/user-attachments/assets/194dcb88-c213-4b38-b4ee-3b15611b2a28" />
<img width="761" height="135" alt="image" src="https://github.com/user-attachments/assets/90ab0f0d-47ec-408a-8686-5f4adf5d701d" />
<img width="697" height="94" alt="image" src="https://github.com/user-attachments/assets/495b0971-df8a-49b4-acb1-2448885fa5bc" />

## Note:
Reminders cannot be removed once they have been set as of now.

## Setup

Install the required python packages:

```bash
pip install discord.py aiofiles
```

Make sure to add your bot token to the main.py file. You can get one via the [Discord Developer Platform](https://discord.dev/) website.

Then to run the bot just do:

```bash
python3 main.py
```

## Usage

To use the bot just run one the following:

```
r.remind TIME REASON
/remind TIME REASON
```

The time uses a `w` (weeks), `d` (days), `h` (hours), `m` (minutes), `s` (seconds).

And yes, you can combine them if you want to.

## Bugs
If there are any bugs, please open a bug report using the `issues` tab on github.

Please make sure to include useful information such as:
- Device you are using
- Python version (can be retrived via `python3 --version`)
- Any logs

## Updates
As stated above, this was just a project I made because I was bored. This may get updates if people actually use it, otherwise, this is the condition it will stay in unless I get bored again.
