const jmespath = require('jmespath');
const AWS = require('aws-sdk');
AWS.config.update({region: 'us-east-1'})

const ec2 = new AWS.EC2();
const s3 = new AWS.S3();

var bucketParams = {
    Bucket : process.argv[2]
  };

  s3.createBucket(bucketParams, function(err, data) {
    if (err) {
      console.log("Error", err);
    } else {
      console.log("Success", data.Location);
    }
  });


//Création de l'instance EC2 
var instanceParameters = {
    ImageId: 'ami-0022f774911c1d690',
    InstanceType: 't2.micro',
    KeyName: 'key-big-data',
    MinCount: 1,
    MaxCount: 1
}

var instancePromise = ec2.runInstances(instanceParameters).promise();

instancePromise.then(
    function(data) {
        console.log(data);
        var instanceId = data.Instances[0].InstanceId;
        console.log("Instance créée", instanceId);
        tagParams = { Resources: [instanceId], Tags: [
            {
                Key: 'Instance BigData',
                Value: 'SDK Sample'
            }
        ]};

        var tagPromise = ec2.createTags(tagParams).promise();

        tagPromise.then(
            function(data) {
              console.log("Instance tagged");
            }).catch(
              function(err) {
              console.error(err, err.stack);
            });
        }).catch(
          function(err) {
          console.error(err, err.stack);
        });


//Lister les instances EC2
ec2.describeInstances({
        Filters: [{
            Name: 'instance-state-name',
            Values: ['running']
        }],
        MaxResults: 10
    }, 
    (err, data) => {
        if (err) {
            console.log(err);
        } 
        else {
            const instanceIds = jmespath.search(data, 'Reservations[].Instances[].InstanceId');
            console.log(instanceIds);
        }
    });