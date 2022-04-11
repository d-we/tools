# tools
Various small tools I developed because I wanted them in my daily life. If not stated otherwise the tools are written for Linux.

## Remove-Alarm
#### Dependencies 
- [pwntools](https://github.com/Gallopsled/pwntools) (python2)
#### Functionality  
Patches a given binary to remove the call for the libc function `alarm`. The patched binary is saved under a new name.
#### Example Usage
```bash
./remove_alarm.py evil-binary
```


## Presentation-Slide-Timer
#### Dependencies 
- [pynput](https://pypi.org/project/pynput/) (python3)
#### Functionality  
When giving presentations I note down the end time of each slide during practise talks. This gives a good guidance for my timing during the actual talk.
This tool can be started in the background when practising a presentation. It will capture pressed keys, e.g., *SPACE*, to check when you skip a slide in your presentation tool. For each slide it notes down the time. It also stores the time to a logfile. 

The script also supports a pause functionality. Pressing Shift-P stops/resumes the timer.
#### Example Usage
```bash
./presentation-slide-timer.py timestamps.log
Press ENTER to start the presentation timer

# press enter and switch to, e.g., pdfpc to practise your talk now. When finished press CTRL-C

[*] Slide 1 took 32 seconds and ended at 0:32.
[*] Slide 2 took 20 seconds and ended at 0:52.
[*] Slide 3 took 50 seconds and ended at 1:42.
^C
[+] Shortest slide: slide 2 with 0:20.
[+] Longest slide: slide 3 with 0:50.
[+] Finished. Results were written to timestamps.log
```


## Notify-Me
#### Dependencies 
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
#### Functionality  
Runs or attaches to a command/binary and sends Telegram notification upon finish.

#### Example Usage
```bash
./notify_me.py find / -iname "flag.txt"
./notify_me.py -p 31337
```

Sent telegram notification:
```
Execution finished.
Command: find / -iname flag.txt
Exit-Code: 256
Time elapsed: 00:00:41.
```

#### Example Config-file (save as 'notify_me.config')
```
# chat-id of my own chat with the Telegram bot
chat-id: <chat-id>
# api-key for the Telegram bot 
api-key: <api-key>
```

#### Credits
Thanks to Jessica Schmidt for the initial idea and code.

## Brightness
#### Functionality
Increases or decreases display brightness. I wrote this because the Linux kernel does not support setting the brightness of OLED displays out-of-the-box hence I bind shortcuts to this script.

#### Example
- Bind "monitor screen brightness increase"-key to `brightness +`
- Bind "monitor screen brightness decrease"-key to `brightness -`
