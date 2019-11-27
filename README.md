Run locally

1. cd flask-app
2. pip install -r requirements.txt
2. python app.py


Run in docker

1. Install docker
2. docker build . -t imgurl-demo
3. docker run -it -p 8080:5000 imgurl-demo
4. Go to http://0.0.0.0:8080/


Run in kubernetes
1. Set up gcloud account (see google documentation)
2. Set up kubernetes cluster (see google documentation) 
3. Create a storage bucket named pexip-demo-files
4. Create credentials that can access the bucket and copy it to the file storage-credentials.txt 
5. Change the settings in app.py to use external storage **_app.config['USE_EXTERNAL_STORAGE'] = False_**
5. Init gcloud and kubectl to use your created cluster
6. Install skaffold (https://skaffold.dev/docs/install/)
7. skaffold run --tail
8. 'kubectl get services' to find the IP to connect to


Credentials
To store the files in  


Test:
curl -i -X POST host:port/post-file -H "Content-Type: image/jpeg" --data-binary "@path/to/file"

eg.
curl -i -X POST 0.0.0.0:5000/api/v1/images -H "Content-Type: image/png" --data-binary "phone-lookup.png"

check the file by going to:
0.0.0.0:5000/api/v1/images/<image name returned by the post>
Change size by going adding one of the size requirements like so
0.0.0.0:5000/api/v1/images/small/<image name returned by the post>

