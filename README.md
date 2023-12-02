# Nuscenes Download
This script is used for downloading and extracting the complete NuScenes dataset. Please use it responsibly and solely for educational and research purposes.

### Usage

1. Please register and log in at [https://www.nuscenes.org/nuscenes](https://www.nuscenes.org/nuscenes) to obtain access permissions.
2. Use the browser's developer tools (F12) to monitor network requests. Click on any download link in the Full Dataset section and find the Bearer Token from the headers of the monitored download link.
3. Insert the Bearer Token into the `bearer_token` variable in the `nuscenes_download.py` script.
4. Set the `output_dir` and `region` variables.
5. Run the `nuscenes_download.py` script.
