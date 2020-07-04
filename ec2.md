aws ec2 describe-instances

aws ec2 describe-images --filters "Name=description, Values=Amazon Linux AMI * x86_64 HVM GP2" --query 'Images[*].[CreationDate, Description, ImageId]' --output text | sort -k 1 | tail

aws ec2 describe-vpcs

aws ec2 create-security-group \
--group-name $SECURITY_GROUP_NAME \
--description $DESCRIPTION_SECURITY_GROUP \
--vpc-id $VPC_ID

aws ec2 authorize-security-group-ingress \
--group-name $SECURITY_GROUP_NAME \
--protocol tcp \
--port 22 \
--cidr 0.0.0.0/0

aws ec2 describe-security-groups \
--group-names $SECURITY_GROUP_NAME
--output table

aws ec2 describe-subnets --output table

aws ec2 create-key-pair --key-name $KEY_NAME

aws ec2 run-instances \
--image-id ami-f09dcc9c \
--security-group-ids $SECURITY_GROUP_ID\
--instance-type t1.micro \
--key-name $KEY_NAME 

aws ec2 describe-instance-status --instance-ids $INSTANCE_ID

aws ec2 describe-instances \
--instance-ids $INSTANCE_ID \
--query "Reservations[*].Instances[*].PublicDnsName"

ssh -i $KEY_FILE ec2-user@$INSTANCE_PUBLIC_IP_ADDRESS

aws ec2 terminate-instances --instance-ids $INSTANCE_ID
