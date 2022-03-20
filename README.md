# carddav-to-yealink-remote-xml-addressbook

Convert CardDav contacts to Yealink xml, and serve it as remove phone book.

Simple server that can request vcf contacts from a carddav server such as nextcloud,
and serve it as xml for usage with Yealink SIP phones.


On your server:

```bash
cp example-config.yaml config.yaml
vim config.yaml
python main.py
```

To enable the remote contacts, on your phone's web interface:
- Directory / Remote Phone Book -> add URL, enable call lookup
- Directory / Settings -> Move Remote Phone Book to enabled sections


## Dependencies (e.g. on Debian)

```bash
apt install python3 (>= 3.6) python3-yaml (>= 5.1) python3-flask python3-waitress python3-lxml python3-vobject python3-requests
```


## Systemd service

```bash
cp carddav-to-yealink.service.example /etc/systemd/system/carddav-to-yealink.service
sed -i "s#%USER%#carddav_bridge#g; s#%PATH%#$PWD#g" /etc/systemd/system/carddav-to-yealink.service # change user and path to your needs

systemctl daemon-reload
systemctl start carddav-to-yealink.service
systemctl enable carddav-to-yealink.service
```


## Acknowledgements:

This project includes code found in following repos:

- https://github.com/ljanyst/carddav-util  
    License:
    ```
    Copyright (c) 2012 by Lukasz Janyst <ljanyst@buggybrain.net>

    Permission to use, copy, modify, and/or distribute this software for any
    purpose with or without fee is hereby granted, provided that the above
    copyright notice and this permission notice appear in all copies.

    THE SOFTWARE IS PROVIDED 'AS IS' AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
    ```
- https://gist.github.com/tsenger/ca4480235b5b29431965ee0b919ff6ad
