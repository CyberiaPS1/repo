import pandas as pd
from scipy.io import arff

# Replace 'your_file.arff' and 'output.xlsx' with your file names
input_arff_file = 'file158f7013d8f0.arff'
output_excel_file = 'output.xlsx'

# Load ARFF file using scipy
with open(input_arff_file, 'rb') as f:
    data = arff.loadarff(f)

# Convert to Pandas DataFrame
df = pd.DataFrame(data[0])

# Save DataFrame to Excel
df.to_excel(output_excel_file, index=False)
