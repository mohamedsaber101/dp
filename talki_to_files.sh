rm /tmp/v; rm /tmp/a;for i in `seq $(cat /tmp/t|wc -l|cut -d' ' -f1)`;do clear;sed -n ${i}p /tmp/t ;echo '===================='; read e;if [ "$e" == "d" ];then continue;fi; echo $e |grep '^v ' 1>/dev/null 2>/dev/null ;if [ $? -eq 0 ];then E=`echo $e|sed 's/^v //g'`; echo "$E  ----------**----------- `sed -n ${i}p /tmp/t`" >> /tmp/v;else echo "E -- $e" >> /tmp/a;echo "-------------------------" >> /tmp/a;echo `sed -n ${i}p /tmp/t` >> /tmp/a;fi ;done