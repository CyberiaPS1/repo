import React, { Component } from 'react';
import pymongo from 'pymongo';

class DataComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: []
    };
  }

  componentDidMount() {
    const client = pymongo.MongoClient("mongodb+srv://Cru:8NPXXAVN2DSfsAHa@cluster0.al2xj16.mongodb.net/test");
    const db = client["Rey"];
    const collection = db["transcripts"];

    collection.find().toArray((error, data) => {
      if (error) {
        console.error(error);
      } else {
        this.setState({ data });
      }
    });
  }

  render() {
    const { data } = this.state;
    return (
      <div>
        {data.map(datum => (
          <div key={datum._id}>{datum.transcript}</div>
        ))}
      </div>
    );
  }
}

export default DataComponent;
