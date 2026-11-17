Welcome. This project is a SMS messaging web application through SMS gateway. Unfortunately, Twilio doesn't support free trials in the Philippines
First I installed django by typing 'pip install django into my cmd'
Then I opened a folder where I will save my project. There I clicked the tab above named terminal and clicked 'new terminal'. In the new terminal I inputted 'python -m django startproject myproject .'. At first I got an error and was so confused. It turns out I had put my project instead of myproject.
After rectifying my err, I also inputted python manage.py startapp shop. And then configured myproject/settings.py and register the new app inside.
Next I opened shop/models.py to define my database tables as python classes from model.Model
Then, run the migration generator in my terminal which is 'python manage.py makemigration', after that I inputted 'python manage.py migration' to execute the pending migrations to update the physical database.
