# IoT-ShowCase

**Vison**
e2e IoT Show Case which demonstrating a (near) real-time monitoring
![IoT Show Case Overview](images/IoT-ShowCaseOverview.png)

**The idea is:**  
1.) to have multiple IoT agents / sensors which using a local mqtt server instance to reduce the risk of loss of data  
2.) Local mqtt server forward to messages to regional mqtt gateway  
3.) NIFI collects the messages form the regional gateway and pushing into Kafka and as JSON & CSV files into HDFS  
4.) Druid runs the Kafka-Index-Service with a supervison-spec with fits to the sensor messages  
5.) Grafana is used for the visualisation 


**Kafka:**
cd /usr/hdp/current/kafka-broker/  
./bin/kafka-topics.sh --create --zookeeper druid.hdp.md:2181 --replication-factor 1 --partitions 1 --topic sensor_md  
./bin/kafka-topics.sh --list --zookeeper druid.hdp.md:2181  
./bin/kafka-console-consumer.sh --bootstrap-server druid.hdp.md:6667 --topic sensor_md


**Druid - supervisior (Kafka-Index-Service):**

FYI: *The Kafka Ingestion is still in Technical Preview as of today, so It doesn’t come bundled as part of the platform. As such, some minor configuration changes will need to be applied.  
In Ambari, navigate to the druid service and click on the configs tab. Now, using the filter, search for “druid.extensions.loadList”.  
For this parameter, enter “druid-kafka-indexing-service” to the list. This parameter essentially tells Druid to load these extensions on startup on the cluster.*

add *supervisor* spec:  
cd /usr/hdp/current/druid-broker/  
mkdir supervisor
cd  supervisor
copy file IoT-kafka-supervisor_v0-1-1.json  into the new directory

start *supervisor* task:  
curl -XPOST -H'Content-Type: application/json' -d @Iot-supervisor-v0-1-1.json http://druid.hdp.md:8090/druid/indexer/v1/supervisor


**IoT Sensor:**  
start data-generator:  
watch -n60 python3 mqtt_loop.py


**Grafana:**  
Install druid-plugin:  
grafana-cli plugins install abhisant-druid-datasource



start grafana server:  
grafana-server --config=/usr/local/etc/grafana/grafana.ini --homepath /usr/local/share/grafana cfg:default.paths.logs=/usr/local/var/log/grafana cfg:default.paths.data=/usr/local/var/lib/grafana cfg:default.paths.plugins=/usr/local/var/lib/grafana/plugins
 


**Configure Grafana dashboard:**
Honestly, the druid editor is a diva and it needs some time to get used to it.... 
It is important to save every part of the query with 'add tag'.  
*Limitation:* with the current grafana-druid plugin (v.0.0.5) the query is at least 60 seconds. To get around this, you have to calculate the sum of the values across all events and divide them by the number of events to get an average. mysql (graph on the left side) is able to show all events individual.  
![grafana dashboard](images/grafana_dashboard.png)


with 3 individual *sensor values* per message on one dashboard:     
![grafana dashboard](images/grafana_editor2.png)

Druid-Plugin editor details:
![grafana dashboard](images/grafana_detail.png)


exported Model:

      "targets": [
        {
          "aggregators": [
            {
              "hidden": true,
              "name": "tpm",
              "type": "count"
            },
            {
              "fieldName": "value_1",
              "hidden": true,
              "name": "t_value_1",
              "type": "longSum"
            },
            {
              "fieldName": "value_3",
              "hidden": true,
              "name": "t_value_3",
              "type": "longSum"
            },
            {
              "fieldName": "value_2",
              "hidden": true,
              "name": "t_value_2",
              "type": "longSum"
            }
          ],
          "currentAggregator": {
            "type": "count"
          },
          "currentFilter": {
            "type": "selector"
          },
          "currentPostAggregator": {
            "fn": "+",
            "type": "arithmetic"
          },
          "currentSelect": {
            "dimension": "",
            "metric": ""
          },
          "customGranularity": "minute",
          "druidDS": "sensor_md_v0-1-1",
          "errors": {},
          "filters": [],
          "hide": false,
          "limit": 5,
          "postAggregators": [
            {
              "fields": [
                {
                  "fieldName": "t_value_3",
                  "type": "fieldAccess"
                },
                {
                  "fieldName": "tpm",
                  "type": "fieldAccess"
                }
              ],
              "fn": "/",
              "name": "avg_value_3",
              "type": "arithmetic"
            },
            {
              "fields": [
                {
                  "fieldName": "t_value_2",
                  "type": "fieldAccess"
                },
                {
                  "fieldName": "tpm",
                  "type": "fieldAccess"
                }
              ],
              "fn": "/",
              "name": "avg_value_2",
              "type": "arithmetic"
            },
            {
              "fields": [
                {
                  "fieldName": "t_value_1",
                  "type": "fieldAccess"
                },
                {
                  "fieldName": "tpm",
                  "type": "fieldAccess"
                }
              ],
              "fn": "/",
              "name": "avg_value_1",
              "type": "arithmetic"
            }
          ],
          "queryType": "timeseries",
          "refId": "B",
          "selectMetrics": [],
          "selectThreshold": 99,
          "shouldOverrideGranularity": true
        }
      ]
