# Multiple Stacks AWS CDK Tutorial - Python

<https://docs.aws.amazon.com/cdk/v2/guide/stack_how_to_create_multiple_stacks.html>

You can create an AWS Cloud Development Kit (AWS CDK) application containing multiple stacks. When you deploy the AWS CDK app, each stack becomes its own AWS CloudFormation template. You can also synthesize and deploy each stack individually using the AWS CDK CLI cdk deploy command.

1. Create the CDK project

   - Create the project directory

    ```bash
    mkdir aws-cdk-multiple-stacks-python
    cd aws-cdk-multiple-stacks-python
    ```

   - Initialize a new CDK project (Python)

    ```bash
    cdk init app --language python
    ```

    This generates the skeleton files for the project. If Git is detected, then the project directory is also initialized as a Git repository.

    See [REFERENCE.md](./REFERENCE.md) for the skeleton README file.

    Update [requirements-dev.txt](./requirements-dev.txt) to add [Astral ruff](https://docs.astral.sh/ruff/), [pytest-cov](https://pypi.org/project/pytest-cov/), and [Git pre-commit](https://pre-commit.com/)

    Activate the Python virtual environment and install the requirements.

    ```bash
    source .venv/bin/activate
    which python   # check python location
    python -V   # check python version
    python -m pip install -r requirements.txt
    python -m pip install -r requirements-dev.txt
    ```

    Install the Git pre-commit hooks - see [.pre-commit-config.yaml](./.pre-commit-config.yaml)

    ```bash
    pre-commit install
    ```

    Add [pyproject.toml](./pyproject.toml) to configure `ruff`.

    The project is now set up for development and testing.

2. Configure the AWS environment

    We will use `CDK_DEFAULT_ACCOUNT` that is provided by the `cdk` command. The region will be specified directly in the stack declarations.

3. Bootstrap the AWS environment (as Admin role) (needed once for each region)

    This example uses regions `us-east-1` and `us-west-1`, so we have to run the bootstrap command in each region as Administrator (if it has never been run in a given region).

    The AWS `config` and `credentials` files were edited to add `admin-us-east-1` and `admin-us-west-1` entries.

    ```bash
    cdk --profile admin-us-east-1 bootstrap
    ...
    [15:04:22] Stack CDKToolkit has completed updating
    ✅  Environment aws://223088417222/us-east-1 bootstrapped.

    cdk --profile admin-us-west-1 bootstrap
    ...
    [15:06:10] CDKToolkit: skipping deployment (use --force to override)
    ✅  Environment aws://223088417222/us-west-1 bootstrapped (no changes).
    ```

    The privileges needed for bootstrap exceed 'PowerUser'. To get this step to work, I used the Administrator role with AdministratorAccess Policy.

    See
    <https://stackoverflow.com/questions/57118082/what-iam-permissions-are-needed-to-use-cdk-deploy>
    and
    <https://stackoverflow.com/questions/71848231/must-cdk-bootstrapping-be-done-by-a-user-with-admin-access?noredirect=1&lq=1>

4. Build the CDK app (not needed for Python)
5. List the CDK stacks in the app

    ```bash
    cdk list
    MyWestCdkStack
    MyEastCdkStack
    ```

6. Define two stacks in the app

    In this example, two different stacks are defined, making use of the extended MultistackStack() class.

    In [app.py](./app.py):

    ```python
        # define the App, and declare two different Stacks.
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
    ```

7. Synthesize a CloudFormation template for each Stack (East, West)

    ```bash
    cdk synth MyEastCdkStack
    cdk synth MyWestCdkStack
    ```

    Outputs a YAML template with the parameters for each Stack in the app.

8. Deploy the East CDK stack

    Deploy the app, accepting/confirming any changes if prompted.

    ```bash
    cdk deploy MyEastCdkStack
    ...
    MyEastCdkStack: deploying... [1/1]
    MyEastCdkStack: creating CloudFormation changeset...

    ✅  MyEastCdkStack

    ✨  Deployment time: 30.88s

    Stack ARN:
    arn:aws:cloudformation:us-east-1:223088417222:stack/MyEastCdkStack/f96d3730-0b57-11f0-aa31-0e0abc6004d9

    ✨  Total time: 37.02s
    ```

9. Check that the AWS S3 Bucket was created for the East Stack.

    List S3 buckets.

    ```bash
    aws s3 ls
    2025-03-27 15:03:49 cdk-hnb659fds-assets-223088417222-us-east-1
    2025-03-27 15:03:46 cdk-hnb659fds-assets-223088417222-us-west-1
    2025-03-26 16:38:15 cdk-hnb659fds-assets-223088417222-us-west-2
    2025-03-27 15:08:25 myeastcdkstack-mynewbucket15ca675a-eyqstmi0zjmo
    ```

    Check the encryption for the 'East' bucket.

    ```bash
    % aws s3api get-bucket-encryption --bucket myeastcdkstack-mynewbucket15ca675a-eyqstmi0zjmo --output text
    RULES   False
    APPLYSERVERSIDEENCRYPTIONBYDEFAULT      aws:kms
    ```

10. Deploy the West CDK stack

    Deploy the app, accepting/confirming any changes if prompted.

    ```bash
    cdk deploy MyWestCdkStack
    ...
    MyWestCdkStack: deploying... [1/1]
    MyWestCdkStack: creating CloudFormation changeset...

    ✅  MyWestCdkStack

    ✨  Deployment time: 27.08s

    Stack ARN:
    arn:aws:cloudformation:us-west-1:223088417222:stack/MyWestCdkStack/fbfcf7e0-0b59-11f0-8712-067194afe31d

    ✨  Total time: 33.43s
    ```

11. Check that the AWS S3 Bucket was created for the West Stack.

    List S3 buckets.

    ```bash
    aws s3 ls
    2025-03-27 15:03:49 cdk-hnb659fds-assets-223088417222-us-east-1
    2025-03-27 15:03:46 cdk-hnb659fds-assets-223088417222-us-west-1
    2025-03-26 16:38:15 cdk-hnb659fds-assets-223088417222-us-west-2
    2025-03-27 15:08:25 myeastcdkstack-mynewbucket15ca675a-eyqstmi0zjmo
    2025-03-27 15:22:47 mywestcdkstack-mynewbucket15ca675a-ti2uqdiqgykw
    ```

    Check the encryption for the 'West' bucket.

    ```bash
    % aws s3api get-bucket-encryption --bucket mywestcdkstack-mynewbucket15ca675a-ti2uqdiqgykw --output text
    RULES   False
    APPLYSERVERSIDEENCRYPTIONBYDEFAULT      AES256
    ```

12. Clean up the Stacks from East and West regions.

    Destroy the East Stack.

    ```bash
        cdk destroy MyEastCdkStack
        Are you sure you want to delete: MyEastCdkStack (y/n)? y
        MyEastCdkStack: destroying... [1/1]

        ✅  MyEastCdkStack: destroyed
    ```

    Destroy the West Stack.

    ```bash
        cdk destroy MyWestCdkStack
        Are you sure you want to delete: MyWestCdkStack (y/n)? y
        MyWestCdkStack: destroying... [1/1]

        ✅  MyWestCdkStack: destroyed
    ```

    Confirm the S3 buckets for East and West Stacks have been removed. The CDK bootstrap bucket for each region will remain, unless explicitly removed, possibly using the AWS Console.

    ```bash
        aws s3 ls
        2025-03-27 15:03:49 cdk-hnb659fds-assets-223088417222-us-east-1
        2025-03-27 15:03:46 cdk-hnb659fds-assets-223088417222-us-west-1
        2025-03-26 16:38:15 cdk-hnb659fds-assets-223088417222-us-west-2
    ```
