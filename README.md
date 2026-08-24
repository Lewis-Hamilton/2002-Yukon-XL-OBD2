# 2002-Yukon-XL-OBD2

Get OBD2 data off of truck

Start collecting data

1. Setup virtual environment
2. run `pip install -e .`
3. run `python3 -m yukon_watcher`

Give script permission to control the pi
1. `sudo visudo -f /etc/sudoers.d/99-yukon-poweroff`
2. paste this line in the file and save `lewis ALL=(ALL) NOPASSWD: /usr/bin/systemctl poweroff, /usr/bin/systemctl stop yukon.service, /sbin/poweroff`
3. `sudo chmod 0440 /etc/sudoers.d/99-yukon-poweroff`

Auto Start on boot

1. cd into dotfiles
2. `sudo stow -d dotfiles -t / startup`
3. `sudo systemctl daemon-reload`
4. `sudo systemctl enable yukon.service`
5. reboot
6. will now run on boot