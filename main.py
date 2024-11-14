import subprocess
import csv
import json
from datetime import datetime
import sys

def get_images_from_helm_chart(chart_name, chart_version):
    """
    Renders the Helm chart and extracts all container images.
    """
    try:
        helm_cmd = [
            'helm', 'template', '--version', chart_version, chart_name
        ]
        result = subprocess.run(helm_cmd, capture_output=True, text=True, check=True)
        
        images = set()
        for line in result.stdout.splitlines():
            if 'image:' in line:
                image = line.split("image:")[-1].strip()
                images.add(image)
        return list(images)
    except subprocess.CalledProcessError as e:
        print(f"Error rendering Helm chart: {e.stderr}")
        sys.exit(1)

def scan_image_with_grype(image):
    """
    Scans a container image for vulnerabilities using Grype.
    """
    try:
        grype_cmd = ['grype', image, '-o', 'json']
        result = subprocess.run(grype_cmd, capture_output=True, text=True, check=True)
        scan_results = json.loads(result.stdout)

        vulnerabilities = []
        for item in scan_results.get("matches", []):
            vuln = item["vulnerability"]
            severity = vuln["severity"]
            if severity in ["Medium", "High", "Critical"]:
                vulnerabilities.append({
                    "image": image,
                    "component": item["artifact"]["name"],
                    "vulnerability": vuln["id"],
                    "severity": severity
                })
        return vulnerabilities
    except subprocess.CalledProcessError as e:
        print(f"Error scanning image {image}: {e.stderr}")
        return []

def save_vulnerabilities_to_csv(vulnerabilities):
    """
    Saves vulnerability object list to a CSV file.
    """
    filename = f"{datetime.now().strftime('%Y-%m-%d')}_vulnerability_report.csv"
    with open(filename, mode='w', newline='') as csv_file:
        fieldnames = ['image:tag', 'component/library', 'vulnerability', 'severity']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for vuln in vulnerabilities:
            writer.writerow({
                'image:tag': vuln['image'],
                'component/library': vuln['component'],
                'vulnerability': vuln['vulnerability'],
                'severity': vuln['severity']
            })
    print(f"Vulnerability report saved to {filename}")

def main(chart_name, chart_version):
    images = get_images_from_helm_chart(chart_name, chart_version)
    

    print("Images found in {chart_name}:")
    for image in images:
        print(f"- {image}")

    all_vulnerabilities = []

    print("\nStarting scan for each images...")
    for image in images:
        print(f"Scanning image: {image}")
        vulnerabilities = scan_image_with_grype(image)
        all_vulnerabilities.extend(vulnerabilities)

    if all_vulnerabilities:
        save_vulnerabilities_to_csv(all_vulnerabilities)
    else:
        print("No vulnerabilities found with severity level Medium or higher.")

    print("Scan and report generation complete.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <chart_name> <chart_version>")
        sys.exit(1)

    chart_name = sys.argv[1]
    chart_version = sys.argv[2]
    main(chart_name, chart_version)
