#!/bin/bash

CONSUL_SERVER=newbee13:32500

unregiste(){
    curl --request PUT http://${CONSUL_SERVER}/v1/agent/service/deregister/$2
}

case $1 in
    unregiste)
        unregiste
        ;;
    *)
        echo "Usage: unregiste ID"
        ;;
esac
exit 0
