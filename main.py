
import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from dotenv import load_dotenv

load_dotenv(".env")
UPLOAD_FOLDER = os.getcwd() + "/cache"
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_to_blob(file_name):
    try:
        print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")
        # Quick start code goes here
        AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING') 
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

        # Create a unique name for the container
        CONTAINER_NAME = os.getenv("CONTAINER_NAME")

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file_name)

        print("\nUploading to Azure Storage as blob:\n\t" + file_name)

        # Upload the created file
        with open(f'./cache/{file_name}', "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        os.remove(f'./cache/{file_name}')
    except Exception as ex:
        print('Exception:')
        print(ex)
    
    
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            save_to_blob(filename)
            return "Upload Success"
    return render_template('home.html')
    
if __name__ == "__main__":
    app.secret_key= os.urandom(16)
    app.run(debug=True)
    
    