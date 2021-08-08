## HOW TO make elasticsearch_exporter on centos-7:
yum  -y install golang
GOPATH=/usr/local go get -u github.com/justwatchcom/elasticsearch_exporter

## RUN:
cat << EOF > /etc/systemd/system/elasticsearch_exporter.service
[Unit]
Description=Prometheus elasticsearch_exporter
After=local-fs.target network-online.target network.target
Wants=local-fs.target network-online.target network.target

[Service]
User=root
Nice=10
ExecStart = /usr/local/bin/elasticsearch_exporter -es.all -es.indices -es.timeout 20s
ExecStop= /usr/bin/killall elasticsearch_exporter

[Install]
WantedBy=default.target
EOF

systemctl daemon-reload
systemctl enable elasticsearch_exporter.service
systemctl start  elasticsearch_exporter.service


## Exampe config for prometheus.yml:
  - job_name: elasticsearch
    scrape_interval: 60s
    scrape_timeout:  30s
    metrics_path: "/metrics"
    static_configs:
    - targets:
      - elastic2.test.lan:9108
      - elastic-log2.prod.lan:9108
      labels:
        service: elasticsearch
    relabel_configs:
    - source_labels: [__address__]
      regex: '(.*)\:9108'
      target_label:  'instance'
      replacement:   '$1'
    - source_labels: [__address__]
      regex:         '.*\.(.*)\.lan.*'
      target_label:  'environment'
      replacement:   '$1'
