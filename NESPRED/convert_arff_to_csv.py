import pandas as pd
from scipy.io import arff

# Replace 'input.arff' and 'output.csv' with your file names
input_arff_file = 'input.arff'
output_csv_file = 'output.csv'

# Load ARFF file using scipy
data = arff.loadarff(input_arff_file)

# Convert to Pandas DataFrame
df = pd.DataFrame(data[0])

# Save DataFrame to CSV
df.to_csv(output_csv_file, index=False)
