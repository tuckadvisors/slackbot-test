# Sample Slackbot code

### Store secret in secrets manager
- [Set up secret](secrets.png)
- [Find role associated with lambda](role.png)
- [Give permissions](policy.png) (note that you need to give permission to that specific secret)
- Test with local boto config `python app.py`
- Slackbot doesn't currently need any Amazon secrets but need to test this code and use in other lambdas


### Set up a Slack app
- https://api.slack.com/apps
- Choose “From scratch” and provide an app name and select the workspace.
- Create a Slack Slash Command:
  - In the Slack app settings, go to “Features” > “Slash Commands” and create a new command.
  - Set the command to /testbot and the Request URL to the AWS Lambda endpoint that will handle the Slack command (see below).
- Enable Incoming Webhooks:
  - In the Slack app settings, go to “Features” > “Incoming Webhooks” and activate the feature.
  - Create a new webhook URL and copy it. You’ll need this URL so the Lambda function can post messages to Slack. (not currently used, response payload is used go generate a Slack message)
  - Save the settings.

### Set Up AWS Lambda to Handle Slack Commands:
  - Lambda function in handler.py will handle the incoming requests from the slackbot, and then respond back to Slack using the incoming Webhook URL.
  - We can deploy by installing the requirements.txt to a local directory and making a deployment package and uploading to AWS, but also have to set up API gateway, logging, permissions etc.
  - Deploy using [serverless](https://www.serverless.com/) to automate this process.
  - Config for AWS is in `serverless.yaml`
- [install npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
```
npm install -g npm@10.8.2
npm install -g serverless
npm install serverless-python-requirements
```

- Interactively create serverless account and project (slackbot)

`serverless`

This will overwrite README.md and serverless.yml, do git diff and revert those changes, make sure repo is in sync with GitHub and then deploy with:

`serverless deploy`

See additional info in [README-serverless.md](README-serverless.md)