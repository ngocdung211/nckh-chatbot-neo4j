import pandas as pd

# Replace 'file1.csv' and 'file2.csv' with your actual file paths
df1 = pd.read_csv('/Users/admin/Working/nckh-chatbot-neo4j/chatbot_api/src/openai_result/first_result_test_openai_set_fit_241221-1520_2.csv')
df2 = pd.read_csv('/Users/admin/Working/nckh-chatbot-neo4j/chatbot_api/src/openai_result/result_test_openai_set_fit_241221-1428_2.csv')
df3 = pd.read_csv('/Users/admin/Working/nckh-chatbot-neo4j/chatbot_api/src/openai_result/second_result_test_openai_set_fit_241221-1520_2.csv')

# Concatenate vertically
concatenated_df = pd.concat([df1, df2, df3], axis=0, ignore_index=True)

# Display the concatenated DataFrame
print(concatenated_df.head())
concatenated_df.to_csv("final_result.csv")