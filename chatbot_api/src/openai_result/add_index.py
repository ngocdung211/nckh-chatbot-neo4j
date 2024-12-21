import pandas as pd

# Read the CSV file
filename = "/Users/admin/Working/nckh-chatbot-neo4j/chatbot_api/src/openai_result/second_result_test_openai_set_fit_241221-1520_2.csv"
df = pd.read_csv(filename)

# Display the first few rows and the current index
print(df.head())
print("Current Index:")
print(df.index)

# Example: Setting 'id' column as the index
df.set_index(inplace=True)

# Verify the change
print(df.head())
print("New Index:")
print(df.index)
df.to_csv("second_result_add_id.csv")