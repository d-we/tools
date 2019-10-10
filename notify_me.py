#! /usr/bin/env python3


import os
import time
import sys
import telegram


def read_config(fname):
    chat_id = None
    api_key = None
    with open(fname, "r") as fd:
        for line in fd:
            if line.startswith("chat-id:"):
                chat_id = ":".join(line.split(":")[1:]).strip()
            if line.startswith("api-key:"):
                api_key = ":".join(line.split(":")[1:]).strip()
    return api_key, chat_id


def main():
    script_path = os.path.dirname(os.path.realpath(__file__))
    config_file = "notify_me.config"
    if len(sys.argv) < 2:
        print(f"[*] USAGE: {sys.argv[0]} <program> <arguments>")
        exit(0)

    # read config file
    api_key, chat_id = read_config(script_path + "/" + config_file)
    if not api_key or not chat_id:
        print(f"[-] Error on reading config-file ({config_file}) . Aborting!")
        print(f"[-] api-key: {api_key} - chat-id: {chat_id}")
        exit(0)

    # treat everything as command
    cmd = " ".join(sys.argv[1::])

    # run command and measure time
    before = time.time()
    ret = os.system(cmd)
    after = time.time()

    # format time and message
    time_elapsed_formatted = time.strftime("%H:%M:%S", time.gmtime(
        after - before))
    msg = f"Execution finished.\n" \
        f"Command: {' '.join(sys.argv[1:])}\n" \
        f"Exit-Code: {ret}\n" \
        f"Time elapsed: {time_elapsed_formatted}."

    # send telegram notification
    bot = telegram.Bot(api_key)
    bot.send_message(chat_id, msg)


if __name__ == "__main__":
    main()
