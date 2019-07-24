#!/bin/bash
basepath=$(cd `dirname $0`; pwd)
HOME=$(cd $basepath/..;pwd)
APP_PID=$HOME/pid/pid.txt
source /root/anaconda3/etc/profile.d/conda.sh
conda activate kg
start(){
cd $HOME/
nohup python main.py --start 1 > logs/nohup.out 2>&1 &
echo $!>$APP_PID
echo "starting at pid"$(cat $APP_PID)
}
stop(){
echo "stoping pid"$(cat $APP_PID)
sudo kill -9 $(cat $APP_PID)
}
case $1 in
        start)
         start
        ;;
        stop)
         stop
        ;;
        restart)
         $0 stop
        sleep 2
         $0 start
        ;;
        *)
         echo "Usage:{start|stop|restart}"
        ;;
esac
exit 0
