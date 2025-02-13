import requests
import os


def download_file_from_google_drive(id, destination):
    URL = "https://drive.google.com/uc?id=1YtAtL7Amsm-fZoPQGF4hJBC9ijjjwiMk"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


def download_weights():
    print("Downloading senet50 weights...")
    download_file_from_google_drive("1YtAtL7Amsm-fZoPQGF4hJBC9ijjjwiMk",
                                    os.path.join(os.path.abspath(os.path.dirname(__file__)), "senet50_ft_weight.pkl"))
    print("done")


if __name__ == '__main__':
    download_weights()

