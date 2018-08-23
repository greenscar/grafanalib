import itertools

from grafanalib.core import *


dashboard = Dashboard(
  title="jstest dashboard title",
  rows=[
    Row(
        title="jstest row title",
        panels=[
      Graph(
        title="jstest graph title",
        dataSource='collectd',
        targets=[
          TargetInfluxDB(
            query='SELECT mean(value) FROM cpu_value WHERE "host" = \'pbp1mi832-09.m3.ebay.com\' AND type = \'cpu\' AND type_instance = \'system\' AND $timeFilter GROUP BY time($interval) fill(null)',
            resultFormat='time_series',
            dsType='influxdb',
            alias='cpu system',
            legendFormat="1xx",
            refId='A',
          )
        ],
        yAxes=[
          YAxis(format=OPS_FORMAT),
          YAxis(format=SHORT_FORMAT),
        ]
      ),
    ]),
  ],
).auto_panel_ids()