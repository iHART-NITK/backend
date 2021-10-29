# iHART

> A Distributed, Real-Time Cross Platform Application for Healthcare Management and Automation

**iHART** is a software product that provides an interface for students and faculty of NITK to access healthcare facilities on campus. It also helps the HCC staff manage their work and documents better.

## Product Scope

* Scheduling appointments with doctors on campus.
* Request for ambulance service in a medical emergency.
* Upload prescription for regular medication.
* Review the medical history section of each student, in cases of emergency (allergies, previous medication, etc.)
* Manage the pharmaceutical inventory at the HCC Pharmacy
* Offer QR Code based verification of sick leave certificates issued by HCC.

## Installation Steps for Localhost Setup

```bash
pip install -r requirements.txt

mysql -u <username> -p
>> create database iHART
>> exit

cd ihart_backend
cp '.env example' .env
# fill up the .env file with your local info
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 3000
# open localhost:3000 on your browser
```
