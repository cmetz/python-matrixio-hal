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

# install aditional python modules
pip install -r requirements.txt
```

## Examples

Run the examples in the base dir.
