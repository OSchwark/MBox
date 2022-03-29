# MBox
Setting up a toniebox like audio playback device

1. Install raspberry pi OS LITE on SD card using raspberry pi imager (https://www.raspberrypi.org/software/)
2. create `ssh` file on SD card to enable ssh
3. boot sd card in raspberry pi
4. Ssh into it
5. Add mopidy gpg key
```
sudo mkdir -p /usr/local/share/keyrings
sudo wget -q -O /usr/local/share/keyrings/mopidy-archive-keyring.gpg https://apt.mopidy.com/mopidy.gpg
```
7. `sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/buster.list`
8. Install python3-spotify
``` 
sudo apt-get update
sudo apt-get install python3-spotify
```
9. Find api key https://github.com/search?q=spotify-appkey 
10. install pyalsaaudio `pip install pyalsaaudio`
12. copy files
13. copy service file to root `sudo cp myscript.service /etc/systemd/system/myscript.service`
14. reload services `sudo systemctl daemon-reload`
15. enable service `sudo systemctl enable myscript.service`

