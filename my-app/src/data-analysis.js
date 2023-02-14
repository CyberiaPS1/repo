const mongodb = require('mongodb');
const pd = require('pandas');

async function analyzeData() {
  // Connect to the MongoDB database
  const client = await mongodb.MongoClient.connect("mongodb+srv://Cru:8NPXXAVN2DSfsAHa@cluster0.al2xj16.mongodb.net/test");
  const db = client.db("Rey");
  const collection = db.collection("transcripts");

  // Retrieve the documents from the collection
  const documents = await collection.find().toArray();

  // Convert the documents to a Pandas DataFrame
  const df = pd.DataFrame(Array.from(documents));

  // Load the data into a Pandas DataFrame
  const data = pd.read_csv('data.csv');

  // Use Numpy to perform numerical computations on the data
  const mean = pd.mean(data);
  const median = pd.median(data);
  const stddev = pd.std(data);

  return { mean, median, stddev };
}

module.exports = analyzeData;


export default analyzeData;
