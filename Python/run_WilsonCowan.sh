#!/bin/bash

set -e

# No Drive
echo "Runing Wilson and Cowan simulation for the no drive case..."
python WilsonCowan.py -wee 10. -wei 12. -wie 8. -wii 3. -ze 0.2 -zi 4. -ie1 0 -ii1 0 -w 0.25

# Driven
echo "Runing Wilson and Cowan simulation for the driven case..."
python WilsonCowan.py -wee 10. -wei 12. -wie 8. -wii 3. -ze 0.2 -zi 4. -ie1 0.5 -ii1 0.5 -w 0.25
