#!/bin/bash

set -e

# No Drive
echo "Running Wilson and Cowan simulation for the no drive case..."
# original values
echo "original neuron parameters"
python WilsonCowan.py -wee 10. -wei 12. -wie 8. -wii 3. -ze 0.2 -zi 4. -ie1 0 -ii1 0 -w 0.25

echo "Fig 11 like"
python WilsonCowan.py -wee 20. -wei 21. -wie 16. -wii 6 -ze 1.6 -zi 7. -ie1 0 -ii1 0 -w 0.25

echo "Fig 4 like"
python WilsonCowan.py -wee 10. -wei 9. -wie 5. -wii 3 -ze 3 -zi 4. -ie1 0 -ii1 0 -w 0.25

# iterate over one parater and see how it change the behaviour
echo "iterate over wei"
list=( 5 8 10 12)
for value in ${list[*]}
do
    echo "wei " $value
    python WilsonCowan.py -wee 10. -wei $value -wie 8. -wii 3. -ze .2 -zi 4. -ie1 0 -ii1 0 -w 0.25
done

# Driven
# echo "Runing Wilson and Cowan simulation for the driven case..."
# python WilsonCowan.py -wee 10. -wei 12. -wie 8. -wii 3. -ze 0.2 -zi 4. -ie1 0.5 -ii1 0.5 -w 0.25

