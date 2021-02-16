# dnproxy
[![python](https://img.shields.io/badge/python-v3.9.1-green.svg)](https://www.python.org/)
[![pip](https://img.shields.io/badge/pip-v21.0.1-yellow.svg)](https://pypi.org/project/pip/)
[![virtualenv](https://img.shields.io/badge/virtualenv-v20.4.2-red.svg)](https://virtualenv.pypa.io/en/stable/)

dnproxy is a tool that allows applications to query a DNS-over-TLS server.

dnproxy handle TCP and UDP requests and allow multiple incoming requests at the same time.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed the latest version of [Python](https://www.python.org/downloads/).
* You have installed the latest version of [Docker](https://docs.docker.com/engine/install/).
* You have installed the latest version of [kdig](https://www.knot-dns.cz/docs/2.6/html/man_kdig.html) or other DNS lookup utility.

## Build and Usage

### Docker

To use dnproxy as docker container, follow these steps:

Build docker image:
```bash
docker build -t dnproxy .
```

Run docker container:
```bash
docker run -d -p 53:53 -p 53:53/udp dnproxy
```

If you want use this image to deploy on K8S cluster then push it on dockerhub or  the registry that you like better:
```bash
docker tag <IMAGE ID> <HUB USERNAME>/dnproxy:latest
docker push <IMAGE ID> <HUB USERNAME>/dnproxy
```

### Script

To use dnproxy as script, follow these steps:

Install requirements:
```bash
pip3 install -r requirements.txt
```

Run script:
```bash
python3 dnproxy.py
```

### Custom configs

if you want to customize dnproxy configurations then you can edit the dnproxy.yml file.

The dnproxy.yml file required the follow params:

| Param | Type | Description |
| ------ | ------ | ------ |
| dnproxy.host | str | a str containing an IPv4 address to accept connections on from clients |
| dnproxy.port | int | it’s the TCP port number to accept connections on from clients |
| upstream.ip | str | a str containing an IPv4 or IPv6 address, where to send the message |
| upstream.hostname | str | a str containing the server’s hostname. |


## Check service

if you want to check if dnproxy is working you can use netstat and check if are some active socket over 53 port.

```bash
netstat -an | grep 53
```

Use a DNS Lookup Utility as kdig to test your dnproxy implementation:
```bash
kdig @<CONTAINER IP> -t A google.com
kdig @<CONTAINER IP> -t A google.com +tcp
```
if you are running dnproxy locally then CONTAINER IP will be 127.0.0.1

## Contributing

To contribute to <project_name>, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Further reading / Useful links

* Lorem ipsum dolor sit amet, consectetur adipiscing elit.
* Lorem ipsum dolor sit amet, consectetur adipiscing elit.

## Contact

If you want to contact me you can reach me at <your_email@address.com>.

## License
<!--- If you're not sure which open license to use see https://choosealicense.com/--->

This project uses the following license: [<license_name>](<link>).
