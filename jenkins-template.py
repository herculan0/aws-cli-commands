import os
from ipaddress import ip_network
from ipify import get_ip
from troposphere.iam import (
  InstanceProfile,
  PolicyType as IAMPolicy,
  Role,
)
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
from awacs.aws import (
  Action,
  Allow,
  Policy,
  Principal,
  Statement,
)
from awacs.sts import AssumeRole

PublicCidr = str(ip_network(get_ip()))

ApplicationName = "jenkins"
port = "8080"

GithubAccount = "herculan0"
GithubAnsibleURL = "https://github.com/{}/ansible".format(GithubAccount)

AnsiblePullCmd = \
        "/usr/local/bin/ansible-pull -U {} {}.yml -i localhost".format(
                GithubAnsibleURL,
                ApplicationName)


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
    "yum install --enablerepo=epel -y git",
    "pip install ansible",
    AnsiblePullCmd,
    "echo '*/10 * * * * {}' > /etc/cron.d/ansible-pull".format(AnsiblePullCmd)
]))

t.add_resource(Role(
    "Role",
    AssumeRolePolicyDocument=Policy(
        Statement=[
            Effect=Allow,
            Action=[AssumeRole],
            Principal=Principal("Service", ["ec2.amazonaws.com"])
            ]
        )
    )
)

t.add_resource(InstanceProfile(
    "InstanceProfile",
    Path="/",
    Roles=[Ref("Role")]
))

t.add_resource(ec2.Instance(
    "instance",
    ImageId="ami-f09dcc9c",
    InstanceType="t2.micro",
    SecurityGroups=[Ref("SecurityGroup")],
    KeyName=Ref("KeyPair"),
    UserData=ud,
    IamInstanceProfile=Ref("InstanceProfile")
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
