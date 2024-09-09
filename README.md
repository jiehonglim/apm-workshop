# Workshop Prep

## Click on the Shell tab

### Clone git repo
git clone https://github.com/jiehonglim/apm-workshop.git
cd apm-workshop

### Mark the setup script executable
chmod +x setup.sh

### Execute setup script
./setup.sh

### Run your streamlit app
streamlit run app.py & sleep 1 && echo "The Local Tunnel Password = $(curl -s ipv4.icanhazip.com)" && npx localtunnel --port 8501