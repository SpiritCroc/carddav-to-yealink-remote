#!/usr/bin/env python3

import yaml
from flask import Flask, Response, request, abort
from waitress import serve

from util import relative_path as rp
from carddav import PyCardDAV
from convert import vcf_to_xml

with open(rp('config.yaml')) as fin:
    config = yaml.full_load(fin)

def get_contacts():
    cdv = PyCardDAV(config["dav_url"], user=config["dav_user"], passwd=config["dav_passwd"])
    vcf = cdv.get_vcard(config["vcf_remote_path"]).decode()
    xml = vcf_to_xml(config, vcf)
    return xml


app = Flask("vcard-xml-bridge")

@app.route(config["listen_path"], methods=['GET'])
def request_get():
    ip_addr = request.remote_addr
    if "ip_whitelist" in config and ip_addr not in config["ip_whitelist"]:
        print(f"Contacts requested by {ip_addr}, but not whitelisted - return 404!")
        abort(404)
    print(f"Contacts requested by {ip_addr}, requesting from carddav...")
    contacts = get_contacts()
    print(f"Return xml contacts to {ip_addr}")
    return Response(contacts, mimetype="text/xml")

host = config["listen_host"]
port = config["listen_port"]
print(f"Starting listening on {host}, port {port}")
serve(app, host = host, port = port)
