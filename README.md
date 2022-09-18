# indianstockscanner PREPROD
https://indianstockscanner-pre.herokuapp.com/

# indianstockscanner PROD
https://indianstockscanner.herokuapp.com/

## Extras Heroku Deployment using CLI Steps

Deployment to Heroku Instructions (Heroku Git)
Sign up for a free heroku account if you havent already done so
Create app ie. myapp #name of app
Type heroku login --> This will take you to a web based login page
cd to your directory on your local drive
Type 'git init'
Type 'heroku git:remote -a myapp'
Type 'git add .'
Type ' git commit -am "version 1"'
Type 'git push heroku master'
Now you need to allocate a dyno to do the work. Type 'heroku ps:scale worker=1'
If you want to check the logs to make sure its working type 'heroku logs --tail'
Now your code will continue to run until you stop the dyno. To stop it scale it down using the command 'heroku ps:scale worker=0'
heroku run bash 

developed by @tanmoy1999
