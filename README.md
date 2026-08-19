# 2002-Yukon-XL-OBD2
Get OBD2 data off of truck

Start collecting data
1. Setup virtual environment
2. run `pip install -r requirements.txt`
3. run `python3 src/get_commands.py` to get list of available commands for vehicle
4. Add commands to `src/main.py`
5. run `python3 src/main.py`

Auto Start script on boot
1. cd into dotfiles
2. `sudo stow -d dotfiles -t / startup`
3. `sudo systemctl daemon-reload`
4. `sudo systemctl enable yukon.service`
5. reboot
6. will now run on boot