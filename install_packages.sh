#!/bin/bash

echo "This script will install NumPy, Pandas, Matplotlib, and Seaborn"
echo "Do you want to continue? [y/n]"
read -r choice

if [ "$choice" = "y" ]; then
  echo "Installing NumPy"
  sudo apt-get install python3-numpy

  echo "Installing Pandas"
  sudo apt-get install python3-pandas

  echo "Installing Matplotlib"
  sudo apt-get install python3-matplotlib

  echo "Installing Seaborn"
  sudo apt-get install python3-seaborn

  echo "Installation complete"
else
  echo "Installation canceled"
fi
