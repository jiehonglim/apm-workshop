# Workshop Prep

## Click on the Shell tab and execute the following commands:

```
git clone https://github.com/jiehonglim/apm-workshop.git 
cd apm-workshop
chmod +x setup.sh
./setup.sh
streamlit run app.py --server.address=localhost & sleep 1 && echo -e "\nThe Local Tunnel Password = $(curl -s ipv4.icanhazip.com)\nClick on the below URL and enter the above IP Address in the Tunnel Password field.\n" && npx localtunnel --port 8501
```

### Clone git repo
git clone https://github.com/jiehonglim/apm-workshop.git
cd apm-workshop

### Mark the setup script executable
chmod +x setup.sh

### Execute setup script
./setup.sh

### Run your streamlit app
streamlit run app.py --server.address=localhost & sleep 1 && echo -e "\nThe Local Tunnel Password = $(curl -s ipv4.icanhazip.com)\nClick on the below URL and enter the above IP Address in the Tunnel Password field.\n" && npx localtunnel --port 8501