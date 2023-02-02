### Stept to install the P1-influxdb script

# 1. Install Dependencies (From a plain Raspian install)
apt install python3-venv git

# 2. Clone code
git clone https://github.com/sandnabba/p1-influxdb.git /opt/p1-influxdb

# 3. Deploy Python virtual environment and install dependencies
cd /opt/p1-influxdb
python3 -m venv .
./bin/pip install -r requirements.txt

# 4. Install systemd unit file
cp p1-influxdb.service /etc/systemd/system/
systemctl enable p1-influxdb

# 5. Create configuration:
cp env_example .env

# 6. Edit configuration and start application
# systemctl start p1-influxdb

