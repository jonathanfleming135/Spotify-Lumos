In order to start this, a few things are needed.

First, both the host computer and raspberry pi require ssh. You must be able to access the rpi over ssh under the hostname "lumos". Furthermore, it is expected that the /spotify-lumos is connected from the host to the rpi over sshfs (could be removed with a few scp commands in the code). 

The "spotify_auth.py" script in the /host directory must be run from the host computer to start the authorization stuff on the rpi. Form this point on, the rpi should deal with all the authorization stuff on its own.
