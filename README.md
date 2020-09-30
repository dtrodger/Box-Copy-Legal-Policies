## Box Legal Hold API Examples 
### Set up and Run  
1. (Optional) From the project root folder, create a Python 3 virtual environment  
`$ virtualenv --python=python3 env`  
2. (Optional) Activate the virtual environment  
`$ source env/bin/activate`  
3. Install the project dependencies  
`$ pip install -r requirements.txt` 
4. Create a `box_jwt.yml` file at the root of the project, and add your JWT key data  
5. Run the command line interface menu to see the available commands  
`$ python main.py` 
6. Run a specific command  
`$ python main.py list-legal-hold-policies` 