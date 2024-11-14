# Helm Chart Vulnerability Scanner

## Project Description

This is Python-based CLI tool designed to scan container images specified in a Helm chart for vulnerabilities. It retrieves images from a specified Helm chart, scans each image using Anchore's Grype tool, and outputs a CSV report with vulnerabilities of severity.

## Setup and Run Instructions

### Prerequisites

1. **Python 3.10+**: Make sure Python is installed on your system.
2. **Helm CLI**: Install the Helm command-line tool: https://helm.sh/docs/intro/install/.
3. **Grype CLI**: Install Grype for vulnerability scanning: https://github.com/anchore/grype/#Installation

### Instructions

1. **Clone the Repository**:

   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Add Necessary Helm Repositories**:
   For example, if you’re scanning an `argo` chart, add its repository with:

   ```bash
   helm repo add argo https://argoproj.github.io/argo-helm
   helm repo update
   ```

3. **Run the Script**:

   ```bash
   python main.py <chart_name> <chart_version>
   ```

   Replace `<chart_name>` and `<chart_version>` with the specific Helm chart name and version you wish to scan.

4. **Output**:
   - The script will output a CSV report named `{date}_vulnerability_report.csv` with the following columns:
     - `image:tag`
     - `component/library`
     - `vulnerability`
     - `severity`
   - Only vulnerabilities with severity "Medium" or higher are listed (which can be changed in main.py).

## Assumptions and Design Decisions

- **Vulnerability Severity Filtering**: Only vulnerabilities with a severity level of "Medium" or higher are reported. This design choice focuses on significant security risks, assuming that lower-severity vulnerabilities may not require immediate attention.
- **Repository Dependencies**: It is assumed that users will add any necessary Helm repositories before running the script. This decision was made to keep the script flexible and avoid hardcoding repositories.

## AI Assistance

AI assistance was used in the development of this project to:

- **Filtering grype output in `scan_image_with_grype`**: Used AI to better filter output coming from grype command and storing it into list of objects according to severity. 
- **Debugging**: Fixed few errors while writing data into file (like it suggested using csv.DictWriter).Also it suggested me to use `helm template` command instead for searching for helm chart repo for images.
- **Documentation**: Used AI for Initial README format.
## Future Improvements

Given more time, the following enhancements could be made:

1. **Enhanced Error Handling**: Should have implement more detailed error handling.
2. **Report Customization**: Added options to specify output format (e.g., JSON, HTML).
3. **Parallelized Scanning**: Used parallel processing for scanning images to speed up the process for multiple images.
4. **Automated Repository Management**: Automatically add and update Helm repositories based on user input, reducing setup time.
