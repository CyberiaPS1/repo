import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

function FileUploadForm() {
  const [result, setResult] = useState(null);

  const onDrop = useCallback(acceptedFiles => {
    const file = acceptedFiles[0];
    uploadFile(file);
  }, []);

  const uploadFile = (file) => {
    const formData = new FormData();
    formData.append('file', file);
    axios.post('http://localhost:8080/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(response => {
      setResult(response.data.result);
    }).catch(error => {
      console.error(error);
    });
  };

  const {getRootProps, getInputProps, isDragActive} = useDropzone({
    onDrop,
    accept: 'audio/*, text/*'
  });

  return (
    <div {...getRootProps()} className="file-upload-form">
      <input {...getInputProps()} />
      {
        isDragActive ?
          <p>Drop the files here ...</p> :
          <p>Drag and drop a file here, or click to select a file</p>
      }
      {
        result &&
        <p>Result: {result}</p>
      }
    </div>
  );
}

export default FileUploadForm;
