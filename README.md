# Nuscenes Download
This script is used for downloading and extracting the complete NuScenes dataset. Please use it responsibly and solely for educational and research purposes.

### Usage

1. Please register and log in at [https://www.nuscenes.org/nuscenes](https://www.nuscenes.org/nuscenes) to obtain access permissions.
2. Use the browser's developer tools (F12) to monitor network requests. Click on any download link in the Full Dataset section and find the Bearer Token from the headers of the monitored download link.
3. Insert the Bearer Token into the `bearer_token` variable in the `nuscenes_download.py` script.
4. Set the `output_dir` and `region` variables.
5. Run the `nuscenes_download.py` script.

```python
# replace with your API url and Bearer Token
bearer_token = 'eyJraWQiOiJaUk14Z2gwZHg0UnRGVGR1VlhpZm9pa2U0bVJGaVlKN1lm'

output_dir = "/path/to/save"
region = 'asia' # 'us' or 'asia'

```