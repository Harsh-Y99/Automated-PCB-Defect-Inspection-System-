import torch
from pathlib import Path
import cv2
import os
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PATHS ----------------
WEIGHTS = "/home/harsh/Desktop/cv_task2/Task_2_Quality_Inspection/runs/weights/baseline.pt"  # trained PCB model
IMG_DIR = "/home/harsh/Desktop/cv_task2/Task_2_Quality_Inspection/dataset/images/test"
OUTPUT_DIR = "/home/harsh/Desktop/cv_task2/Task_2_Quality_Inspection/sample_outputs"
CSV_PATH = os.path.join(OUTPUT_DIR, "defect_analysis.csv")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- DEVICE ----------------
device = "cuda" if torch.cuda.is_available() else "cpu"

# ---------------- LOAD MODEL ----------------
model = torch.hub.load('ultralytics/yolov5', 'custom', path=WEIGHTS, force_reload=True)
model.to(device)
model.eval()

# ---------------- INFERENCE ----------------
img_paths = list(Path(IMG_DIR).glob("*.jpg"))
all_data = []

for img_path in img_paths:
    img = cv2.imread(str(img_path))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = model(img_rgb)

    # Loop over detections
    for *box, conf, cls in results.xyxy[0]:
        x1, y1, x2, y2 = map(int, box)
        label = model.names[int(cls)]
        conf_score = float(conf)

        # Defect center coordinates
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        # Defect severity (simple: area of bbox normalized by image area)
        img_area = img.shape[0] * img.shape[1]
        bbox_area = (x2 - x1) * (y2 - y1)
        severity = round(bbox_area / img_area, 3)  # normalized 0-1

        # Draw bounding box and label
        color = (0, 0, 255)  # red for defect
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, f"{label} {conf_score:.2f}", (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Append to data list
        all_data.append({
            "image": img_path.name,
            "defect_type": label,
            "confidence": conf_score,
            "center_x": cx,
            "center_y": cy,
            "severity": severity
        })

    # Save annotated image
    out_path = os.path.join(OUTPUT_DIR, img_path.name)
    cv2.imwrite(out_path, img)
    print(f"[SAVED] {out_path}")

# ---------------- SAVE CSV ----------------
df = pd.DataFrame(all_data)
df.to_csv(CSV_PATH, index=False)
print(f"✅ Defect analysis saved to {CSV_PATH}")

# ---------------- PLOT SEVERITY ----------------
plt.figure(figsize=(8,5))
severity_summary = df.groupby("defect_type")["severity"].mean().sort_values(ascending=False)
severity_summary.plot(kind="bar", color="tomato")
plt.title("Average Defect Severity by Type")
plt.ylabel("Severity (normalized)")
plt.xlabel("Defect Type")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "severity_graph.png"))
plt.show()
print(f"✅ Severity graph saved to {OUTPUT_DIR}/severity_graph.png")
