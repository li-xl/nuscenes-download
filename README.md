# Nuscenes Download
This script is used for downloading and extracting the complete NuScenes dataset. Please use it responsibly and solely for educational and research purposes.

### What's New

Updated the md5sum (from [songshiyu01](https://github.com/songshiyu01)) & Automation of getting bearer token (from [harsanyidani](https://github.com/harsanyidani))

### Usage

1. Please register and log in at [https://www.nuscenes.org/nuscenes](https://www.nuscenes.org/nuscenes) to obtain access permissions.
2. Set the `useremail`, `password`, `output_dir` and  `region` variables.
3. Run the `download_nuscenes.py` script.

```python
# replace your email and password in https://www.nuscenes.org/
useremail = "your_email"
password = "your_password"

output_dir = "/path/to/save"
region = 'asia' # 'us' or 'asia'

```

### Acknowledgement
Many thanks to the following open-source projects:
1. https://github.com/Syzygianinfern0/NuPlan-Download-CLI

