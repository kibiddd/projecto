#  Install the Python ScrapingBee library:
# pip install scrapingbee
from scrapingbee import ScrapingBeeClient

client = ScrapingBeeClient(api_key='JHQI99AYJX46AGYOYL2XQV5J6LE297I19N0E4OAXHW6S09NJ0W4FW61YAW3FKP5IZAEG4ADF9S3XQXI8')

response = client.get(
    'https://cyberfraudlawyers.com/',
    params={
        'screenshot_full_page': True
    }
)

if response.ok:
    with open("./screenshot-scam.png", "wb") as f:
        f.write(response.content)