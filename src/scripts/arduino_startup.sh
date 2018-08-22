#bin/bash/!

pico_running=true
port_active=true

pico_str="$(ps -ef | grep ttyACM0)"

#is picocom running on our serial port
if [[ $pico_str = *"picocom"* ]]; then
	pico_running=true
else
	pico_running=false
fi

#is our serial port active
port_str="$(ls /dev | grep tty)"
if [[ $port_str = *"ACM0"* ]]; then
	port_active=true
else
	port_active=false
fi

if [ $pico_running = true ] && [ $port_active = false ]; then
	regex="^pi\s+([0-9]+).+ttyACM0"
	[[ $pico_str =~ $regex ]] && pid=${BASH_REMATCH[1]}
	kill -9 $pid
fi

picocom -b 115200 /dev/ttyACM0 &>/dev/null &
