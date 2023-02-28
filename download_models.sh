#! /bin/bash

wget https://drive.google.com/uc?id=1-LKJTZakqd8ntKzqVNtQZUgdZnFoYtpK
unzip Contract_Embedding.zip
cp -r Embedding/ contract_level/
rm -rf Embedding/

wget https://drive.google.com/uc?id=1lbaQVtZbNuEEjHIWVnwLqGvILxNWwtZW  
unzip Contract_Model.zip  
mv Model contract_level/
rm -rf Model

wget https://drive.google.com/uc?id=18GiDgSwoRjPC25d2Vp15oi_xH2NivyXH  
unzip Statement_Model.zip 
mv Model statement_level/  
rm -rf Model
rm *.zip