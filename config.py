# The default_config module automatically gets imported by Appconfig, if it
# exists. See https://pypi.python.org/pypi/flask-appconfig for details.

# Note: Don't *ever* do this in a real app. A secret key should not have a
#       default, rather the app should fail if it is missing. For the sample
#       application, one is provided for convenience.
SECRET_KEY = 'devkey'
PROC_DIR = "/sys/devices/soc0/amba"
MODULES_PATH = "modules.json"
ADDRESSES_PATH = "addresses.csv"

DATA_FILE_PATH = "/mnt/emmc"
DATA_FILE_EXTENSION = "elmg"

LOG_FILE_PATH = "/mnt/emmc"
LOG_FILE_EXTENSION = "log"


START_SCRIPT = "/mnt/emmc/go.sh"
STOP_SCRIPT = "/mnt/emmc/stop.sh"
DTCON_SCRIPT = "/mnt/emmc/dtcon.sh"
DTCOFF_SCRIPT = "/mnt/emmc/dtcoff.sh"
PSNC_SCRIPT = "/mnt/emmc/poscont.sh"
SPDC_SCRIPT = "/mnt/emmc/spdcont.sh"
DLOG_SCRIPT = "/mnt/emmc/dloghf.elf -k -n &"
