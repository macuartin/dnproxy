# dnproxy
[![python](https://img.shields.io/badge/python-v3.9.1-green.svg)](https://www.python.org/)
[![pip](https://img.shields.io/badge/pip-v21.0.1-yellow.svg)](https://pypi.org/project/pip/)
[![virtualenv](https://img.shields.io/badge/virtualenv-v20.4.2-red.svg)](https://virtualenv.pypa.io/en/stable/)

dnproxy is a tool that allows applications to query a DNS-over-TLS server.

dnproxy handle TCP and UDP requests and allow multiple incoming requests at the same time. All this possible thanks to the joint use of the socket and dns libraries.

dnproxy creates two sockets, one for each protocol implemented and using the selectors module it evaluates the type of socket that receives the request and thus can handle the message appropriately according to the communication protocol with which it was sent.

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

Note: For Docker implementation it's recommended use 0.0.0.0 as dnproxy.host

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

## Security and Architecture Concerns

Imagining that dnproxy will be deployed in the public cloud and will be integrated into a solution with a distributed and microservices-oriented architecture, the following implementation is proposed:

1. Deploying dnproxy as a isolate service in a private subnet with the following security group rules:

| type | from_port | to_port | protocol | source/destination |
| ------ | ------ | ------ | ------ | ------ |
| egress | 0 | 0 | -1 | 0.0.0.0/0 |
| ingress | dnproxy.port | dnproxy.port | tcp | backend security groups |
| ingress | dnproxy.port | dnproxy.port | udp | backend security groups |

I think that with these rules you have the minimum access so that the rest of the services can use dnproxy and dnproxy can send request to others DNS.

2. dnproxy is containerized so it could be deployed in any kubernetes cluster under a LoadBalancer service, using a DNS like AWS route53, the LoadBalancer could be registered so that dnproxy can be used under a specific domain for the rest of the microservices. Being in a K8S cluster it could scale according to the cluster parameters.

## Future improvements

* Helm Chart to K8S deploy.
* Enable DNS over HTTPS (DoH).

## Contributing

To contribute to dnproxy, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contact

If you want to contact me you can reach me at <macuartin@gmail.com>.
