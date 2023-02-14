import React, { Component } from 'react';
import axios from 'axios';
import { connect as connectMongo, close as closeMongo, collection } from './db';

class UploadForm extends Component {
  state = {
    selectedFile: null,
    score: null,
    error: null,
    loading: false,
    collection: null
  }

  componentDidMount() {
    connectMongo().then(coll => {
      this.setState({ collection: coll });
    });
  }

  componentWillUnmount() {
    closeMongo();
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
        this.state.collection.insertOne({
          file: this.state.selectedFile.name,
          score: res.data.score
        });
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
          selectedFile && <
