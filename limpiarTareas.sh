#!/bin/bash
sudo pkill -9 -u www-data
sudo service apache2 stop
sudo service apache2 start