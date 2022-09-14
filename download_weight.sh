#!/bin/bash


if [ $# != 1 ]
then
echo "Usage: $0 weight_directory"
exit 0
fi

function google_download(){
    confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://drive.google.com/uc?export=download&id='$1 -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')
    echo $confirm
    wget --load-cookies /tmp/cookies.txt "https://drive.google.com/uc?export=download&confirm=$confirm&id=$1" -O $2 && rm -rf /tmp/cookies.txt
    gzip -d $2
}

path=`pwd`
mkdir -p $1/wMF
mkdir -p $1/woMF
cd $1/woMF
echo "--> Download Weight files for Non-MF model"
google_download 1R3TEimRLpCp7i6n0EoCUM3LzKB7KE_iR  weight3.pkl.gz
google_download 1Ce1A0Bw0aiawr5Sj2n5-C5pGEf_0ibrn  weight2.pkl.gz
google_download 1YlIWcwd1Qxc5a33HqnxHQp1k1ukE4AcN  weight1.pkl.gz
cd $path
cd $1/wMF
echo "--> Download Weight files for MF model"
google_download 1nOz0O7qGI0riKO5gzmswG08kzYfjaADK weight3.pkl.gz
google_download 10ajrzXFUH2uiCkI5zDiDI6PBy_1d52hk weight2.pkl.gz
google_download 1Rx1mm_WcCj8DAGOCQiupTcaiumaq6PJH weight1.pkl.gz
cd $path
echo "Done"

