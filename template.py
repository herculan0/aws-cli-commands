import os
from ipaddress import ip_network
from ipify import get_ip
from troposphere import (
  Base64,
  ec2,
  GetAtt,
  Join,
  Output,
  Parameter,
  Ref,
  Template,
)
PublicCidr = str(ip_network(get_ip()))
port = "3000"

t = Template()

t.set_description("DevOps in AWS - HelloWorld application")

t.add_parameter(Parameter("KeyPair",
    Description="herculano_devops",
    Type="AWS::EC2::KeyPair::KeyName",
    ConstraintDescription="herculano_devops",
))

t.add_resource(ec2.SecurityGroup(
    "SecurityGroup",
    GroupDescription="Allow SSH and TCP/ {} access".format(port),
    SecurityGroupIngress=[
        ec2.SecurityGroupRule(
            IpProtocol="tcp",
            FromPort="22",
            ToPort="22",
            CidrIp=PublicCidr
            ),
        ec2.SecurityGroupRule(
            IpProtocol="tcp",
            FromPort=port,
            ToPort=port,
            CidrIp="0.0.0.0/0"
            ),
        ],
    )
)

ud = Base64(Join('\n', [
    "#!/bin/bash",
    "yum install --enablerepo=epel -y nodejs",
    "wget http://bit.ly/2vESNuc -O /home/ec2-user/helloworld.js",
    "wget http://bit.ly/2vVvT18 -O /etc/init/helloworld.conf",
    "start helloworld"
]))


t.add_resource(ec2.Instance(
    "instance",
    ImageId="ami-f09dcc9c",
    InstanceType="t1.micro",
    SecurityGroups=[Ref("SecurityGroup")],
    KeyName=Ref("KeyPair"),
    UserData=ud,
))

t.add_output(Output(
    "Instance",
    Description="Public Ip of our instance.",
    Value=GetAtt("instance", "PublicIp"),
))

t.add_output(Output(
    "WebUrl",
    Description="Application endpoint",
    Value=Join("", [
        "http://", GetAtt("instance", "PublicDnsName"),
        ":", port]),
))

print(t.to_json())
