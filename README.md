# sample slackbot code

### store secret in secrets manager
- [Set up secret](secrets.png)
- [Find role associated with lambda](role.png)
- [Give permissions](policy.png) (note that you need to give permission to that specific secret)

- test with local boto config `python app.py`


### set up Slack app
- https://api.slack.com/apps
- Choose “From scratch” and provide an app name and select the workspace where you want to install the app.
- Create a Slack Slash Command:
  - In the Slack app settings, go to “Features” > “Slash Commands” and create a new command.
  - Set the command to /testbot and the Request URL to your AWS Lambda endpoint that will handle the Slack command (we’ll set this up later).
  - Save the settings.
- Enable Incoming Webhooks:
  - In the Slack app settings, go to “Features” > “Incoming Webhooks” and activate the feature.
  - Create a new webhook URL and copy it. You’ll need this URL so the Lambda function can post messages to Slack.

### Set Up AWS Lambda to Handle Slack Commands:
  - Lambda function in handler.py will handle the incoming requests from the slackbot, and then respond back to Slack.
  - We can install the requirements.txt to a local directory and make a deployment package, but also have to set up API gateway, logging, permissions etc.
  - deploy using [serverless](https://www.serverless.com/)
  - config for AWS is in `serverless.yaml`
- [install npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
```
npm install -g npm@10.8.2
npm install -g serverless
npm install serverless-python-requirements
```

- interactively create serverless account and project (slackbot)
`serverless`
this will update README.md and serverless.yml, do git diff and revert those changes, make sure repo is in sync with GitHub
serverless deploy
