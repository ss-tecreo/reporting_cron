#!/bin/bash

# Variables
PREVIOUS_DAYS2=$(date -d "-2 days "  +'%Y%m%d')
DB_HOST="localhost"
DB_USER="root"
DB_PASSWORD="root"
DB_NAME="tecreo"
BACKUP_PATH="/root/DB_DUMP/"
BACKUP_NAME="${DB_NAME}_backup_$(date +'_%Y%m%d%H%M%S').sql"

# Configuration
SPACE_NAME="tecreo-reporting-dev"
REGION="sgp1"  # e.g., nyc3
FILE_PATH="/root/DB_DUMP/${BACKUP_NAME}"
FILE_NAME_IN_SPACE="mysql-dumps/"
ENDPOINT_URL="https://${REGION}.digitaloceanspaces.com"



# Create backup directory if it doesn't exist
mkdir -p ${BACKUP_PATH}

# Create the MySQL dump
mysqldump -h ${DB_HOST} -u ${DB_USER} -p${DB_PASSWORD} ${DB_NAME} > ${BACKUP_PATH}/${BACKUP_NAME}

# Check if the dump was successful
if [ $? -eq 0 ]; then
  echo "Backup successful: ${BACKUP_PATH}/${BACKUP_NAME}"
  # Upload the file to the DigitalOcean Space
  aws s3 mv "$FILE_PATH" "s3://$SPACE_NAME/$FILE_NAME_IN_SPACE"  --region "$REGION" --endpoint-url "$ENDPOINT_URL"

  if [ $? -eq 0 ]; then
      echo "File '$FILE_PATH' uploaded successfully to '$SPACE_NAME/$FILE_NAME_IN_SPACE'."
  else
      echo "An error occurred during file upload."
  fi
else
  echo "Backup failed!"
fi


#CSV files configuration 
CSV_FILE_PATH="/root/reporting_cron/attachment/${PREVIOUS_DAYS2}"
CSV_FAIL_FILE_PATH="/root/reporting_cron/attachment/fail/${PREVIOUS_DAYS2}"
FOLDER_NAME_ON_SPACE="reports-csv/${PREVIOUS_DAYS2}"


# Upload the file to the DigitalOcean Space
aws s3 mv "$CSV_FILE_PATH" "s3://$SPACE_NAME/$FOLDER_NAME_ON_SPACE" --recursive  --region "$REGION" --endpoint-url "$ENDPOINT_URL"

if [ $? -eq 0 ]; then
    echo "File '$CSV_FILE_PATH' uploaded successfully to '$SPACE_NAME/$FOLDER_NAME_ON_SPACE'."
    rm -rf "${CSV_FILE_PATH}"
    rm -rf "${CSV_FAIL_FILE_PATH}"
else
    echo "An error occurred during file upload."
fi


