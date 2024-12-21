# **Real-Time Vehicle License Plate Recognition Using Deep Learning 🚗🔍**

Welcome to the Real-Time Vehicle License Plate Recognition (LPR) System! This powerful application leverages YOLOv8 (You Only Look Once version 8), a state-of-the-art deep learning model for object detection, to identify and recognize vehicle license plates in real-time. The system captures images or video streams, detects license plates, and stores relevant information in a PostgreSQL database for efficient querying and tracking. Built with Flask, the app serves as the backend for handling incoming requests and providing easy access to the data.

<p align="center">
  <img src='https://github.com/Shuhaib73/ANPR_DeepLearning/blob/prj_branch/cv_data/readme_img1.png' width='800' height='350' />
</p>

----

**Beyond Object Detection: Unlocking Content Within Objects**

- Object detection has become a cornerstone of computer vision, enabling us to identify and locate objects in images and videos. However, the power of AI extends beyond simply recognizing "what's there." A crucial area within computer vision delves deeper, focusing on content recognition within objects.

**What is Content Recognition Within Objects?**

- This field takes object detection a step further by recognizing the specific information contained within the identified object. Imagine it as zooming in on a detected object and extracting its hidden details. Common techniques used here include Optical Character Recognition (OCR) for text within objects like license plates, barcodes, or signs.

- Automatic License Plate Detection (ALPR) is a powerful technology that goes beyond simply identifying and locating vehicles. It delves deeper by recognizing the alphanumeric characters on license plates, offering a wide range of applications across various industries. This case study delves into the potential of ALPR to automate tasks and enhance security in parking, access control, traffic management, and logistics.

----

## **📖 Features**

* Real-Time License Plate Recognition: Detect and recognize vehicle license plates in real-time from images or video streams, ensuring immediate data processing.
* YOLOv8 Object Detection: Built using YOLOv8, a cutting-edge object detection model known for its speed and accuracy, making it ideal for real-time applications.
* PostgreSQL Database Integration: Automatically stores detected license plates and associated metadata (e.g., timestamp, image data) in a PostgreSQL database for easy querying, analysis, and tracking of vehicles.
* Flask Backend: The app is powered by Flask, a backend web framework, ensuring smooth integration with the frontend and database.

----

## **📍 Use Cases**: 

* Parking Management: Automate parking lot access by detecting vehicles and ensuring that only authorized vehicles can enter.
* Traffic Monitoring: Monitor vehicle flow and track traffic patterns in real-time to optimize road usage and improve traffic management.
* Security and Surveillance: Enhance security by tracking vehicles at specific locations or monitoring suspicious vehicles in high-security areas.
* Law Enforcement: Detect stolen or wanted vehicles by comparing license plate data with a pre-existing database of vehicles of interest.
* Toll Collection: Automate toll collection by reading license plates and associating them with pre-registered payment systems.
* Fleet Management: Keep track of company vehicle movements by recognizing and logging the license plates of fleet vehicles.

-----

**Dataset Details:**

- The dataset is organized into three main folders: test, train, and valid.
* Dataset Contains around 24,200 images along with their corresponding annotated labels.
