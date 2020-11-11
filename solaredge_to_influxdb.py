#!/usr/bin/env python3

import os
import datetime
import yaml
import influxdb
from solaredge import SolarEdge


def main():
    cwd = os.path.dirname(os.path.abspath(__file__))
    config_path = f'{cwd}{os.path.sep}config.yaml'

    config = None
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    if config is not None:
        solaredge = SolarEdge(
            url=config['solaredge']['url'],
            site=config['solaredge']['site'],
            api_key=config['solaredge']['api_key']
        )
        data = solaredge.get_overview()

        tags = config['influxdb']['tags']
        fields = {}

        # Cumulative data
        if 'lifeTimeData' in data['overview']:
            for k, v in data['overview']['lifeTimeData'].items():
                fields[f'cumulative_{k}'] = v

        # Instant data
        if 'currentPower' in data['overview']:
            for k, v in data['overview']['currentPower'].items():
                fields[f'instant_{k}'] = v

        # Prepare data for influxdb
        if len(fields) > 0:
            output_data = {
                'time': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
                'measurement': 'solaredge',
                'tags': tags,
                'fields': fields,
            }
        else:
            print('No data fields present!')
            exit(1)

        # Send to influxdb
        influxdb_client = influxdb.InfluxDBClient(**config['influxdb']['influxdbclient'])
        influxdb_client.write_points([output_data])


if __name__ == "__main__":
    main()
