import requests


def download_url(url, save_path, chunk_size=10000):
    """
    Download the file present on url to the path save_path

    Arg:
        url (str): url to download data from
        save_path (str): where to store file
        chunk_size (int): size of chunks for request library
    """
    response = requests.get(url, stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, position=0, leave=True)

    with open(save_path, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=chunk_size):
            progress_bar.update(len(chunk))

            fd.write(chunk)
    progress_bar.close()


def extract_tar(tar_path):
    """
    Extract a tar file inplace

    Args:
        tar_path (str): path to the .tar or .tar.gz file
    """
    if tar_path.name.endswith("tar.gz"):
        tar = tarfile.open(tar_path, "r:gz")
        tar.extractall(tar_path.parent)
        tar.close()
    elif tar_path.name.endswith("tar"):
        tar = tarfile.open(tar_path, "r:")
        tar.extractall(tar_path.parent)
        tar.close()

