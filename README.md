# python-matrixio-hal
Python matrixio (Creator) hal using SPI

## Requirements installation
```
# Add repo and key
curl https://apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list

# Update packages and install
sudo apt-get update
sudo apt-get upgrade

# Installation
sudo apt install matrixio-creator-init

# Enable SPI
sudo raspi-config >> Interfacing options >> SPI >> yes >> exit and reboot

# install additional python modules
pip install -r requirements.txt
```

## Examples

Run the examples in the base dir.

## Docker example

### Install docker if not installed
```
curl -fsSL get.docker.com -o get-docker.sh
sudo CHANNEL=stable sh get-docker.sh
sudo usermod -aG docker pi
```

### Build and run led\_roate example (Dockerfile)
```
# Build the docker image led_rotate
docker build -t led_rotate .

# Run led_rotate
docker run --name led_rotate -d --rm --device=/dev/spidev0.0 led_rotate

# List active containers
docker ps

# Stop it
docker stop led_rotate
```
