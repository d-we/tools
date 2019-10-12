#! /usr/bin/env python3
import errno
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


def get_cmdline(pid):
    cmdline = ""
    try:
        with open(f"/proc/{pid}/cmdline", "rb") as fd:
            for line in fd:
                # nullbyte encodes space in this file
                cmdline += " ".join(line.decode().split("\x00"))
    except FileNotFoundError:
        print(f"[-] Process({pid}) not running")
        return None
    return cmdline


def wait_for_process_exit(pid):
    starttime = os.path.getctime(f"/proc/{pid}")
    has_finished = False
    while not has_finished:
        try:
            # we check if the creation time has changed
            # (new process spawned with same pid)
            new_starttime = os.path.getctime(f"/proc/{pid}")
            if starttime != new_starttime:
                has_finished = True

            # if SIGNAL 0 works the process is still alive
            os.kill(pid, 0)
        except (OSError, FileNotFoundError) as err:
            if err.errno == errno.EPERM:
                # there exists a process but we have no permissions to it
                continue
            has_finished = True
        # wait to prevent being to noisy
        time.sleep(3)


def print_help():
    print(f"[*] USAGE (command):\t{os.path.basename(sys.argv[0])} <program> <arguments>")
    print(f"[*] USAGE (attach):\t{os.path.basename(sys.argv[0])} -p <pid>")


def main():
    script_path = os.path.dirname(os.path.realpath(__file__))
    config_file = "notify_me.config"
    if len(sys.argv) < 2:
        print_help()
        exit(0)

    command_mode = True
    if sys.argv[1] == "-p":
        if len(sys.argv) != 3:
            print_help()
            exit(0)
        pid = int(sys.argv[2])
        command_mode = False

    # read config file
    api_key, chat_id = read_config(script_path + "/" + config_file)
    if not api_key or not chat_id:
        print(f"[-] Error on reading config-file ({config_file}) . Aborting!")
        print(f"[-] api-key: {api_key} - chat-id: {chat_id}")
        exit(0)

    if command_mode:
        # treat everything as command
        cmd = " ".join(sys.argv[1::])

        # run command and measure time
        before = time.time()
        exit_code = os.system(cmd)
        after = time.time()
    else:
        cmd = get_cmdline(pid)
        if not cmd:
            print("[-] Aborting!")
            exit(0)
        print(f"[+] Waiting for process({pid}): {cmd}")
        before = os.path.getctime(f"/proc/{pid}")
        wait_for_process_exit(pid)
        after = time.time()
        exit_code = "Unknown"

    # format time and message
    time_elapsed_formatted = time.strftime("%H:%M:%S", time.gmtime(
        after - before))
    msg = f"Execution finished.\n" \
        f"Command: {cmd}\n" \
        f"Exit-Code: {exit_code}\n" \
        f"Time elapsed: {time_elapsed_formatted}."

    # send telegram notification
    bot = telegram.Bot(api_key)
    bot.send_message(chat_id, msg)


if __name__ == "__main__":
    main()
