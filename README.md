# tr-064-honey
honeypot script to detect payload used in tr-064 iot exploitation

## usage
1. git clone this repo
2. sudo pip install -r requirements.txt
3. be sure to allow netowrk traffic `iptables -I INPUT -p tcp --dport 7547 -j ACCEPT` or so.
4. run `python ./tr-064-honey.py`
