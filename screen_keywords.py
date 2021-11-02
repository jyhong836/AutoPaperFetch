"""Go thru a list of keywords."""
import sys, os
import subprocess

# keywords = ['federated', "distill", 'fair', 'domain', 'backdoor', 'privacy', ]
keywords = ['fair']
for kw in keywords:
    print(f"\n======== KW: {kw} ========")
    cmd = f"python paper_fetcher.py {kw} --print-paper"
    log_file = f"{kw}.txt"
    print(f"TO RUN: {cmd}\nOutput to: {log_file}")
    # os.system(cmd)
    subprocess.call(cmd, stdout=open(log_file, 'w'), shell=True)
    # subprocess.call('ls')
