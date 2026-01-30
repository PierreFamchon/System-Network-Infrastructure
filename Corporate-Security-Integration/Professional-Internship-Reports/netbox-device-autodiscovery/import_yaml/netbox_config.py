# netbox_config.py
NETBOX_URL = "http://192.168.100.160:8000/api/"
NETBOX_TOKEN = "04946ef59ffeb57bc7a0e7c6ac73f787eb272c57"

HEADERS = {
    "Authorization": f"Token {NETBOX_TOKEN}",
    "Content-Type": "application/json",
}
DEBUG_MODE = True
