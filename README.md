# Style-transfer-app
This repo uses a Tensorflow Model Hub model to perform neural style transfer.

The structure is simple:
- The style transfer model dir is the model saved in the Tensorflow saved model format. It is not used
- The websrc dir contains the django app
- gunicorn_start.sh is my exploration into using gunicorn for this app but in the end I decided it was to much of a hassle. I also tryed using nginx with gunicorn

The server is easily started via:
+ go into the websrc dir
+ in the terminal enter `manage.py runserver --insecure`
The insecure part is to make sure that static files are served.
