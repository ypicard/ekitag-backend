# Backend

In flask

# You can connect an IOT object to this app (no way ?!)
If on Eki's network, we will use ngrok (npm package), your MAC's internet sharing, and an SSH tunnel between a localhost:port to the IOT's webserver IP
```
ngrok http 5050
ssh -L5050:192.168.2.2:80 yourusername@localhost
```

This may require you to launch the SSH service before:

```
sudo launchctl load -w /System/Library/LaunchDaemons/ssh.plist
```

To stop it:

```
sudo launchctl unload  /System/Library/LaunchDaemons/ssh.plist
```