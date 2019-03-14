# CZ4071 - Network Science

## Minimum Computer Requirements (Estimated Loading Time < 5mins)
CPU: i9-9900k  
GPU: RTX 2070  
RAM: 32GB 3200Mhz  
Storage: Samsung SSD Evo 840  

## Instructions for set-up  

Install python (https://www.python.org/downloads/release/python-368/)  
python==3.6.8  

Add python to computer system environment variables if needed.  
Check python version by using Windows PowerShell with the following command  
**python --version**  
Ensure that you install the correct version  

Install pip if needed however python should have install pip by default.  
Change directory to 'cz4071/ns'  
You should see a **ns-requirements.txt** file.  
This file contains all the required libraries needed for this project.  
Run **pip install -r ns-requirements.txt**  
Ensure that all libraries are installed successfully.  

Run **python manage.py runserver**  
Open up a web browser (recommended FireFox)  
Go to http://localhost:8000  
You should see the project.    

**DO NOTE THAT IT IS NORMAL THAT THE SERVER STOP AFTER EVERY RUN**    

## FAQ  
Q: Why do my web server stops after every run?  
A: This is normal as there is a bug with Matplotlib library whereas the default backend for rendering causes the main thread to stop.    

Q: Why does it take so long to generate a network more than a 1000 nodes?
A: It is not recommended to generate a random network with more than a 1000 nodes unless you are using a super-computer. As it requires a long amount of processing time.    

Q: Unable to run the server!  
A: Please note that you have to install all of the required libraries versions in ns-requirements.txt. Any missing library might cause an error.    

Q: Application not executing after inputting the values.  
A: Please close each interactive diagram prompt in order for the application to continue running. Do not worry all the images are saved in uploads/plot/ folder. You can view all images after loading into the next page.
