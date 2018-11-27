#!/usr/bin/env bash
#
#Download the data of interest from the National Cancer Institute
#Genomic Data Commons using a manifest file
#
#The GDC Data Transfer tools can be downloaded from: 
#https://gdc.cancer.gov/access-data/gdc-data-transfer-tool
#

if [ "$#" -eq 0 ] || [ $1 == "help" ] || [ $1 == "h" ] || [ $1 == "-help" ] || [ $1 == "-h" ]; then
	echo "
		Usage: download_gdc_data.sh [manifest_file]
			
			[manifest_file]: Manifest file generated from the GDC Data Portal (https://portal.gdc.cancer.gov/)
				 with information for downloading your data of interest
	"

	exit 1
fi 



MANIFEST=$1

gdc-client download -m  $MANIFEST
