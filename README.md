# MPCPyTk

Exemple d'un reproductor MP3 GUI (amb interfície gràfica d'usuari) amb Python i tkinter, per MPD i MPC de GNU Linux.
Amb finestra principal, subfinestres, refresc pantalla, control de volum, equalitzador animat, botonera, control ListboxSelect, Double Click, ...
Ús de  classes, gestió de llistes de reproducció i fitxers.

## Requeriments

- OS: Arch Linux x86_64
- Kernel: 6.0.9-arch1-1
- DE: GNOME 43.1
- python = [3.8, 3.10]
- MPD: Music Player Daemon 0.23.5 (0.23.5)
- MPC: A minimalist command line interface to MPD / mpc version: 0.34
- tkinter 8.6.12

## setup environment: pyenv and venv
- https://github.com/pyenv/pyenv
- https://github.com/pyenv/pyenv?tab=readme-ov-file#linuxunix
- install **pyenv** for Arch
```
curl -fsSL https://pyenv.run | bash
```
- install Arch dependencies
```
pacman -S --needed base-devel openssl zlib xz tk zstd
```
- edit `.bashrc`
```
nano ~/.bashrc
```
- Append these lines to the end of the file
```
# Pyenv
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"
eval "$(pyenv virtualenv-init -)"
```
- call .bashrc
```
source ~/.bashrc
```
- check pyenv
```
pyenv versions
```
- install Python 3.10
```
pyenv install 3.10.4
```
- go to the project folder and set the local Python version
```
cd /home/aleon/mpcpy_aleon/
pyenv local 3.10.4
```
- create the virtual environment **venv**
```
python -m venv .venv
```
- activate the virtual environment
```
source .venv/bin/activate
```
- check python version in venv
```
(.venv) [aleon@arch mpcpy_aleon]$ python --version
Python 3.10.4
```
- install dependencies in venv
```
pip install [package]
```

## MPD
https://www.musicpd.org/
https://mpd.readthedocs.io/en/stable/user.html

- install on **arch**
```sudo pacman -S mpd```
- or **ubuntu**
```apt install mpd```
- configure /etc/mpd.conf
- add permissions rx for others (user mpd) in all of necessary folders
- add permissions rx for others in /home/user if is necessary
```
music_directory "/home/aleon/Música"
playlist_directory "/home/aleon/playlists"
user "mpd"
auto_update "yes"
audio_output {
        type            "alsa"
        name            "My ALSA Device"
#       device          "hw:0,0"        # optional
#       mixer_type      "hardware"      # optional
#       mixer_device    "default"       # optional
##      mixer_control   "PCM"           # optional
##      mixer_index     "0"             # optional
}
#
...
```
- load mp3 music in music_directory
- add info.txt in every album directory with gender, year and author 
- sudo systemctl enable mpd
- sudo systemctl start mpd
- sudo systemctl status mpd
- check errors, files, directories and folder permissions
- reboot if is necessary

## MPC
https://www.musicpd.org/clients/mpc/
https://www.musicpd.org/doc/mpc/html/

- sudo pacman -S mpc (**arch**)
- apt install mpc (**ubuntu**)
- mpc update
- mpc ls
- mpd add /
- mpc play

## tkinter
https://docs.python.org/3/library/tkinter.html
https://realpython.com/python-gui-tkinter/

(**arch**)
- sudo pacman -S tk
- sudo pacman -S pyqt5
- sudo pacman -S pyside2
- sudo pacman -S python-pillow

## mpcpy_aleon

- DIR_MUSIC = '/home/aleon/Music' (= /etc/mpd.conf)
- DIR_PLAYLIST = '/home/aleon/playlists' (/etc/mpd.conf)

## files

- **albums**: album objects pickel
- **estat_reproductor**: MPC current state
- **playlist.txt**: current playlist
- **playlists.txt**: list of playlist
- **info.txt**: album information in album folder
```
gender
year
author
```

## Run

- `cd mpcpytk_aleon`
- `source .venv/bin/activate`
- `python tk_aleon.py`

![Screenshot](img/1.png)

![Screenshot](img/2.png)