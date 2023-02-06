import React, { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';
import { CircularProgress, Button, Typography } from '@material-ui/core';
import { CloudUpload } from '@material-ui/icons';

function UploadForm() {
  const [file, setFile] = useState(null);
  const [score, setScore] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploaded, setUploaded] = useState(false);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: acceptedFiles => setFile(acceptedFiles[0]),
  });

  const handleSubmit = async event => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await axios.post('/upload', formData);
      setScore(response.data.score);
      setUploaded(true);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div {...getRootProps()}>
        <input {...getInputProps()} />
        <Button
          variant={isDragActive ? 'contained' : 'outlined'}
          color={isDragActive ? 'primary' : 'default'}
          startIcon={<CloudUpload />}
          disabled={loading}
        >
          {isDragActive ? 'Drop the file here' : 'Select a file'}
        </Button>
      </div>
      {file && (
        <Typography variant="subtitle2">Selected file: {file.name}</Typography>
      )}
      {uploaded && (
        <Typography variant="subtitle2">Score: {score}</Typography>
      )}
      {error && (
        <Typography variant="subtitle2" color="error">
          Error: {error.message}
        </Typography>
      )}
      {loading && <CircularProgress />}
      <br />
      <br />
      <Button variant="contained" color="primary" type="submit" disabled={loading}>
        Upload
      </Button>
    </form>
  );
}

export default UploadForm;
