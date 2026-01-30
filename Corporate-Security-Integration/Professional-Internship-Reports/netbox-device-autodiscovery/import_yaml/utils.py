import re

def format_slug(text):
    """Convertit une chaîne en slug lisible par NetBox (ex: Cisco Switch → cisco-switch)"""
    slug = re.sub(r'[^a-zA-Z0-9-]+', '-', text.strip().lower())
    return slug.strip('-')

def format_mac(mac):
    mac = mac.lower().replace('.', '').replace('-', '').replace(':', '')
    return ':'.join(mac[i:i+2] for i in range(0, 12, 2))
