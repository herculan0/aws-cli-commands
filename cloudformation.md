aws cloudformation create-stack --capabilities CAPABILITY_IAM --stack-name $STACK_NAME --template-body file://$TEMPLATE_FILE --parameters ParameterKey=KeyPair,ParameterValue=$KEY_NAME
