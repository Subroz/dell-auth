import requests
import os

token = os.environ.get("token")

def folder_ext(id=None):
	if id:
		url = f"https://www.seedr.cc/api/folder/{id}?access_token={token}"
	else:
		url = f"https://www.seedr.cc/api/folder?access_token={token}"

	print(url)
	r = requests.get(url)
	print(r.json())
	return r.json()

def fetch_file(folder_file_id):
	url = "https://www.seedr.cc/oauth_test/resource.php"
	data = {"access_token" : token, "func" : "fetch_file", "folder_file_id" : folder_file_id }
	r = requests.post(url, data=data)
	print(r.json())
	return r.json()
	
def addMagnet(magnet):
	url = "https://www.seedr.cc/oauth_test/resource.php"
	data = {"access_token" : token, "func" : "add_torrent", "torrent_magnet" : magnet }
	r = requests.post(url, data=data)
	print(r.json())
	return r.json()
	

if __name__ == "__main__":
	folder_ext()