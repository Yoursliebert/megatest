sudo apt install git -y

sudo apt install python3 -y

sudo apt install python3-pip -y

sudo apt install python3-venv -y

git clone https://github.com/Yoursliebert/megatest
cd megatest

nano .env

python3 -m venv venv

. venv/bin/activate

pip install -r requirements.txt

python3 bot.py
