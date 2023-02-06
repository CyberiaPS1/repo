import React, { Component } from 'react';
import axios from 'axios';

class UploadForm extends Component {
  state = {
    selectedFile: null,
    score: null,
    error: null,
    loading: false
  }

  handleFileChange = event => {
    this.setState({ selectedFile: event.target.files[0] });
  }

  handleSubmit = event => {
    event.preventDefault();
    this.setState({ loading: true });

    const formData = new FormData();
    formData.append('file', this.state.selectedFile);

    axios.post('/upload', formData)
      .then(res => {
        this.setState({ score: res.data.score });
      })
      .catch(err => {
        this.setState({ error: err });
      })
      .finally(() => {
        this.setState({ loading: false });
      });
  }

  render() {
    const { selectedFile, score, error, loading } = this.state;

    return (
      <form onSubmit={this.handleSubmit}>
        <input type="file" onChange={this.handleFileChange} />
        <button type="submit" disabled={loading}>Upload</button>
        {
          selectedFile && <p>Selected file: {selectedFile.name}</p>
        }
        {
          score && <p>Score: {score}</p>
        }
        {
          error && <p>Error: {error.message}</p>
        }
        {
          loading && <p>Loading...</p>
        }
      </form>
    );
  }
}

export default UploadForm;
