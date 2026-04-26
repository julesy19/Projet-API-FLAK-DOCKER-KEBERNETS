import boto3
from botocore.exceptions import ClientError
from datetime import date

session = boto3.Session()


# ------------------ COSTS ------------------
def get_costs():
    ce = session.client("ce", region_name="us-east-1")

    today = date.today()
    start = today.replace(day=1).strftime("%Y-%m-%d")
    end = today.strftime("%Y-%m-%d")

    response = ce.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
    )

    costs = []

    for group in response["ResultsByTime"][0]["Groups"]:
        service = group["Keys"][0]
        amount = group["Metrics"]["UnblendedCost"]["Amount"]

        costs.append({
            "service": service,
            "cost": round(float(amount), 2)
        })

    return costs


# ------------------ MAIN SCAN ------------------
def scan_all():

    data = {
        "iam_users": [],
        "s3_buckets": [],
        "ec2_instances": [],
        "rds": [],
        "lambda": [],
        "vpcs": [],
        "ecr": [],
        "eks": [],
        "cloudwatch": [],
        "costs": []
    }

    # -------- IAM --------
    iam = session.client("iam")
    users = iam.list_users()

    for user in users["Users"]:
        username = user["UserName"]

        mfa = iam.list_mfa_devices(UserName=username)

        data["iam_users"].append({
            "username": username,
            "mfa": "ENABLED" if mfa["MFADevices"] else "DISABLED"
        })

    # -------- S3 --------
    s3 = session.client("s3")
    buckets = s3.list_buckets()

    for b in buckets["Buckets"]:
        data["s3_buckets"].append(b["Name"])

    # -------- REGIONS --------
    ec2_global = session.client("ec2", region_name="us-east-1")
    regions = ec2_global.describe_regions()

    for r in regions["Regions"]:
        region = r["RegionName"]

        # EC2
        ec2 = session.client("ec2", region_name=region)
        try:
            instances = ec2.describe_instances()
            for res in instances["Reservations"]:
                for i in res["Instances"]:
                    data["ec2_instances"].append({
                        "id": i["InstanceId"],
                        "state": i["State"]["Name"],
                        "region": region
                    })
        except ClientError:
            pass

        # RDS
        rds = session.client("rds", region_name=region)
        try:
            dbs = rds.describe_db_instances()
            for db in dbs["DBInstances"]:
                data["rds"].append({
                    "id": db["DBInstanceIdentifier"],
                    "region": region
                })
        except ClientError:
            pass

        # Lambda
        lam = session.client("lambda", region_name=region)
        try:
            functions = lam.list_functions()
            for f in functions["Functions"]:
                data["lambda"].append({
                    "name": f["FunctionName"],
                    "region": region
                })
        except ClientError:
            pass

        # VPC
        try:
            vpcs = ec2.describe_vpcs()
            for v in vpcs["Vpcs"]:
                data["vpcs"].append({
                    "id": v["VpcId"],
                    "region": region
                })
        except ClientError:
            pass

        # -------- ECR --------
        ecr = session.client("ecr", region_name=region)
        try:
            repos = ecr.describe_repositories()
            for repo in repos["repositories"]:
                data["ecr"].append({
                    "name": repo["repositoryName"],
                    "uri": repo["repositoryUri"],
                    "region": region
                })
        except ClientError:
            pass

        # -------- EKS --------
        eks = session.client("eks", region_name=region)
        try:
            clusters = eks.list_clusters()
            for cluster_name in clusters["clusters"]:
                details = eks.describe_cluster(name=cluster_name)

                data["eks"].append({
                    "name": cluster_name,
                    "status": details["cluster"]["status"],
                    "version": details["cluster"]["version"],
                    "region": region
                })
        except ClientError:
            pass

        # -------- CloudWatch --------
        cw = session.client("cloudwatch", region_name=region)
        try:
            metrics = cw.list_metrics(Namespace="AWS/EC2")

            data["cloudwatch"].append({
                "region": region,
                "metrics_count": len(metrics["Metrics"])
            })
        except ClientError:
            pass

    # -------- COSTS --------
    data["costs"] = get_costs()

    return data