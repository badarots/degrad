FROM grafana/grafana:11.0.0

# Add provisioning
ADD ./provisioning /etc/grafana/provisioning
# Add configuration file
ADD ./grafana.ini /etc/grafana/grafana.ini
# Add dashboard json files
ADD ./dashboards /etc/grafana/dashboards
