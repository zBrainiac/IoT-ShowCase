# IoT-ShowCase
IoT Agent > local mqtt forward to central mqtt gateway > NIFI > Kafka > Druid &amp; Grafana


**Kafka:**
cd /usr/hdp/current/kafka-broker/  
./bin/kafka-topics.sh --create --zookeeper druid.hdp.md:2181 --replication-factor 1 --partitions 1 --topic sensor_md  
./bin/kafka-topics.sh --list --zookeeper druid.hdp.md:2181  
./bin/kafka-console-consumer.sh --bootstrap-server druid.hdp.md:6667 --topic sensor_md


**Druid - supervisior (kafka index service:**

cd /usr/hdp/current/druid-broker/  
mkdir supervisor  
copy file IoT-kafka-supervisor_v0-1-1.json  
curl -XPOST -H'Content-Type: application/json' -d @Iot-supervisor-v0-1-1.json http://druid.hdp.md:8090/druid/indexer/v1/supervisor


**IoT Sensor:**

watch -n60 python3 mqtt_loop.py


**grafana:**

start grafana server:  
grafana-server --config=/usr/local/etc/grafana/grafana.ini --homepath /usr/local/share/grafana cfg:default.paths.logs=/usr/local/var/log/grafana cfg:default.paths.data=/usr/local/var/lib/grafana cfg:default.paths.plugins=/usr/local/var/lib/grafana/plugins
 
**add druid-plugin:** 


**configure dashboard:**
