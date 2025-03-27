#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws_cdk_multiple_stacks_python.multistack_stack import MultistackStack

app = cdk.App()

MultistackStack(
    app,
    "MyWestCdkStack",
    env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region="us-west-1"),
    encrypt_bucket=False,
)

MultistackStack(
    app,
    "MyEastCdkStack",
    env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region="us-east-1"),
    encrypt_bucket=True,
)

app.synth()
