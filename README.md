# tools
Some useful tools
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

#### Example Usage
```bash
./presentation-slide-timer.py timestamps.log
Press ENTER to start the presentation timer

# press enter and switch to, e.g., pdfpc to practise your talk now. When finished press CTRL-C

[*] Slide 1 took 2 seconds and ended at 0:02.
[*] Slide 2 took 5 seconds and ended at 0:08.
[*] Slide 3 took 3 seconds and ended at 0:11.
^C
[+] Shortest slide: slide 1 with 0:02.
[+] Longest slide: slide 2 with 0:05.
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
