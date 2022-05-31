#!/bin/bash --utf8
sudo hdfs dfs -copyToLocal /tmp/data/bigdata.csv /bigdata
sudo scp -i "key-big-data.pem" bigdata.csv ec2-user@ec2-54-82-57-161.compute-1.amazonaws.com:~/Data/bigdata.csv