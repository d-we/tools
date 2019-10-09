#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#

from pwn import *
import sys


def main():
    context.log_level = "error"
    if len(sys.argv) != 2:
        print("usage: %s <binary_name>" % sys.argv[0])
        return
    bin_name = sys.argv[1]
    e = ELF(bin_name)
    try:
        alarm_plt = e.plt['alarm']
    except KeyError:
        print("[+] No alarm in binary! :)")
        return 0
    print("[*] alarm@plt: 0x%x" % alarm_plt)
    # just write "ret" as first instruction to alarm@plt
    e.write(alarm_plt, asm("ret"))
    print("[*] patched alarm@plt to just return")
    # save new binary under different name
    patched_bin_name = bin_name + "_no_alarm"
    e.save(patched_bin_name)
    print("[+] saved binary as %s" % patched_bin_name)


if __name__ == "__main__":
    main()
