import os
import json
import logging
from pysitemapgen import Sitemap
import requests
import msal
from firebase import DatabaseWorker
from pages_generator import PageGenerator


# Optional logging
# logging.basicConfig(level=logging.DEBUG)

config = json.load(open("parameters.json"))
secret = json.load(open("secret.json"))
config.update(secret)

# Create a preferably long-lived app instance which maintains a token cache.
app = msal.ConfidentialClientApplication(
    config["client_id"], authority=config["authority"],
    client_credential=config["secret"],
    # token_cache=...  # Default cache is in memory only.
                       # You can learn how to use SerializableTokenCache from
                       # https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
    )

# The pattern to acquire a token looks like this.
result = None

# Firstly, looks up a token from cache
# Since we are looking for token for the current app, NOT for an end user,
# notice we give account parameter as None.
result = app.acquire_token_silent(config["scope"], account=None)

if not result:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config["scope"])


if "access_token" in result:
    print(result['access_token'])
    # Calling graph using the access token
    graph_data = requests.get(  # Use token to call downstream service
        config["endpoint"],
        headers={'Authorization': 'Bearer ' + result['access_token']}, ).json()
    print("Graph API call result: ")
    # print(json.dumps(graph_data, indent=2))
    print("columnCount", graph_data["address"], graph_data['columnCount'])
    # with open('items.json', 'w') as fp:
    #     json.dump(graph_data['text'], fp)
    pg = PageGenerator(graph_data['text'])
    pg.parse_pages()
    pg.get_main_page()
    pg.generate_deploy_pages()
    print(pg.deploy_pages_count())
    # pg.deploy_pages_clear()
    # pg.generate_deploy_pages_mix()
    # print(pg.deploy_pages_count())
    # pg.save_pages_json()

    # dw = DatabaseWorker()
    # dw.send_data_to_db(pg.get_deploy_pages())

    

    sm=Sitemap(changefreq='weekly', sitemap_url='https://{0}/'.format(config["sitemap_domain"]))

    for x in pg.get_deploy_pages():
        sm.add('https://{0}/{1}/{2}'.format(config["sitemap_domain"], "remont", "/".join(x['slug'])),
                changefreq='daily',
                priority=0.7,
                lastmod='2021-27-07')

    sm.write('sitemap')
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You may need this when reporting a bug

