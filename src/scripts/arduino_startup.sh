#bin/bash/!

xterm -e 'picocom -b 115200 /dev/ttyACM0' & export APP_PID=$!;
#sleep 20;
#kill $APP_PID;
