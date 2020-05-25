Slide Into the DMs: Twitter + Python!
======


Description
------------
Exploratory Tool to Interact with Twitter API.
Components include:
1. `direct_message.py` to send DMs (with Media, Calls-to-action, or Quick-reply forms) via Python to specified users and `direct_message_analyzer.py` to perform sentiment analysis for auto responses.
2. `welcome_message.py` to create a welcome message for any user who interacts with account via DM.

Installation
------------
Ensure you are using Python 3 (version 3.7.4 as of this writing).  See your default:
    $ python --version

Ideally, don't use the default Mac OS X Python.  Use [pyenv](https://github.com/pyenv/pyenv) to manage Python environments.
Here is an abridged guide, but find detailed instructions by [Broberg and Zadka](https://opensource.com/article/19/5/python-3-default-mac).
Install the latest python version:
    $ pyenv install 3.7.4

Set this Python 3.7.4 as global default for pyenv environments:
    $ pyenv global 3.7.4
    # and verify it worked
    $ pyenv version

Give control of shell's path [add to configuration file (**.zshrc** or **.bash_profile**):
    $ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshrc


Usage
------------
In the downloaded directory, **activate the virtual environment** as changes have been made to the Tweepy library to make direct-message actions actually functional.
    $ source ./venv/bin/activate

Update Twitter API Credentials (find details on [TwitterDev](https://developer.twitter.com/en.html)) in `twitter_credentials.py`.
**Run** as usual:
    $ python <selectedscript.py>

