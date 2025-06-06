import pandas as pd

# Đọc file CSV
model_name = "all-mpnet-base-v2"
print(model_name)
file_path = '/Users/admin/Working/January/nckh-chatbot-neo4j/chatbot_api/src/results/phobert/response_fit241222-1727_4_result2.csv' # Đổi tên thành đường dẫn file CSV của bạn'
data = pd.read_csv(file_path)

# Lọc các cột số
numerical_columns = data.select_dtypes(include='number')

# Tính trung bình cho từng cột số
average_values = numerical_columns.mean()
null_counts = numerical_columns.isnull().sum()

zero_counts = (numerical_columns == 0).sum()


# In kết quả
print("Giá trị trung bình của các cột số:")
print(average_values)
print(null_counts)
print(zero_counts)