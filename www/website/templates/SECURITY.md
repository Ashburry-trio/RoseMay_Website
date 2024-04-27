# Security Policy

## Supported Versions

Right now there is no released versions, however if you find
a security vulnerability then it will be assumed to be
in either mIRC Script (Machine Gun script named Bauderr) or proxy-server
(Trio-ircproxy) or web-server (named RoseMay) all under one version (11.01.15)

| Version         | Supported          |
| --------------- | ------------------ |
| PEACE-3.0       | :white_check_mark: |
| >= MiNDneT-4.13 | :x:                |

## Reporting a Vulnerability

To report a vulnerability you may create an issue at
https://github.com/ashburry-trio/Ircproxy/issues
or send an email to mailto:ashburryop@gmail.com
or lastely find me on ***IRC*** in ***#5ioE*** on ***Undernet*** and speak
in the channel.

If your reported vulnerability is received I will create an Issue at
https://github.com/ashburry-trio/Ircproxy/issues as soon as
it is received. This new Issue should be created within 24hrs of the
report. If you leave an ***email address*** or contact ***nickname*** on ***IRC***\
I will message you back with a statement stating the vulnerability has
been reported successfully, and is being investiaged, and will be fixed in
the next version (and maybe not fixed).

Vulnerabilities in the irc clients mIRC and Adiirc can also be protected against
maliicious messages by filtering incomming messages from the irc-server to the
proxy-server (filter here) to the irc-client. One exploit is being protected against
by filtering binary data in the irc-protocol text (not the message-text).

Also, there is (will be) protection against sensitive website, nickname and channel passwords
from being leaked in to public chat space. A leaked password message will be blocked for your protection.

* End of document.
