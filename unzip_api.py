from fastapi import FastAPI, File, UploadFile
import zipfile
import tempfile
import shutil
import os
import base64

app = FastAPI()

@app.post("/unzip/")
async def unzip_file(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as temp_zip:
        shutil.copyfileobj(file.file, temp_zip)
        temp_zip_path = temp_zip.name

    extract_dir = tempfile.mkdtemp()

    try:
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            file_list = []
            for fname in os.listdir(extract_dir):
                full_path = os.path.join(extract_dir, fname)
                if os.path.isfile(full_path):
                    with open(full_path, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode()
                    file_list.append({
                        "filename": fname,
                        "data": b64
                    })
        return {"files": file_list}
    finally:
        os.unlink(temp_zip_path)
        shutil.rmtree(extract_dir)