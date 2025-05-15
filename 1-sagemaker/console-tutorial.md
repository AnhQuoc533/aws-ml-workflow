<h1 align="center">Introduction to Amazon SageMaker</h1>
<!-- TABLE OF CONTENTS -->
<details>
  <summary><h2>Table of Contents</h2></summary>
  <ol>
    <li><a href="#overview">Overview</a></li>
    <li><a href="#amazon-s3">Amazon S3</a>
    <ul>
        <li><a href="#introduction">Introduction</a></li>
        <li><a href="#creating-bucket">Creating bucket</a></li>
        <li><a href="#uploading-data">Uploading data</a></li>
      </ul>
    </li>
  </ol>
</details>

## Overview
Amazon SageMaker is an umbrella of services that AWS provides for Machine Learning. In a nutshell, Sagemaker is a service that enables the developer to be much more efficient with their valuable time when developing and deploying ML models. This methodology is applicable across many learning algorithms and many production use cases.

In this exercise, you will harness some of the most commonly used microservices of SageMaker to contruct basic components of a machine learning workflow. By the end of this lesson, you will be able to:
* Launch a processing job, to preprocess your data.
* Launch a training job, and build your ML model.
* Deploy an endpoint, an API for your trained model.
* Launch a batch transform job, to try out your model.
<center><img src="img/sagemaker_microservices.png"></center>

## Amazon S3
First of all, you need to create a bucket in Amazon S3 to store any future files and data.

### Introduction
Amazon Simple Storage Service (Amazon S3) is an object storage service that can store almost any object needed for machine learning. That includes datasets, model artifacts, logs, and more.

A [bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingBucket.html) is a container for objects (i.e., files) stored in S3. 

S3 supports the folder concept as a means of grouping objects. It does this by using a shared name *prefix*. In other words, the grouped objects have names that begin with a common string. This common string, or shared prefix, is the folder name. Object names are also referred to as key names.

For example: `s3://example-bucket/1/2/3/example.txt`
 * Bucket: example-bucket 
 * Prefix: 1/2/3
 * Key name: 1/2/3/example.txt

### Creating bucket
1. Head to Amazon S3 using the search bar and in the left navigation sidebar, select *Buckets*.
<center><img src="img/bucket.png"></center>

2. Select *Create bucket*.
3. Enter a name for your bucket. Once created, you cannot change its name.
4. For region, select the AWS Region close to you to minimize latency and costs.
<center><img src="img/create_bucket.png"></center>

5. Scroll all the way down and select *Create bucket*.

Now that you have create a bucket on AWS, you can upload any files into this storage manually or through API. \
Furthermore, you can create folders for organization purpose. Simply go to your bucket and click *Create folder*.
<center><img src="img/folder.png"></center>

### Uploading data
After creating bucket, you can upload the data and any other files there. But right now, you need to upload two datasets in the [data](../data) folder first.

1. Go to your bucket. If you have created a folder within your bucket and want to upload there instead, then click at the folder to open it up.
2. Select *Upload*.
<center><img src="img/upload.png"></center>

3. From here, you can drag and drop files or/and folders you want to upload into the website, or you can select *Add files* or *Add folder*.
<center><img src="img/add.png"></center>

3. Select *Upload* at the bottom when all set.

## Amazon SageMaker
Good job on your work so far! After uploading necessary data, the next thing to do is training a machine learning model and making use of it to produce inferences. This is the most important part as you will perform common machine learning operations on AWS.

Today, you will be making a model that predicts the usefulness of a product review, given only the text. This is an example of a problem in the domain of supervised sentiment analysis.

### Processing jobs
First of all, you need the input data in order to train the model. The [dataset](../data/reviews_Toys_and_Games_5.json.zip) you will be working with is a collection of reviews for an assortment of toys and games found on Amazon. It includes, but is not limited to, the text of the review itself as well as the number of user "votes" on whether or not the review was helpful.

However, the dataset is inside the .zip file so you need to extract it before proceeding. One more thing to know is that the dataset is a file containing a single JSON object per line representing a review with the following format: 
```JSON
{
 "reviewerID": "<string>",
 "asin": "<string>",
 "reviewerName": "<string>",
 "helpful": [
   <int>, (indicating number of helpful votes)
   <int>  (indicating total number of votes)
 ],
 "reviewText": "<string>",
 "overall": <int>,
 "summary": "<string>",
 "unixReviewTime": <int>,
 "reviewTime": "<string>"
}
```
For now, you just need to filter the fields *helpful* and *reviewText* out of the "raw" data for each sample. Finally, it is your responsibility is to separate the dataset into a training set and testing set. Ensure the training set represents 80% of the data while the rest is testing set. Be careful that the data doesn't overlap because this will result in overfitting.

All of the procedures mentioned above and more are collectively called *data pre-processing*, the first and most crucial step in any machine learning project. To do all of that in AWS, do the following steps:
1. Navigate to Amazon SageMaker.
2. In the left navigation sidebar, go to *Processing* → *Processing jobs*.
<center><img src="img/processing.png"></center>

3. Click on *Create processing job* button.
<center><img src="img/create_job.png"></center>

4. In the *Job name* field, enter a unique name for your processing job.
5. In the *Container* field, enter registry path of a processing image stored in Amazon ECR. For this exercise, you will use scikit-learn's image.\
To find the registry path, go to [Docker Registry Paths and Example Code](https://docs.aws.amazon.com/sagemaker/latest/dg-ecr-paths/sagemaker-algo-docker-registry-paths.html). On the left navigation sidebar, choose the AWS region that you're logging in. Then, scroll down to *Scikit-learn (algorithm)* section, you will find the registry path and the version associated. Replace `<tag>` by `[version]-cpu-py3`. For example, if you choose version 1.2-1, your registry path will be `683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:1.2-1-cpu-py3`\
See the illustration for more intuition.
<center><img src="img/path.png"></center>













