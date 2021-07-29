# MBox
Setting up a toniebox like audio playback device

1. Install raspberry pi OS on SD card
2. create `ssh` file on SD card to enable ssh
3. boot sd card in raspberry pi
4. Ssh into it
5. Switch python version(*):
`sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10`
6. Add mopidy gpg key
`wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -`
7. `sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/buster.list`
8. Install python3-spotify
``` 
sudo apt-get update
sudo apt-get install python-spotify
```
9. Find api key https://github.com/search?q=spotify-appkey 
10. install pyalsaaudio `sudo apt-get install python-alsaaudio`






*(undo with `sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 10`

