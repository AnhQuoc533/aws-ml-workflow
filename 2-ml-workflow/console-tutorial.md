<h1 align="center">Machine Learning Workflow Automation</h1>

<details>
  <summary><h2>Table of Contents</h2></summary>
  <ol>
    <li><a href="#overview">Overview</a></li>
    <li><a href="#aws-lambda">AWS Lambda</a>
    <ul>
        <li><a href="#introduction">Introduction</a></li>
        <li><a href="#lambda-functions">Lambda functions</a></li>
        <li><a href="#invoking-a-lambda-function">Invoking a Lambda function</a></li>
    </ul>
    </li>
    <li><a href="#aws-step-functions">AWS Step Functions</a>
    <ul>
        <li><a href="#introduction">Introduction</a></li>
        <li><a href="#amazon-states-language">Amazon States Language</a></li>
        <li><a href="#setting-up">Setting up</a></li>
        <li><a href="#creating-a-workflow">Creating a workflow</a></li>
        <li><a href="#invoking-a-workflow">Invoking a workflow</a></li>
    </ul>
    </li>
    <li><a href="#epilogue">Epilogue</a></li>
  </ol>
</details>

## Overview
A machine learning (ML) workflow is the structured, end-to-end process of developing and deploying an ML model. The key components of any ML workflow are data collection and pre-processing, model selection, model training and testing, and deployment. It is usually event-driven, meaning the end of one activity provokes the start of the next. 
<p align="center"><img src="img/ml-workflow.png" width="80%"></p>

As you have practiced the previous tutorial, you are now familiar with executing different components of a machine learning workflow in Amazon SageMaker AI. However, they are done manually and seperately. Additionally, you often need to repeat them multiple times to fix errors, improve your model and achieve desired performance. This process is error-prone and time-consuming. 

In this tutorial, you will learn how to automate these components and chain them together, ultimately forming a seamless ML workflow. By the end of this tutorial, you will be able to:
* Create an ML workflow with AWS Step Functions.
* Automate ML workflows with AWS Lambda.

## AWS Lambda
### Introduction
AWS Lambda is a serverless compute service that runs a single, self-contained function in response to events. It allows you to execute code without specifying underlying infrastructure, like hardware specifications, the operating system, or the maintenance of standard libraries. This service is ideal for small tasks that are frequently repeated.

In the programming realm, it is common to encounter situations where code that works on one machine often fails on another. Even in the managed services like Amazon SageMaker AI, you can still run into failures when running under different configurations. This is not the case in AWS Lambda.

### Lambda functions
A Lambda function is a piece of code that runs in response to events. When invoked, Lambda runs the function handler to process events and return necessary response. The handler function is the entry point of a Lambda function and other AWS services will use it to interact with your code. While the code in a Lambda function can  ontain more than one function, it can only have one handler.

