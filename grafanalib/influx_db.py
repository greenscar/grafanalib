from influxdb import client as influxdb


class InfluxDB(object):
    session = None

    def __init__(self, host="test-influxdb.m3.ebay.com"):
        self.host = host
        self.port = 80
        self.username = "collectd_ro_account"
        self.password = "collectd_ro"
        self.database = "collectd"
        self.dbclient = influxdb.InfluxDBClient(self.host, self.port, self.username, self.password, self.database)
        print("##################################")
        print("INFLUXDB HOST: " + self.host)
        # Encrypt password

    def load_host_list(self):
        query_stmt = "SHOW TAG VALUES WITH KEY = host"
        result = self.dbclient.query(query_stmt)
        results = result._raw
        to_return = []

        print("---------------")
        print(results)
        print("---------------")
        for val in results['series'][0]['values']:
            to_return.append(val[0])
            print(val[0])
        print("---------------")
        return to_return
