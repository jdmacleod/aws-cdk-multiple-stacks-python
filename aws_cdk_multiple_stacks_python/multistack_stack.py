import aws_cdk as cdk
from aws_cdk import aws_s3 as s3
from constructs import Construct


class MultistackStack(cdk.Stack):
    """Define a multi-stack class that extends Stack.

    Args:
        cdk.Stack (_type_): an AWS CDK Stack
    """

    # The Stack class doesn't know about our encrypt_bucket parameter,
    # so accept it separately and pass along any other keyword arguments.
    def __init__(
        self, scope: Construct, id: str, *, encrypt_bucket=False, **kwargs
    ) -> None:
        """Initialize the Multistack instance.

        Args:
            scope (Construct): _description_
            id (str): _description_
            encrypt_bucket (bool, optional): Whether to provision the bucket with encryption. Defaults to False.
        """
        super().__init__(scope, id, **kwargs)

        # Add a Boolean property "encrypt_bucket" to the stack constructor.
        # If true, create an encrypted bucket. Otherwise, the bucket is unencrypted.
        # Encrypted bucket uses KMS-managed keys (SSE-KMS).
        if encrypt_bucket:
            s3.Bucket(
                self,
                "MyNewBucket",
                encryption=s3.BucketEncryption.KMS_MANAGED,
                removal_policy=cdk.RemovalPolicy.DESTROY,
            )
        else:
            s3.Bucket(self, "MyNewBucket", removal_policy=cdk.RemovalPolicy.DESTROY)
