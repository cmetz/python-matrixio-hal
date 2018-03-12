# python-matrixio-hal
Python driver for Matrix Creator / Voice

## Requirements installation
```
# Add repo and key
curl https://apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list

# Update packages and install
sudo apt-get update
sudo apt-get upgrade

# Installation
sudo apt install matrixio-creator-init libmatrixio-creator-hal-dev

# Enable SPI
sudo raspi-config >> Interfacing options >> SPI >> yes >> exit and reboot

# install the package python-matrixio-hal to your python environment
sudo apt-get install cython (optional, to speedup build process)
pip install .
```

## Examples

Run the examples in the examples folder.

## Docker example

### Install docker if not installed
```
curl -fsSL get.docker.com -o get-docker.sh
sudo CHANNEL=stable sh get-docker.sh
sudo usermod -aG docker pi
```

### Build and run led\_roate example (Dockerfile)
```
# Build the docker image led_rotate (it uses the examples from the examples folder)
docker build -t led_rotate .

# Run led_rotate as new container led_rotate
docker run --name led_rotate -d --device=/dev/spidev0.0 led_rotate

# List active containers
docker ps

# Stop it
docker stop led_rotate

# Restart it
docker start led_rotate

# Remove Cotainer
docker stop led_roate
docker rm led_roate

# Auto restart cotainer after a reboot
# create the cotainer with --restart always
docker run --name led_rotate -d --restart always --device=/dev/spidev0.0 led_rotate
```
