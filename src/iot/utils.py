# yourapp/utils.py
VALID_API_KEYS = {
    "abc123": "device01",
    "xyz789": "device02",
}

def is_valid_apikey(apikey, device_id):
    return VALID_API_KEYS.get(apikey) == device_id
