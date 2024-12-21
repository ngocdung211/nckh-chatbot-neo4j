import pandas as pd

# Replace 'file1.csv' and 'file2.csv' with your actual file paths
df1 = pd.read_csv('/Users/admin/Working/nckh-chatbot-neo4j/chatbot_api/src/test_set/test_set_with_web_FIT_20-12_2.csv')
df2 = pd.read_csv('/Users/admin/Working/nckh-chatbot-neo4j/chatbot_api/src/test_set/test_set_with_web_FIT_20-12_3.csv')

# Concatenate vertically
concatenated_df = pd.concat([df1, df2], axis=0, ignore_index=True)

# Display the concatenated DataFrame
print(concatenated_df.head())
concatenated_df.to_csv("fit_data.csv")