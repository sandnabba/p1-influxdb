import sys
import logging
import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from smeterd.meter import SmartMeter

# Settings:
SERIAL_PORT = os.getenv("SERIAL_PORT")
SERIAL_BAUDRATE = os.getenv("SERIAL_BAUDRATE")
SERIAL_BYTESIZE = int(os.getenv("SERIAL_BYTESIZE"))
SERIAL_PARITY = os.getenv("SERIAL_PARITY")
SERIAL_STOPBITS = int(os.getenv("SERIAL_STOPBITS"))
SERIAL_XONXOFF = os.getenv("SERIAL_XONXOFF")
INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")

# Setup logging:
logging.basicConfig(format='%(levelname)s %(message)s')
#logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger("p1-influxdb")
log.setLevel("INFO")

meter = SmartMeter(
    SERIAL_PORT,
    baudrate=SERIAL_BAUDRATE, 
    bytesize=SERIAL_BYTESIZE,
    parity=SERIAL_PARITY,
    stopbits=SERIAL_STOPBITS,
    rts=True
)
client = InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG
)

write_api = client.write_api(write_options=SYNCHRONOUS)

log.debug("Entering infinite loop")
while True:
    try:
        log.debug("Waiting for packet")
        packet = meter.read_one_packet()

        log.info("Writing to InfluxDB")
        write_api.write(bucket=INFLUXDB_BUCKET, record=[
            Point("volt").field("l1", packet['instantaneous']['l1']['volts']),
            Point("volt").field("l2", packet['instantaneous']['l2']['volts']),
            Point("volt").field("l3", packet['instantaneous']['l3']['volts']),
            Point("current").field("l1", packet['instantaneous']['l1']['amps']),
            Point("current").field("l2", packet['instantaneous']['l2']['amps']),
            Point("current").field("l3", packet['instantaneous']['l3']['amps']),
            Point("consumption").field("now", packet['kwh']['consumed']['now']),
            Point("consumption").field("total", packet['kwh']['consumed']['total']),
            Point("total_consumption").field("total_consumed_active", packet['kwh']['consumed']['total']) # Old syntax
        ])
    except Exception as e:
        log.error("Exception while writing to InfluxDB")
        print(e)


