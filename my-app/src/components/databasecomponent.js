const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://Cru:8NPXXAVN2DSfsAHa@cluster0.al2xj16.mongodb.net/test?retryWrites=true&w=majority";
const client = new MongoClient(uri, { useNewUrlParser: true });
client.connect(err => {
const collection = client.db("Rey").collection("transcripts");
// perform actions on the collection object
client.close();
});