The handler function must match the name and structure expected by the runtime environment. For Python, the function must have:
* Name: `lambda_handler`
* First parameter: `event`, a dictionary containing the event data that triggered the Lambda function.
* Second parameter: `context`, an object provided by AWS Lambda that gives [methods and properties](https://docs.aws.amazon.com/lambda/latest/dg/python-context.html) to access information about the invocation, function, and execution environment.
* Optional response to return, in the form of a dictionary containing status message.

```python
def lambda_handler(event, context):
    # Your code here
    return {
        'statusCode': 200,
        'body': 'Insert your message'
    }
```

In this exercise, you're going to create a basic Lambda function in Python. Then you will deliberately cause it to fail and practice finding error:
1. Head to AWS Lambda using the search bar and in the left navigation sidebar, select *Functions*.
<p align="center"><img src="img/lambda.png" width="80%"></p>

2. Click on *Create function* button.
3. Select *Author from scratch* option.
4. Enter a unique name for your Lambda function.
5. Under *Runtime*, select a version of Python.
6. Scroll down and click on *Create function* button.
<p align="center"><img src="img/function.png" width="80%"></p>

7. After the function is created, go to the *Test* tab to create a test event.
8. Select *Create new event*.
9. Give the test event a name if you intend to save it. Select *Hello World* as *Template*. There are several test template to simulate other AWS services invoking Lambda function. The select template is merely for basic or custom event simulation, as it doesn't represent any specific AWS service.
10. Leave the default Event JSON and click on the *Test* button to run the test event. You will soon receive a notification showing successful execution and the expected response message from the function. If you want to keep this test event for future experiment, click on the *Save* button.
<p align="center"><img src="img/test.png" width="80%"></p>
<p align="center"><img src="img/test-success.png" width="80%"></p>

11. Go to the *Code* tab and insert some technical error into your code. Then, click on the *Deploy* button inside the editor to update the function. In this code editor, if you look around, you can see that test events can be created and triggered from here instead.
<p align="center"><img src="img/function-error.png" width="80%"></p>

12. Go back to the *Test* tab and run the same test event again. You will soon receive a notification showing fail execution and the error message from the function.
<p align="center"><img src="img/test-fail.png" width="90%"></p>

13. However, if an error occurred outside a test environment, e.g. algorithmic error from a processing job, and you want to see what the issue is, go to the *Monitor* tab and and click on *View CloudWatch logs* button. It will direct you to CloudWatch Logs regarding your Lambda function. 
<p align="center"><img src="img/function-logs.png" width="80%"></p>

14. Click through the log of an event you want to investigate and you can see the error message from there.
<p align="center"><img src="img/error-log.png" width="80%"></p>

### Invoking a Lambda function
There are two types of Lambda function invocation:
* Synchronous invocation will launch the function and expect a immediate response from the function. As a general rule, you'll be invoking Lambda functions synchronously in ML engineering operations.
<p align="center"><img src="img/invocation-sync.png" width="40%"></p>

* Asynchronous invocation does not wait for a response from the function, and when you submit an event, you are actually submitting it in a queue to be processed. This type of invocations is used when you don't want to have to handle all of the replies, and you may not even need to handle it.
<p align="center"><img src="img/invocation-async.png" width="60%"></p>

It is important to keep these two ways of invoking a Lambda function in mind and to consult the documentation to confirm which of these options are available to you.

As seen earlier, a Lambda function is triggered through an event. It is a JSON object, but its structure differs depending on the service sending it. When configuring a service to send events to a Lambda function, consult the AWS documentation to determine the structure of the events your function will process.

To trigger your Lambda function synchronously, you can use AWS SDK or integrate it into workflows using AWS Step Functions. But for now, you will simulate a synchronous invocation with test events, just as you did previously:
1. Go to your S3 bucket and upload the dataset [`reviews_Musical_Instruments_5.json.zip`](../data/reviews_Musical_Instruments_5.json.zip).
2. Modify the code of Lambda function you created earlier so that it acts as a data preprocessing script, similar to the one used in your processing jobs. Alternatively, you can upload [code.zip](./code.zip) provided to override your Lambda function's code. Simply select *Upload from* → *.zip file* and upload the file. Note that the name of the Python file containing the function handler must be `lambda_function.py`, not any name.\
If you decide to implement your own Lambda function, remember to properly define `lambda_handler` function, as your Lambda function will only execute this function. If needed, you can include helper functions in your code. Moreover, your code should directly download the raw dataset using its S3 location extracted from the `event` argument, which will be explained later, and should directly upload training set and testing set into your S3 bucket. These actions requires you to work with AWS SDK for Python, i.e. [`boto3`](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html). Lastly, Lambda function restricts your file operations within the local directory `/tmp/`. Hence, all files created, downloaded, or extracted must be in this folder.
<p align="center"><img src="img/upload-code.png" width="80%"></p>

3. Go to *Configuration* tab, select *General configuration* on the left sidebar. Then select *Edit* on the right.
<p align="center"><img src="img/config.png" width="80%"></p>

4. Under *Timeout*, set it to about 5 minutes. And under *Existing role*, click on *View the role*. This will navigate you to *Identity and Access Management (IAM)* console of your Lamdba function's role.
<p align="center"><img src="img/timeout.png" width="80%"></p>

5. Since your Lamdba function's role is automatically created, it doesn't have the permission to access S3. Therefore, you have to grant it that permission. From the role details console, go to *Add permissions* → *Attach policies*.
<p align="center"><img src="img/add-permission.png" width="80%"></p>

6. Search for *AmazonS3FullAccess* and select it. Scroll down and click on *Add permissions* button.
<p align="center"><img src="img/s3-permission.png" width="80%"></p>

7. Go back to the previous browser tab, Lambda function's configuration console, and click on *Save* button.
8. Go to the *Test* tab and create a new test event. This time, select *S3 Put* as *Template*. This will simulate the actual event data that is sent to a Lambda function when a file is uploaded into an observed S3 bucket.
<p align="center"><img src="img/test-event.png" width="80%"></p>

9. In *Event JSON*, you can see that this is what will be sent to your Lambda function’s handler, via the `event` argument. To match the desired test scenario, replace the text inside the *name* field under the *bucket* field with your S3 bucket name. Also, replace the text inside the *key* field under the *object* field with key name of newly uploaded dataset, not its S3 location as explained in the first tutorial. These are the two values your function handler should extract from the `event` argument. \
Note that the *Records* field in the event payload contains a list, not subfields. This allows AWS S3 to notify a Lambda function about multiple object-related events in a single invocation. In this case, it would be two or more files uploaded simultaneously. Therefore, your code should iterate over this list to handle each record.
<p align="center"><img src="img/test-json.png"></p>

10. Give this test event a name and save it, if necessary. Then, click on the *Test* button to trigger your Lambda function.

After a few minutes, you will receive the notification within the *Test* tab. If it fails, try to fix the problem showed in the notification and in the CloudWatch Logs. If it succeeds, you will be able to see training set and testing set of the new dataset in your S3 bucket.

Next, you will trigger this Lambda function asynchronously with real event:
1. From the Lambda function console, click on the *+ Add trigger* button.
<p align="center"><img src="img/add-trigger.png" width="80%"></p>

2. Select *S3* as the source of invocation.
<p align="center"><img src="img/trigger-source.png" width="50%"></p>

3. In the *Bucket* field, select your S3 bucket name.
4. In the *Event types* field, deselect *All objects create events* and select *PUT* and *Multipart upload completed* only. This ensures the Lambda function is triggered only when new objects are uploaded.
<p align="center"><img src="img/event-type.png" width="50%"></p>

5. In the *Prefix* field, enter the directory path in your bucket where the datasets are expected to be uploaded. This will filter events so that only objects uploaded to that path will trigger the Lambda function.
6. In the *Subfix* field, enter `.json.zip` as this will restrict the invocation to this certain file type.
7. Tick the checkbox in the *Recursive invocation* field. This acknowledgement warns you about the risk of recursive invocations. They happen when your Lambda function is automatically triggered by its own uploads. Specifically, when uploaded files reside in the same bucket and match the prefix as well as the file type you specified in this setting. 
<p align="center"><img src="img/trigger-config.png"></p>
 
8. Click on *Add* button to finalize the trigger setting.
9. Go to your S3 bucket and upload the dataset [`reviews_Patio_Lawn_and_Garden_5.json.zip`](../data/reviews_Patio_Lawn_and_Garden_5.json.zip) in the directory path you specified earlier. This will soon trigger your Lambda function and you will be able to see the training set and the testing set of the new dataset.

Unlike synchronous invocation, you cannot receive a direct response message from your Lambda function with asynchronous invocation. However, you are still able to inspect error messages in CloudWatch Logs.

<ins>**Please note**</ins>: You are billed for every Lambda function invocation, even if it is a test event. Therefore, refrain yourself from spamming invocations and delete all triggers after you finish your experiment.
<p align="center"><img src="img/delete-trigger.png" width="80%"></p>

Similarly, you can construct a Lambda function to automate a workflow in AWS Step Functions with invocations.

## AWS Step Functions
### Introduction
AWS Step Functions is a visual workflow service that helps you use AWS services to build distributed applications, automate processes, orchestrate microservices, and create ML workflows.

It is based on two abstractions:
* State machine: serverless workflow, which is a series of event-driven steps.
* Task: a state within a workflow that represents a single unit of work performed by another AWS service.

Advantages:
* Intuitive UI.
* Easy visualization.
* Easy isolation of failure points.

Disadvantages:
* Significantly more expensive than Lambda function.
* Dependent on proprietary Amazon State Language.
* Not compatible with similar orchestration tools in other platforms.

### Amazon States Language
In AWS Step Functions console, you will directly intergrate and chain several microservices of Amazon SageMaker AI in order to construct an ML workflow. This requires a deeper understanding of the [Amazon States Language](https://states-language.net/spec.html) to configure each component. 

The Amazon States Language (ASL) is a JSON-based, structured language used to define your state machine. It mostly resembles a nested dictrionary in Python, from the syntax to the structure, with the exception of query langague embedded. 

ASL originally employs JSONPath as its query language. However, it recently adopts [JSONata](https://docs.jsonata.org/overview.html) as the default query language. When a state machine execution receives JSON input from execution, it passes that data to the first state in the workflow as input. With JSONata, you can retrieve a state input from `states.input`. If a state is successfully completed, its API response will be stored in `states.result`. Furthermore, you can use JSONata to dynamically configure your state machine during each execution.
<p align="center"><img src="img/vars-jsonata.png" width="80%"></p>

In this exercise, you will embed JSONata expression inside a string value. The expression must start with `{%` with no leading spaces, and must end with `%}` with no trailing spaces. Improperly opening or closing the expression will result in a validation error.
```JSON
"{% <JSONata expression> %}"
```
Any JSONata functions, provided by Step Functions, or variables must start with the character `$`, e.g. `$states.result` or `$split($variable_1)[0]`. Moreover, because the JSONata expression is in a string value, to add a string into the expression, use the single quote `'` or `\"`. Finally, to concatenate string, use the ampersand character `&`. For example:
```JSON
"{% $states.input.prefix & 'train/' & $split($states.input.dataset, '.', 1)[0] & '_train.txt' %}"
```

No worries, this tutorial will help you set up an ML workflow with ASL along the way. For more information, read [this](https://docs.aws.amazon.com/step-functions/latest/dg/transforming-data.html#writing-jsonata-expressions-in-json-strings) and watch [this](https://www.youtube.com/watch?v=kVWxJoO_zc8).

### Setting up
First of all, you need to create a role and your state machine will use it to gain full access to SageMaker AI and CloudWatch Events:
1. Head to IAM using the search bar.
<p align="center"><img src="img/iam.png" width="60%"></p>

2. In the left navigation sidebar, go to *Access Management* → *Roles*. Then, click on *Create role* button.
<p align="center"><img src="img/create-role.png" width="80%"></p>

3. In *Step 1*, select *AWS service* for *Trusted entity type* and select *Step Functions* for *Service or use case*. Then go to the next step.
<p align="center"><img src="img/step-1.png" width="80%"></p>

4. In *Step 2*, click on the *Next* button. In *Step 3*, give a name for the role and click on the *Create role* button at the bottom.
5. From the list of role names, click on the name of the role you have just created. From the role details console, attach both *AmazonSageMakerFullAccess* and *CloudWatchEventsFullAccess* to your role. \
Your state machine needs access to Amazon CloudWatch Events (now part of Amazon EventBridge) so that it can send logs and events to CloudWatch. This enables you to monitor, debug, and manage your workflow.

### Creating a workflow
Now it's time to contruct an ML workflow with Step Functions:
1. Head to Step Functions using the search bar and in the left sidebar, select *State machines*.
2. Click the *Create state machine* button.
3. In the pop-up window, select *Create from blank*, give a unique name for your state machine, and select *Standard* for *State machine type*. Finally, click on the *Continue* button.
<p align="center"><img src="img/state-machine.png"></p>

4. Take a look at the picture below. Now, use the search bar in the left sidebar of the console, find the illustrated states, and drag them onto the graph canvas to create the corresponding workflow. Rename each state as needed.
<p align="center"><img src="img/stepfunctions-graph.png"></p>

5. Click on the first state. In the right sidebar, go to the *Configuration* tab, scroll down, and check the option *Wait for task to complete*.
<p align="center"><img src="img/sync.png" width="60%"></p>

6. Go to the *Arguments & Output* tab, remove text in the *Arguments* field and write below text instead. You will gradually add more fields to correctly configure this state. For more information about CreateProcessingJob's arguments, go [here](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateProcessingJob.html). <p align="center"><img src="img/arg-config.png" width="70%"></p>

    ```JSON
    {
      "ProcessingJobName": "?",
      "RoleArn": "?"
    }
    ```
7. Since the name for new processing job must be unique, you should not hard-code its name in the *ProcessingJobName* field. If a static name is used, the state machine will create processing job with the same name for every execution, which will cause error and disrupt the workflow. Instead, dynamically generate a unique name using JSONata expression. In the *ProcessingJobName* field, enter the leading string of your choice for the name and concatenate it with the function `millis()`. For example, `{% 'BlazingText-' & $millis() %}`. Feel free to use different expression.
8. In the *RoleArn* field, enter the ARN (Amazon Resource Name) of the role you created and used throughout your SageMaker AI experiments in the last tutorial. To do this, head to IAM. In the left navigation sidebar, go to *Access Management* → *Roles*. Then find and click on the name of the role and you will be able to see its ARN.
<p align="center"><img src="img/sagemaker-role.png" width="80%"></p>

9. Add the field below to set up the resources for the job. Remember to seperate it from the previous field with a comma.
    ```JSON
    "ProcessingResources": {
      "ClusterConfig": {
        "InstanceCount": 1,
        "InstanceType": "ml.m5.large",
        "VolumeSizeInGB": 1
      }
    }
    ```
10. Add the field below to set up the inputs for the job. Remember to seperate it from the previous field with a comma. This field contains a list. Just like before, your processing job will have 2 inputs: raw dataset and Python script. So, this list contains two corresponding elements.
    ```JSON
    "ProcessingInputs": [
      {
        "InputName": "input",
        "S3Input": {
          "S3DataType": "S3Prefix",
          "S3InputMode": "File",
          "S3Uri": "?",
          "LocalPath": "?"
        }
      },
      {
        "InputName": "code",
        "S3Input": {
          "S3DataType": "S3Prefix",
          "S3InputMode": "File",
          "S3Uri": "?",
          "LocalPath": "?"
        }
      }
    ]
    ```
    The first element of the list is for the dataset. Provide its S3 location and local path in the corresponding subfields, *S3Uri* and *LocalPath*. Each execution of the state machine will require you to work with different dataset in different bucket. Thus, you should use JSONata expression to retrieve the S3 location of the dataset from the state input, e.g. `{% $states.input.prefix & $states.input.dataset %}`. Since this is the first state in your state machine, its input will directly be the input of state machine. Later, you will execute your state machine with an input like this:
    ```JSON
    {
    "bucket": "your-bucket",
    "prefix": "s3://your-bucket/data/",
    "dataset": "reviews_Musical_Instruments_5.json.zip"
    }
    ```
    The second element is for the Python script. Provide the S3 location and the local path in the corresponding subfields. No JSONata expression needed.
11. Add the below field. As before, find and enter the registry path of scikit-learn's processing image in the *AppSpecification* field. For the second element of the *ContainerEntrypoint* field, enter the local address to your Python script, e.g. `/opt/ml/processing/input/code/<your_script_name>`. If you use the provided Python code, enter a JSONata expression in the *ContainerArguments* field, which retrieves the dataset name through state input. Otherwise, remove this subfield.
    ```JSON
    "AppSpecification": {
      "ImageUri": "?",
      "ContainerEntrypoint": [
        "python3",
        "?"
      ],
      "ContainerArguments": [
        "?"
      ]
    }
    ```
12. Add the below field to set up the outputs for the job. The *Outputs* field contains a list with two items defining the configuration for the training set and the testing set. In each element, specify where the set should be uploaded in your bucket in the *S3Uri* field, and the local path where your Python script saves the set in the *LocalPath* field. Use JSONata expressions to dynamically determine the S3 output locations from the state input. 
    ```JSON
    "ProcessingOutputConfig": {
      "Outputs": [
        {
          "OutputName": "train_set",
          "S3Output": {
            "S3Uri": "?",
            "LocalPath": "?",
            "S3UploadMode": "EndOfJob"
          }
        },
        {
          "OutputName": "test_set",
          "S3Output": {
            "S3Uri": "?",
            "LocalPath": "?",
            "S3UploadMode": "EndOfJob"
          }
        }
      ]
    }
    ```
13. You have done setting up all required and important arguments for the first state. But you need to define the output of this state so that it will pass the expected S3 locations of the training set and the testing set to the next state in the workflow. Scroll to the *Output* field right below and enter the following:
    ```JSON
    {
      "train": "?",
      "test": "?"
    }
    ```
    In each field, use JSONata expression to contruct S3 location from the state input. The exact object names will depend on how your Python script saves the files. If you are using the provided Python script, use with the following instead:
    ```JSON
    {
      "train": "{% $states.input.prefix & 'train/' & $split($states.input.dataset, '.', 1)[0] & '_train.txt' %}",
      "test": "{% $states.input.prefix & 'test/' & $split($states.input.dataset, '.', 1)[0] & '_test.txt' %}"
    }
    ```
14. Go to the *Variables* tab and enter the text shown below to assign the bucket name extracted from this state's input to the variable `bucket`. This variable can be later referenced in subsequent states.
<p align="center"><img src="img/variables.png" width="60%"></p>

15. Click on the second state in the workflow. In the *Configuration* tab, scroll down and check the option *Wait for task to complete*.
16. Go to the *Arguments & Output* tab, remove text in the *Arguments* field and write below text instead. You will gradually add more fields to correctly configure this state. For more information about CreateTrainingJob's arguments, go [here](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateTrainingJob.html).
    ```JSON
    {
      "TrainingJobName": "?",
      "RoleArn": "?"
    }
    ```
    As earlier, you should dynamically generate a unique name for the training job using JSONata expression in the *TrainingJobName* field. In the *RoleArn* field, enter the ARN of the same role used in the previous state.
17. Add the below field. Then, find and enter registry path where container image of your select algorithm, BlazingText, is stored in Amazon ECR.
    ```JSON
    "AlgorithmSpecification": {
      "TrainingImage": "?",
      "TrainingInputMode": "File"
    }
    ```
18. Add the field below to set up the resources for the job.
    ```JSON
    "ResourceConfig": {
      "VolumeSizeInGB": 5,
      "InstanceCount": 1,
      "InstanceType": "ml.m5.large"
    }
    ```
19. To customize hyperparemeters of the BlazingText algorithm, add the below field. You are encouraged to add more subfields to calibrate more hyperparemeters. Remeber to read its [documentation](https://docs.aws.amazon.com/sagemaker/latest/dg/blazingtext_hyperparameters.html#blazingtext_hyperparameters_text_class) for more information.
    ```JSON
    "HyperParameters": {
      "mode": "supervised"
    }
    ```
20. Add below field to configure input data for the job. The *InputDataConfig* field contains a list with two elements, one for the training set and one for the testing set. In each one, specify S3 location of the corresponding set in the *S3Uri* field. Use JSONata expressions to extract the locations from the state input, which is the output of last state. Since the chosen algorithm only works with one type of data, plain text, you don't have to add and specify the *ContentType* field in each element. But if you work with other algorithms, pay attention to this in their documentation, as they may have different data format options to select.
    ```JSON
    "InputDataConfig": [
      {
        "ChannelName": "train",
        "DataSource": {
          "S3DataSource": {
            "S3DataType": "S3Prefix",
            "S3Uri": "?"
          }
        }
      },
      {
        "ChannelName": "validation",
        "DataSource": {
          "S3DataSource": {
            "S3DataType": "S3Prefix",
            "S3Uri": "?"
          }
        }
      }
    ]
    ```
21. Add below field to configure output data for the job. In the *S3OutputPath* field, enter the S3 path where you want SageMaker AI to output your model artifact. You should use JSONata expressions to dynamically construct this path with the assigned variable `bucket`, e.g. `{% 's3://' & $bucket & '/models/' %}`. 
    ```JSON
    "OutputDataConfig": {
      "S3OutputPath": "?"
    }
    ```
22. Add this last field to set maximum runtime to 10 minutes.
    ```JSON
    "StoppingCondition": {
      "MaxRuntimeInSeconds": 600
    }
    ```
23. Suppose that the training job runs successfully and creates a model artifact, the exact S3 location of the model artifact will be stored in the API response. You should pass this location to the next state in the workflow. Scroll to the *Output* field right below and enter the following:
    ```JSON
    {
      "artifact": "{% $states.result.ModelArtifacts.S3ModelArtifacts %}"
    }
    ```
24. Move to the third state of the workflow. Go to the *Arguments & Output* tab, remove text in the *Arguments* field and write below text instead:
    ```JSON
    {
      "ModelName": "?",
      "ExecutionRoleArn": "?",
      "PrimaryContainer": {
        "Image": "?",
        "Mode": "SingleModel",
        "ModelDataUrl": "?"
      }
    }
    ```
25. In *ModelName*, generate a unique name for the model object. In *ExecutionRoleArn*, enter the usual ARN. In *Image*, enter registry path of container image of *BlazingText*. In *ModelDataUrl*, enter S3 location of model artifact, extracted from state input.
26. Scroll down to the *Output* field. Set it to pass the name of the model object to the next state. You should use the `split` function on the `states.result.ModelArn` variable to isolate the name from the full ARN string. 
27. Move to the *CreateEndpointConfig* state. Go to the *Arguments & Output* tab, remove text in the *Arguments* field and write below text instead:
    ```JSON
    {
      "EndpointConfigName": "?",
      "ProductionVariants": [
        {
          "ModelName": "?",
          "InitialInstanceCount": 1,
          "InstanceType": "ml.m5.large",
          "VariantName": "variant-1"
        }
      ]
    }
    ```
28. In *EndpointConfigName*, generate a unique name for the endpoint configuration. In *ModelName*, enter the name of model object, extracted from state input.
29. Scroll down to the *Output* field. Set it to pass the name of the endpoint configuration to the next state. You should use the `split` function on the `states.result.EndpointConfigArn` variable to isolate the name from the full ARN string.
30. Move to the *CreateEndpoint* state. In the *Arguments & Output* tab, remove text in the *Arguments* field and write below text instead:
    ```JSON
    {
      "EndpointConfigName": "?",
      "EndpointName": "BlazingText-Reviews-Classifier"
    }
    ```
31. In *EndpointConfigName*, enter the name of endpoint configuration, extracted from state input. For the *EndpointName* field, since you will delete the endpoint shortly after you invoke it to save resources, you don't have to generate a unique name for it. But if you decide to generate, remember to pass its name to the next state.
32. Move to the *DescribeEndpoint* state. In the *Arguments & Output* tab, under the *Arguments* field, enter the name of endpoint for *EndpointName*.
33. Move to the *Choice* state. At this state, you will make a loop that occasionally checks for the endpoint status via the output of *DescribeEndpoint*. The loop will stop when the endpoint creation is done. To do this, scroll down to the *Choice Rules* section and click on the pencil icon of *Rule #1*.
<p align="center"><img src="img/edit-rule.png" width="60%"></p>

34. In the *Condition* field, enter the JSONata expression below to check if the endpoint status is *Creating*. Because you don't specify the output for the *DescribeEndpoint* state, it will have the API response as state output and pass that to the next state. Therefore, you can easily retrieve the endpoint status from the API response.
```JSON
{% $states.input.EndpointStatus = 'Creating' %}
```
35. Move to the *Wait* state. In the *Seconds* field, enter `60` to force the state machine wait for 1 minute before jumping to the next state. You can increase or decrease the waiting time if needed. In the *Next state* field, select *DescribeEndpoint* to make a loop.
<p align="center"><img src="img/loop.png" width="80%"></p>


36. Move to the *InvokeEndpoint* state. Go to the *Arguments & Output* tab, remove text in the *Arguments* field and write below text instead:
    ```JSON
    {
      "Body": "{\"instances\": [\"Review sentence #1.\", \"Review sentence #2.\", \"Review sentence #3.\"]}",
      "EndpointName": "BlazingText-Reviews-Classifier"
    }
    ```
    Replace the placeholder sentences with your custom review sentences and add more if needed.
37. In the *Body* field, write down a list of custom review sentences, as many as you like.
38. Move to the *DeleteEndpoint* state. Go to the *Arguments & Output* tab, remove text in the *Arguments* field and write below text instead:
    ```JSON
    {
      "EndpointName": "BlazingText-Reviews-Classifier"
    }
    ```
39. Move to the *CreateTransformJob* state. Go to the *Arguments & Output* tab, remove text in the *Arguments* field and write below text instead:
    ```JSON
    {
      "TransformJobName": "?",
      "ModelName": "?",
      "TransformResources": {
        "InstanceCount": 1,
        "InstanceType": "ml.m5.large"
      },
      "TransformInput": {
        "ContentType": "application/json",
        "DataSource": {
          "S3DataSource": {
            "S3DataType": "S3Prefix",
            "S3Uri": "?"
          }
        },
        "SplitType": "Line"
      },
      "TransformOutput": {
        "AssembleWith": "Line",
        "S3OutputPath": "?"
      }
    }
    ```
40. Fill in the missing parts with appropriate values or JSONata expressions.
41. Now switch to the *Config* tab of the state machine console.
<p align="center"><img src="img/config-tab.png" width="80%"></p>

42. Scroll down to the *Permissions* section and select the role you have preserved for your state machine. Finally, click on the *Create* button on the top right.
<p align="center"><img src="img/create-state-machine.png" width="80%"></p>

Alternatively, you can use *AWS Lambda Invoke* state to intergrate your Lambda function from previous section as your first state of the workflow. With this setup, you have to change either state machine input or your Lambda function's code.

Finally, you can add more states after *DeleteEndpoint* state to delete endpoint configuration and model object to free up resources.

### Executing a state machine
To try out your new ML workflow, simply do the following:
1. Go to your S3 bucket and delete all training sets, all testing sets, and all inference results of batch transform jobs from previous practices.
2. In your state machine console, click on the *Start execution* button.
<p align="center"><img src="img/start-execution.png" width="80%"></p>

3. In the pop-up window, enter the input values for the state machine. It should be in JSON format and include bucket name, S3 path to the dataset, and the dataset filename. You can write down one of any uploaded datasets you wish to test. Moreoever, depending on how you construct your workflow, you can include more values.
<p align="center"><img src="img/format-execution.png" width="80%"></p>

4. Click on the *Start execution* button once you have done.

Wait for a few minutes to let your workflow run to the end. If all states run successfully, you will be able to see the training set, the testing set, and the inference results in your S3 bucket. Additionally, you can see the results of endpoint invocation in the state output of *invokeEndpoint*.
<p align="center"><img src="img/result.png" width="80%"></p>

If the workflow is disrupted by a failed state, you can inspect the reason by click on the last failed state, colored in red. If your workflow fails to delete endpoint, please manually delete it to avoid __unwanted charges__.
<p align="center"><img src="img/error-workflow.png" width="80%"></p>

In addition, you can test an individual state while configuring it to ensure it behaves as expected before running the entire workflow:
1. From your state machine console, click on a state you want to test. In the right sidebar, click on the *Test state* button.
<p align="center"><img src="img/test-state.png" width="50%"></p>

2. In the pop-up window, choose the role with necessary permissions that you reserve for your state machine, in the *Execution role* field.
3. In *State input* field, enter a sample input for the state. The input must be literal and must contain no JSONata expressions.
4. In *Variables* field, enter the expected variables if the state references them in its parameters or output. The variables must contain literal values with no JSONata expressions.
<p align="center"><img src="img/test-input.png" width="60%"></p>

5. Go to the *State definition* tab. Under *Definition*, if the *Resource* field contains a postfix such as `.sync` or `.waitForTaskToken`, remove that postfix. 
<p align="center"><img src="img/test-def.png" width="60%"></p>

6. If you see and delete one of the postfixes mentioned above, you need to go to the *Arguments & Output* tab and remove any subfields of `states.result` that rely on post-complete API response. Otherwise, click the *Start test* button.
<p align="center"><img src="img/test-output.png" width="60%"></p>

Keep in mind that the test state feature does not support [*Activity tasks*](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-activities.html), *Parallel* state, and *Map* state and it can run for up to 5 minutes.

### Invoking a workflow
The final step of this tutorial is to automate your newly made ML workflow. You can do this by utilizing Lambda function in conjunction with the AWS SDK for Python:
1. Create a Lambda function with a Python runtime.
2. Attach *AWSStepFunctionsFullAccess* to the role of this Lambda function.
3. Use this code in your function. Enter your state machine's ARN in the missing part.
    ```python
    import json
    import boto3

    def lambda_handler(event, context):
        stateMachineArn = ?
        client = boto3.client('stepfunctions')

        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            prefix, dataset = record['s3']['object']['key'].rsplit('/', maxsplit=1)
            input = json.dumps({"bucket": bucket,
                                "prefix": f"s3://{bucket}/{prefix}/",
                                "dataset": dataset})
            client.start_execution(stateMachineArn=stateMachineArn, input=input) 
        return {
            'statusCode': 200,
            'body': 'MLWorkflow lanched successfully'
        }
    ```
4. Add an *S3* trigger with 2 event types, *PUT* and *Multipart upload completed*, to the function with approriate configuration, as guided from the previous section.
5. Now you will start automate your ML workflow with a Lambda synchronous invocation. Go to your S3 bucket and delete all training sets, all testing sets, and all inference results of batch transform jobs. Then, delete any dataset of your choice and upload it again in the same place.

As soon as the dataset is uploaded successfully, your Lambda funtion will be triggered, which will execute your state machine and automate your ML workflow.

If you have done your practice, please make sure you have completely deleted any endpoints and any triggers in AWS Lambda.

## Epilogue
Congratulations! You have successfully built and automated your first machine learning workflow. This marks a significant milestone in building production-ready, event-driven ML solutions using AWS services. 

As a best practice, __remember to delete or turn off__ any cost-consuming instances in AWS SageMaker AI and AWS Lambda. Moreover, you are encouraged to practice what you have learned so far to a different use case.