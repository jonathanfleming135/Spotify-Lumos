#bin/bash/!

xterm -e 'picocom -b 115200 /dev/ttyACM0' & export APP_PID=$!;