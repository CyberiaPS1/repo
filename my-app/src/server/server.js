const mongoose = require('mongoose')
mongoose.connect('mongodb://<dbuser>:<dbpassword>@<dbhost>:<dbport>/<dbname>', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://Ryan:flkajsdhfkdljsfh8fdlhjdslkjds90@cluster.mongodb.net/test?retryWrites=true&w=majority";
const client = new MongoClient(uri, { useNewUrlParser: true });
client.connect(err => {
  const collection = client.db("test").collection("devices");
  // perform actions on the collection object
  client.close();
});

const multer = require('multer');
const express = require('express');
const app = express();
const mongo = require('mongodb');
const upload = multer({ dest: 'uploads/' });

app.post('/upload', upload.single('file'), (req, res) => {
  // access the file and perform the logic here
  console.log(req.file);
  // Perform the logic of processing the file and assign score
  // for example you could use some library that parse the file,
  // and based on certain criteria you can assign a score.
  // You can then store the score and the file in your MongoDB 
  // database using MongoClient
  res.send("file received and processed");
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
  console.log('Connected to MongoDB');
});


const fs = require('fs');
const fileContent = fs.readFileSync(req.file.path);

if (words > 1000) {
  var score = 100;
} else if (words < 500) {
  var score = 50;
}
console.log("score: " + score);
 
app.listen(3000, () => console.log('Server started'));
