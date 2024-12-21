import pandas as pd
# import pandas as pd

# # Load the source CSV with the additional columns
# source_csv = "/Users/admin/Working/nckh-chatbot-neo4j/chatbot_api/src/response_test_set_fit_201224-2013.csv"  # Replace with the filename of the source CSV
# target_csv = "/Users/admin/Working/nckh-chatbot-neo4j/chatbot_api/src/result_openai_201204-2022.csv"  # Replace with the filename of the target CSV
# output_csv = "output.csv"  # Name of the output CSV file

# # Read the CSVs into DataFrames
# source_df = pd.read_csv(source_csv)
# target_df = pd.read_csv(target_csv)

# # Ensure the source has the needed columns
# columns_to_add = ['retriever_time', 'invoke_time']
# if all(col in source_df.columns for col in columns_to_add):
#     # Add the columns from source to target
#     target_df[columns_to_add] = source_df[columns_to_add]
# else:
#     print(f"Source CSV does not contain all required columns: {columns_to_add}")

# # Save the updated target DataFrame to a new CSV
# target_df.to_csv(output_csv, index=False)
# print(f"Updated CSV saved to {output_csv}")


df = pd.read_csv("/Users/admin/Working/nckh-chatbot-neo4j/chatbot_api/src/result_openai_202104-0151.csv")

df_num = df.select_dtypes("number")
for col in df_num.columns:
    print(f"{col}: {df[col].mean()}")