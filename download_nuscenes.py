import requests
import os
import hashlib
from tqdm import tqdm
import tarfile
import gzip

# replace with your API url and Bearer Token
bearer_token = 'eyJraWQiOiJaUk14Z2gwZHg0UnRGVGR1VlhpZm9pa2U0bVJGaVlKN1lm'

output_dir = "/path/to/save"
region = 'asia' # 'us' or 'asia'


download_files = {
    "v1.0-trainval_meta.tgz":"3eee698806fcf52330faa2e682b9f3a1",
    "v1.0-trainval01_blobs.tgz":"8b5eaecef969aea173a5317be153ca63",
    "v1.0-trainval02_blobs.tgz":"116085f49ec4c60958f9d49b2bd6bfdd",
    "v1.0-trainval03_blobs.tgz":"9de7f2a72864d6f9ef5ce0b74e84d311",
    "v1.0-trainval04_blobs.tgz":"4d0bec5cc581672bb557c777cd0f0556",
    "v1.0-trainval05_blobs.tgz":"3747bb98cdfeb60f29b236a61b95d66a",
    "v1.0-trainval06_blobs.tgz":"9f6948a19b1104385c30ad58ab64dabb",
    "v1.0-trainval07_blobs.tgz":"d92529729f5506f5f0cc15cc82070c1b",
    "v1.0-trainval08_blobs.tgz":"90897e7b58ea38634555c2b9583f4ada",
    "v1.0-trainval09_blobs.tgz":"7cf0ac8b8d9925edbb6f23b96c0cd1cb",
    "v1.0-trainval10_blobs.tgz":"fedf0df4e82630abb2d3d517be12ef9d",
    "v1.0-test_meta.tgz":"f473fa9bb4d91e44ace5989d91419a46",
    "v1.0-test_blobs.tgz":"3e1b78da1e08eed076ab3df082a54366",
}

# set request header
headers = {
    'Authorization': f'Bearer {bearer_token}',
    'Content-Type': 'application/json',
}

def download_file(url, save_file,md5):
    response = requests.get(url, stream=True)
    if save_file.endswith(".tgz"):
        content_type = response.headers.get('Content-Type', '')
        if content_type == 'application/x-tar':
            save_file = save_file.replace('.tgz', '.tar')
        elif content_type != 'application/octet-stream':
            print("unknow content type",content_type)
            return save_file

    if os.path.exists(save_file):
        print(save_file,"has downloaded")
        # check md5
        md5obj = hashlib.md5()
        with open(save_file, 'rb') as file:
            for chunk in file:
                md5obj.update(chunk)
        hash = md5obj.hexdigest()
        if hash != md5:
            print(save_file,"check md5 failed,download again")
        else:
            print(save_file,"check md5 success")
            return save_file
        
    file_size = int(response.headers.get('Content-Length', 0))
    progress_bar = tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024,desc=save_file, ascii=True)


    # save file & check md5
    md5obj = hashlib.md5()
    with open(save_file, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                md5obj.update(chunk)
                file.write(chunk)
                progress_bar.update(len(chunk))
    progress_bar.close()

    hash = md5obj.hexdigest()
    if hash != md5:
        print(save_file,"check md5 failed")
    else:
        print(save_file,"check md5 success")

    return save_file




def extract_tgz_to_original_folder(tgz_file_path):
    original_folder = os.path.dirname(tgz_file_path)
    print(f"Extracting {tgz_file_path} to {original_folder}")

    with gzip.open(tgz_file_path, 'rb') as f_in:
        with tarfile.open(fileobj=f_in, mode='r') as tar:
            tar.extractall(original_folder)

def extract_tar_to_original_folder(tar_file_path):
    original_folder = os.path.dirname(tar_file_path)
    print(f"Extracting {tar_file_path} to {original_folder}")

    with tarfile.open(tar_file_path, 'r') as tar:
        tar.extractall(original_folder)

def main():
    print("Getting download urls...")
    download_data = {}
    for filename,md5 in download_files.items():
        api_url = f'https://o9k5xn5546.execute-api.us-east-1.amazonaws.com/v1/archives/v1.0/{filename}?region={region}&project=nuScenes'

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            print(filename,'request success')
            download_url = response.json()['url']
            download_data[filename] = [download_url,os.path.join(output_dir,filename),md5]
        else:
            print(f'request failed : {response.status_code}')
            print(response.text)

    print("Downloading files...")

    os.makedirs(output_dir,exist_ok=True)
    for output_name,(download_url,save_file,md5) in download_data.items():
        save_file = download_file(download_url,save_file,md5)
        download_data[output_name] = [download_url,save_file,md5]

    print("Extracting files...")
    for output_name,(download_url,save_file,md5) in download_data.items():
        if output_name.endswith(".tgz"):
            extract_tgz_to_original_folder(save_file)
        elif output_name.endswith(".tar"):
            extract_tar_to_original_folder(save_file)
        else:
            print("unknow file type",output_name)

    print("Done!")

if __name__ == "__main__":
    main()