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

## Notify-Me
#### Dependencies 
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
#### Functionality  
Runs a command/binary and sends Telegram notification upon finish.

#### Example Usage
```bash
./notify_me.py find / -iname "flag.txt"
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
