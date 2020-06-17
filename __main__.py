import os
from cfn_flip import to_json
import json

import pulumi
from pulumi_aws import s3
from pulumi_aws import cloudwatch

def make_metric_filter(name, _log_group_name, properties):
    y=properties['FilterPattern']
    tmp_metric_transf = properties['MetricTransformations'][0]
    z= {
        'name' : tmp_metric_transf['MetricName'],
        'namespace' : tmp_metric_transf['MetricNamespace'],
        'value' : tmp_metric_transf['MetricValue']
    }

    # Docs https://www.pulumi.com/docs/reference/pkg/aws/cloudwatch/logmetricfilter/
    log_metric_filter = cloudwatch.LogMetricFilter(name,
        log_group_name=_log_group_name,
        pattern=y,
        metric_transformation=z
    )
    
    # Logging in Pulumi
    pulumi.log.info(f"Hello World! I'm a log statement")


def read_yaml():
    try:
        with open("CIS.yaml", "rb") as stream:
            yaml_string = stream.read().strip()
            cis_doc = to_json(yaml_string)
            return json.loads(cis_doc)
    except:
        print("Uh Oh, looks like something went wrong during demo")

def main():
    # Do what you would typically do in Python!
    cis_document = read_yaml()

    # Log Group
    log_group = cloudwatch.LogGroup("CISComplianceLogGroup")

    # Careful not to create too many resources! xD
    for key, value in cis_document['Resources'].items():
        if value['Type'] == 'AWS::Logs::MetricFilter':
            make_metric_filter(key, log_group.name, value['Properties'])

if __name__ == "__main__":
    main()