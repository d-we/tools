#! /usr/bin/env python3


import sys
import time
from pynput.keyboard import Listener, Key, KeyCode


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class PresentationTimer:
    # these are the keys that we assume skip to the next slide during the presentation
    keys_to_skip_slides = [Key.space, Key.enter, Key.right]
    # pressing this key pauses/resumes the timer
    pause_key = "P"

    def __init__(self, logfilename):
        self.start_time = -1
        self.paused = False
        self.pause_start_time = -1

        # per slide statistics
        self.last_slide_end = -1
        self.logfilename = logfilename

        # global statistics
        self.min_time_per_slide = -1
        self.max_time_per_slide = -1
        self.min_time_per_slide_slideno = -1
        self.max_time_per_slide_slideno = -1

        self.logfile = open(logfilename, "w")
        self.slide_no = 1

    def __del__(self):
        if self.logfile is not None:
            self.write_statistics_and_close_logfile()

    @staticmethod
    def seconds_to_min_and_seconds(timestamp_in_seconds):
        timestamp_minutes = timestamp_in_seconds // 60
        timestamp_seconds = timestamp_in_seconds % 60
        return timestamp_minutes, timestamp_seconds

    def on_keypress(self, key):
        # check if slide was skipped
        if key in self.keys_to_skip_slides and not self.paused:
            # get statistics for the current slide
            slide_end = time.time()
            slide_time_elapsed = int(slide_end - self.last_slide_end)
            slide_end_absolute = int(slide_end - self.start_time)

            slide_end_timestamp_minutes, slide_end_timestamp_seconds = \
                self.seconds_to_min_and_seconds(slide_end_absolute)

            # update global statistics
            if slide_time_elapsed > self.max_time_per_slide or self.max_time_per_slide == -1:
                self.max_time_per_slide = slide_time_elapsed
                self.max_time_per_slide_slideno = self.slide_no
            if slide_time_elapsed < self.min_time_per_slide or self.min_time_per_slide == -1:
                self.min_time_per_slide = slide_time_elapsed
                self.min_time_per_slide_slideno = self.slide_no

            log_message = f"Slide {self.slide_no} took {slide_time_elapsed} seconds " \
                          f"and ended at " \
                          f"{slide_end_timestamp_minutes}:{slide_end_timestamp_seconds:02}."

            # print msg to stdout and write to logfile
            print(f"{bcolors.OKBLUE}[*] {log_message}{bcolors.ENDC}")
            self.logfile.write(log_message + "\n")

            # set values for next slide
            self.slide_no += 1
            self.last_slide_end = slide_end

        # checker for pause key
        if key == KeyCode.from_char(self.pause_key):
            if not self.paused:
                print(f"{bcolors.WARNING}Paused.{bcolors.ENDC}")
                # pause begin
                self.pause_start_time = time.time()
                self.paused = True
            else:
                # pause end
                print(f"{bcolors.WARNING}Resumed.{bcolors.ENDC}")
                paused_time = time.time() - self.pause_start_time
                self.start_time += paused_time
                self.paused = False

    def write_statistics_and_close_logfile(self):
        assert self.logfile is not None
        shortest_slide_minutes, shortest_slide_seconds = \
            self.seconds_to_min_and_seconds(self.min_time_per_slide)
        logmessage_shortest = f"Shortest slide: slide {self.min_time_per_slide_slideno} " \
                              f"with {shortest_slide_minutes}:{shortest_slide_seconds:02}."
        print(f"\n{bcolors.OKGREEN}[+] {logmessage_shortest}{bcolors.ENDC}")
        self.logfile.write(logmessage_shortest + "\n")

        longest_slide_minutes, longest_slide_seconds = \
            self.seconds_to_min_and_seconds(self.max_time_per_slide)
        logmessage_longest = f"Longest slide: slide {self.max_time_per_slide_slideno} " \
                             f"with {longest_slide_minutes}:{longest_slide_seconds:02}."
        print(f"{bcolors.OKGREEN}[+] {logmessage_longest}{bcolors.ENDC}")
        self.logfile.write(logmessage_longest + "\n")

        self.logfile.close()
        self.logfile = None

    def wait_for_start_and_initialize_states(self):
        input("Press ENTER to start the presentation timer")
        # initialize values on start
        self.start_time = time.time()
        self.last_slide_end = self.start_time

    def start(self):
        self.wait_for_start_and_initialize_states()
        try:
            # start listening for skipped slides
            with Listener(on_press=self.on_keypress) as listener:
                listener.join()
        except KeyboardInterrupt:
            self.write_statistics_and_close_logfile()
            print(f"{bcolors.OKGREEN}[+] Finished. Results were written to {self.logfilename}"
                  f"{bcolors.ENDC}")


def main():
    if len(sys.argv) != 2:
        print(f"USAGE: {sys.argv[0]} <timestamp-logfile>")
        exit(0)

    logfile = sys.argv[1]
    presentation_timer = PresentationTimer(logfile)
    presentation_timer.start()


if __name__ == "__main__":
    main()
