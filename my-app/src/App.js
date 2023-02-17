import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import analyzeDataModule from './data-analysis.js';

const App = () => {
  // State variables
  const [files, setFiles] = useState([]);
  const [results, setResults] = useState(null);

  // Dropzone configuration
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: 'image/*',
    onDrop: acceptedFiles => {
      setFiles(acceptedFiles.map(file => Object.assign(file, {
        preview: URL.createObjectURL(file)
      })));

      // Analyze the data and set the results state
      setResults(analyzeDataModule());
    }
  });

  // Remove file from the state
  const handleRemoveFile = (file) => {
    setFiles(files.filter(f => f !== file));
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="dropzone-container" {...getRootProps()}>
          <input {...getInputProps()} />
          {
            isDragActive ?
              <p>Drop the files here ...</p> :
              <p>Drag 'n' drop some files here, or click to select files</p>
          }
        </div>
        <div className="preview-container">
          {
            files.map(file => (
              <div className="preview-item" key={file.name}>
                <img src={file.preview} alt="preview" />
                <div className="preview-item-footer">
                  <p>{file.name}</p>
                  <button onClick={() => handleRemoveFile(file)}>Remove</button>
                </div>
              </div>
            ))
          }
        </div>
        { results && <p>{results}</p> }
      </header>
    </div>
  );
};

export default App;
