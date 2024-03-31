import requests
import os
import hashlib
from tqdm import tqdm
import tarfile
import gzip

# replace with your API url and Bearer Token
bearer_token = 'eyJraWQiOiJaUk14Z2gwZHg0UnRGVGR1VlhpZm9pa2U0bVJGaVlKN1lmMmVZSUxUblpZPSIsImFsZyI6IlJTMjU2In0.eyJjdXN0b206bmV3c19sZXR0ZXIiOiIxIiwiY3VzdG9tOmNvdW50cnkiOiJVbml0ZWQgU3RhdGVzIiwic3ViIjoiOGY1Y2I1ZGMtNDNmZi00NjlhLWI0MTMtNTNiZjUwYzBkNTQzIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0c1NWVQenVzcCIsImNvZ25pdG86dXNlcm5hbWUiOiI4ZjVjYjVkYy00M2ZmLTQ2OWEtYjQxMy01M2JmNTBjMGQ1NDMiLCJnaXZlbl9uYW1lIjoiU2hpeXUiLCJjdXN0b206Y29tcGFueSI6IlNhZmVBSSIsImF1ZCI6IjdmcTVqdnM1ZmZzMWM1MGhkM3Rvb2JiM2I5IiwiZXZlbnRfaWQiOiJjOGI2NDEyMC05MGM4LTQxNTAtODNjNC1iN2M4YTYyOWMyOWQiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTcxMTg0MzI4MywiZXhwIjoxNzExODU3NjQ5LCJpYXQiOjE3MTE4NTQwNDksImZhbWlseV9uYW1lIjoiU29uZyIsImVtYWlsIjoic2hpeXVzQHNhZmVhaS5haSJ9.As2s4V_Gylv-oNfT4lsZxehvj4HgawWEhi07q2HK4twZwwCpxcWbCZZTF-ob2znvYEinODVnREFTq0pC5s33xxPVkW8AQRU1znWEFL_ZgY_kL6vszSC_2uoSd7s2ETOcAm49ZXiY_5dieJVnDbvZKMpJeRAszpwfiMm_nOJ6_LeT21lm7Zj4PVAP6zFDTBbrMZ4kgajnyKu69gD7PVRMEkTHAhK4dY-Dy2Wt-uXRXOte_5ZdgXZ0sHC08APJkZDHEgevIfNyWJ0yeIusJSX85re3uOdUN0H-CuffeCepKXoBr0DVijPVu6N0SfgLJZWkUJjcMUfxFGdOmt4B_x-16g'

output_dir = "/path/to/save"
extract_dir_suffix = "/../v1.0"
region = 'us' # 'us' or 'asia'


download_files = {
    "v1.0-test_meta.tgz":"b0263f5c41b780a5a10ede2da99539eb",
    "v1.0-test_blobs.tgz":"e065445b6019ecc15c70ad9d99c47b33",
    "v1.0-trainval01_blobs.tgz":"cbf32d2ea6996fc599b32f724e7ce8f2",
    "v1.0-trainval02_blobs.tgz":"aeecea4878ec3831d316b382bb2f72da",
    "v1.0-trainval03_blobs.tgz":"595c29528351060f94c935e3aaf7b995",
    "v1.0-trainval04_blobs.tgz":"b55eae9b4aa786b478858a3fc92fb72d",
    "v1.0-trainval05_blobs.tgz":"1c815ed607a11be7446dcd4ba0e71ed0",
    "v1.0-trainval06_blobs.tgz":"7273eeea36e712be290472859063a678",
    "v1.0-trainval07_blobs.tgz":"46674d2b2b852b7a857d2c9a87fc755f",
    "v1.0-trainval08_blobs.tgz":"37524bd4edee2ab99678909334313adf",
    "v1.0-trainval09_blobs.tgz":"a7fcd6d9c0934e4052005aa0b84615c0",
    "v1.0-trainval10_blobs.tgz":"31e795f2c13f62533c727119b822d739",
    "v1.0-trainval_meta.tgz":"537d3954ec34e5bcb89a35d4f6fb0d4a",
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
            extract_tgz_to_original_folder(save_file) + extract_dir_suffix
        elif output_name.endswith(".tar"):
            extract_tar_to_original_folder(save_file) + extract_dir_suffix
        else:
            print("unknow file type",output_name)

    print("Done!")

if __name__ == "__main__":
    main()
