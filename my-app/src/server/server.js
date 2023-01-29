const express = require('express');
const app = express();
const mongo = require('mongodb');
const multer = require('multer');
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

app.listen(3000, () => {
  console.log('Server started on port 3000');
});

  
