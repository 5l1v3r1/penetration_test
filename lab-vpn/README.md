## Description
`lab-vpn.py` helps to automate the openvpn connection for the InfoSec labs (i.e. PWK / CTP / WAPTx).

### Usage
```
usage: lab-vpn.py [-h] -p  -c  -e  -t  [-d]

automate the openvpn lab connection

optional arguments:
  -h, --help            show this help message and exit
  -p , --vpn_credential 
                        provide vpn credential in a json file
  -c , --config         provide a ovpn file for the lab
  -e , --email_credential 
                        provide email credential in a json file
  -t , --email_to       provide a email to send the notification
  -d , --set_dns        set the dns entry into resolv.conf


sample:
python lab-vpn.py -p asinha_waptx_creds.json -c XSS_11_challenging_labs_320.ovpn -e asinha_emailFrom_creds.json -t asinha@apple.com -d 10.100.13.37

```


 


