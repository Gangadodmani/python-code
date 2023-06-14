import time
import boto3

# AWS Credentials and Region
aws_access_key_id = 'AKIATM3ZJ4VE4C7ZYLMJ'
aws_secret_access_key = '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'
region_name = 'ap-south-1'

# ASG Configuration
asg_name = 'lv-test-cpu'
desired_capacity = 2  # Desired minimum number of instances in the ASG

# CPU Utilization Thresholds for Test Cases
test_case_a_threshold = 80  # Percentage
test_case_b_threshold = 20  # Percentage

# Initialize AWS clients
autoscaling = boto3.client('autoscaling', region_name=region_name)
cloudwatch = boto3.client('cloudwatch', region_name=region_name)


def verify_test_case_a():
    print("Verifying Test Case A - Scaling Out")
    # Trigger load simulation or run your workload to exceed the CPU threshold
    # Monitor CPU utilization using CloudWatch or other monitoring tools
    # Ensure the ASG scales out by adding instances to meet the increased load
    # Wait for scaling activities to complete
    while True:
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'AutoScalingGroupName', 'Value': asg_name}],
            StartTime=time.time() - 300,  # Look back 5 minutes
            EndTime=time.time(),
            Period=60,
            Statistics=['Average']
        )
        datapoints = response['Datapoints']
        if datapoints:
            average_cpu = datapoints[-1]['Average']
            if average_cpu >= test_case_a_threshold:
                print("Test Case A Passed - ASG scaled out successfully.")
                break
        time.sleep(60)  # Wait for 1 minute before checking again


def verify_test_case_b():
    print("Verifying Test Case B - Scaling In")
    # Reduce the load or simulate reduced load to lower the CPU utilization
    # Monitor CPU utilization using CloudWatch or other monitoring tools
    # Ensure the ASG scales in by terminating instances to match the reduced load
    # Wait for scaling activities to complete
    while True:
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'AutoScalingGroupName', 'Value': asg_name}],
            StartTime=time.time() - 300,  # Look back 5 minutes
            EndTime=time.time(),
            Period=60,
            Statistics=['Average']
        )
        datapoints = response['Datapoints']
        if datapoints:
            average_cpu = datapoints[-1]['Average']
            if average_cpu <= test_case_b_threshold:
                print("Test Case B Passed - ASG scaled in successfully.")
                break
        time.sleep(60)  # Wait for 1 minute before checking again


def main():
    # Set the desired capacity to ensure the minimum number of instances in the ASG
    autoscaling.set_desired_capacity(
        AutoScalingGroupName=asg_name,
        DesiredCapacity=desired_capacity
    )

    # Verify Test Case A
    verify_test_case_a()

    # Verify Test Case B
    verify_test_case_b()

    # Restore desired capacity
    autoscaling.set_desired_capacity(
        AutoScalingGroupName=asg_name,
        DesiredCapacity=desired_capacity
    )
    
if __name__ == '__main__':
    main()
