#! /usr/bin/env python3


import os
import shutil
import time
import tempfile
import argparse
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    VERBOSE = '\033[96m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def copy_symlink(src, dest):
    link_target = os.readlink(src)
    if os.path.isabs(link_target):
        print(f"{bcolors.FAIL}[!] Tool does not handle absolute symlinks! Aborting!{bcolors.ENDC}")
        exit(1)
    os.symlink(link_target, dest)
    
# this copies the directory while leaving the additional files 
# that are already in the dest in place
def copy_dir(source_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    for file in os.listdir(source_dir):
        source = source_dir + "/" + file
        dest = dest_dir + "/" + file
        if os.path.isdir(source):
            copy_dir(source, dest)
        else:
            try:
                if os.path.islink(source):
                    copy_symlink(source, dest)
                else:
                    shutil.copy(source, dest)
            except FileNotFoundError:
                print(f"{bcolors.WARNING}[!] Could not copy {source}!{bcolors.ENDC}")

class FileSyncher(FileSystemEventHandler):

    def __init__(self, local_path, remote_path, verbose):
        super().__init__()
        self.local_path = local_path
        self.remote_path = remote_path
        self.verbose = verbose

    def get_relative_path(self, remote_path):
        return os.path.relpath(remote_path, self.local_path)

    def delete_file_or_folder(self, path):
        try:
            os.remove(path)
        except IsADirectoryError:
            shutil.rmtree(path)

    def copy_file_or_folder(self, src_path, dest_path):
        if os.path.islink(src_path):
            copy_symlink(src_path, dest_path)
            return
            
        try:
            # try copytree first as it also handles symlinks
            shutil.copytree(src_path, dest_path)
        except NotADirectoryError:
            shutil.copy(src_path, dest_path)
        
    def on_modified(self, event):
        if self.verbose: print(f"[+] Updating {event.src_path}")

        if os.path.isfile(event.src_path):
            file_relpath = self.get_relative_path(event.src_path)
            try:
                shutil.copy(event.src_path, self.remote_path + "/" + file_relpath)
            except FileNotFoundError:
                # file does not exist; probably already deleted
                pass
    
    def on_created(self, event):
        if self.verbose: print(f"[+] Creating {event.src_path}")

        file_relpath = self.get_relative_path(event.src_path)
        try:
            self.copy_file_or_folder(event.src_path, self.remote_path + "/" + file_relpath)
        except FileNotFoundError:
            # file does not exist; probably already deleted
            pass
    
    def on_deleted(self, event):
        if self.verbose: print(f"[+] Deleting {event.src_path}")
        file_relpath = self.get_relative_path(event.src_path)

        try: 
            self.delete_file_or_folder(self.remote_path + "/" + file_relpath)
        except FileNotFoundError:
            # file does not exist; so we dont need to delete
            pass
    
    def on_moved(self, event):
        if self.verbose: print(f"[+] Moving {event.src_path} to {event.dest_path}")

        src_relpath = self.get_relative_path(event.src_path)
        dest_relpath = self.get_relative_path(event.dest_path)
        try:
            shutil.move(self.remote_path + "/" + src_relpath, self.remote_path + "/" + dest_relpath)
        except FileNotFoundError:
            # file does not exist; probably already deleted
            pass
        

def parse_arguments() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument(type=str,  # cast argument to this type
                        metavar="<source-directory>",  # the value used for help messages
                        dest="source",
                        action="store",  # just store the value
                        help="The directory to sync from")
    parser.add_argument(type=str,  # cast argument to this type
                        metavar="<destination-directory>",  # the value used for help messages
                        dest="destination",
                        action="store",  # just store the value
                        help="The directory to sync to")
    parser.add_argument('--verbose',
                        dest="verbose",
                        action="store_true",  # just store that the value was set
                        help="Enable verbose messages",
                        required=False)

    return vars(parser.parse_args())

    
def create_sshfs_mount(local_path, remote_path, remote_host):
    p = subprocess.run(["sshfs", f"{remote_host}:{remote_path}", local_path])
    if p.returncode != 0:
        print(f"{bcolors.FAIL}[!] Failed to create sshfs directory. Aborting!{bcolors.ENDC}")
        print(f"{bcolors.FAIL}[!] Does the remote directory exist? If not, create it!")
        exit(1)

def remove_sshfs_mount(local_path):
    p = subprocess.run(["fusermount3", "-u", local_path])
    if p.returncode != 0:
        print(f"{bcolors.FAIL}[!] Failed to cleanup sshfs directory!{bcolors.ENDC}")


    
def main():
    
    arg_dict = parse_arguments()

    local_path = arg_dict["source"]

    if ":" in arg_dict["destination"]:
        remote_connection_used = True
        # parse host
        remote_host, remote_path = arg_dict["destination"].split(":")
        print(f"{bcolors.OKGREEN}[+] Syncing from {local_path} to {remote_path} (on {remote_host}){bcolors.ENDC}")

        # create an sshfs
        sshfs_temp_directory = tempfile.mktemp()
        os.mkdir(sshfs_temp_directory)
        create_sshfs_mount(sshfs_temp_directory, remote_path, remote_host)

        # let the remote path point to the sshfs directory
        remote_path = sshfs_temp_directory
    else:
        remote_path = arg_dict["destination"]
        print(f"{bcolors.OKGREEN}[+] Syncing from {local_path} to {remote_path} (local){bcolors.ENDC}")

    copy_dir(local_path, remote_path)
    
    event_handler = FileSyncher(local_path, remote_path, arg_dict["verbose"])

    observer = Observer()
    observer.schedule(event_handler, local_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        if remote_connection_used:
            remove_sshfs_mount(sshfs_temp_directory)
            shutil.rmtree(sshfs_temp_directory)
        observer.stop()
        observer.join()

    



if __name__ == "__main__":
    main()
