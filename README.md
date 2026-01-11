# Automated PCB Defect Inspection System

## Overview
This project implements an **Automated Quality Inspection System** for **Printed Circuit Boards (PCBs)** using **YOLOv5 and PyTorch**.  
It detects, classifies, and localizes PCB defects, providing **confidence scores, defect coordinates**, and **severity analysis**.  

The system generates:
- Annotated images with bounding boxes
- CSV report of defects
- Severity graphs



## Key Features
- Detects multiple PCB defects: missing holes, short circuits, scratches, mouse bites  
- Classifies defects with confidence scores  
- Outputs defect center coordinates `(x, y)`  
- Computes defect severity (normalized bounding box area)  
- Generates CSV report and severity bar chart  



## Tech Stack
- Python 3.12  
- PyTorch 2.9.1  
- YOLOv5 
- OpenCV, Pandas, Matplotlib  


# Quick Setup

bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate
# Install dependencies
pip install --upgrade pip
pip install torch torchvision opencv-python pandas matplotlib

Run Script

Set your model weights path in pcb_inspection_baseline.py:

WEIGHTS = "/path/to/runs/weights/baseline.pt"


Run the inspection:

python pcb_inspection_baseline.py


Outputs will be saved in sample_outputs/:

Annotated images (*.jpg)

defect_analysis.csv containing defect type, confidence, center coordinates, and severity
severity_graph.png visualizing average severity per defect type
Input Images 

<img src="01_missing_hole_01.jpg" width="400" alt="Annotated PCB Image"> <br> <img src="06_short_06 copy.jpg" width="400" alt="Annotated PCB Image">
<br>
Sample Outputs
Annotated PCB Images
<img src="01_missing_hole_01 copy.jpg" width="400" alt="Annotated PCB Image"><br> <img src="06_short_06.jpg" width="400" alt="Annotated PCB Image">
and many more in the folder You can check it 
<br>
Severity Graph
<img src="severity_graph.png" width="600" alt="Severity Graph">

CSV Data Example
image	defect_type	confidence	center_x	center_y	severity
01_missing_hole_01.jpg	missing_hole	0.92	150	230	0.05
06_short_06.jpg	short	0.88	310	120	0.08
11_mouse_bite_03.jpg	mouse_bite	0.95	250	200	0.07

 Folder Struture
 <h2>Technical Challenges & Solutions</h2>

<table border="1" cellpadding="8" cellspacing="0" width="100%">
  <thead style="background-color:#2c3e50; color:white;">
    <tr>
      <th>Problem</th>
      <th>Observation</th>
      <th>Solution</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>YOLO model not found</td>
      <td>Script couldn’t locate <code>baseline.pt</code></td>
      <td>Used absolute path to the weights file</td>
    </tr>
    <tr>
      <td>Fallback to default model</td>
      <td>YOLOv5 loaded default <code>yolov5s</code></td>
      <td>Used <code>force_reload=True</code> to load custom model</td>
    </tr>
    <tr>
      <td>Slow CPU inference</td>
      <td>Processing multiple images took longer time</td>
      <td>Implemented batch processing and optional GPU detection</td>
    </tr>
    <tr>
      <td>PyTorch warnings</td>
      <td>Deprecated <code>autocast</code> warnings appeared</td>
      <td>Suppressed warnings using <code>warnings.filterwarnings("ignore")</code></td>
    </tr>
    <tr>
      <td>Defining defect severity</td>
      <td>No built-in severity metric available</td>
      <td>Computed normalized bounding box area (0–1 scale)</td>
    </tr>
    <tr>
      <td>Multiple outputs & reports</td>
      <td>Required CSV reports and performance graphs</td>
      <td>Integrated Pandas CSV export and Matplotlib graph generation</td>
    </tr>
  </tbody>
</table>
<style>
table {
  border-collapse: collapse;
  font-family: Arial, sans-serif;
}
th, td {
  text-align: left;
}
tr:nth-child(even) {
  background-color: #f2f2f2;
}
</style>




  # Main Program Location is in  Scripts/perfect.py // program to run 

Challenges & Solutions
Problem	Solution
YOLO model not found	Used absolute path to weights file
Slow CPU inference	Optional GPU support / batch processing
Defining severity	Computed normalized bounding box area
Multiple outputs	Integrated CSV export and Matplotlib graphs

Future Enhancements

Confidence threshold filtering

Real-time PCB inspection with cameras

Color-coded bounding boxes per defect type

Advanced defect prioritization metrics

Link of The video demo 
Here :-
https://drive.google.com/file/d/16YuD5963cQ60LJbAYh3ttZVEb9CnSUX_/view?usp=drive_link

Data with Program files(Zip file of Full programm)
 Here the drive link is there 
 https://drive.google.com/file/d/1GrnNvKw6nvDgyWCOmIR2j350SRNdoKUN/view?usp=drive_link
 

