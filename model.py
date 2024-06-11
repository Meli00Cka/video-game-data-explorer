from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split as split
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor as dt
import pandas as pd

class model():
    def __init__(self,data):
        self.data = data
        self.is_data_ready = False
        
    @staticmethod
    def encode_column(data, column):
        col_num = {}
        for i, c in enumerate(data[column].unique()):
            col_num[c] = i

        return data[column].map(col_num), col_num


    def preprocess_data(self):
        data = self.data
        
        data.dropna(how="any", inplace=True)
        data = data.astype({"Year": 'int'})
        data = data.reset_index(drop=True)

        # replace rare platforms with "Other"
        plat_count_val = data["Platform"].value_counts()
        plat_replace = plat_count_val[data["Platform"].value_counts() < 250].index
        data.loc[(data["Platform"].isin(plat_replace)) & (data["Rank"] > data["Rank"].median()), "Platform"] = "Other"

        # replace rare publishers with "Other"
        q1 = data["Publisher"].value_counts(normalize=True).quantile(0.75)
        pub_outliers = data["Publisher"].value_counts(normalize=True)[data["Publisher"].value_counts(normalize=True) < q1].index
        data.loc[data["Publisher"].isin(pub_outliers), "Publisher"] = "Other"

        # encode the "Genre" column
        data["Genre"], self.genre_names = self.encode_column(data, "Genre")

        # OneHot encode "Platform" and "Publisher" columns
        encoder = OneHotEncoder(sparse_output=False)
        selected_features = ['Platform', 'Publisher']

        encoder.fit(data[selected_features])
        encoded_data = encoder.transform(data[selected_features])
        encoded_cols = encoder.get_feature_names_out(selected_features)

        encoded_data = pd.DataFrame(encoded_data, columns=encoded_cols, index=data.index)
        data = pd.concat([data.drop(selected_features, axis=1), encoded_data], axis=1)

        # drop unnecessary columns
        data.drop(columns=["Name","NA_Sales","EU_Sales","JP_Sales","Other_Sales","Rank"], axis=1, inplace=True)
        
        
        self.data = data
        
        # split data into train and test sets
        y = data["Global_Sales"]
        X = data.drop("Global_Sales", axis=1)
        self.X_train, self.X_test, self.y_train, self.y_test = split(X, y, test_size=0.2, random_state=42)
        
        # update status
        self.is_data_ready = True

            
    
    def train_dt(self):
        self.model = dt(random_state=42)
        self.model.fit(self.X_train, self.y_train)
        
    
    def evaluate_model(self):
        self.y_pred = self.model.predict(self.X_test)
        self.mse_error = mean_squared_error(self.y_test, self.y_pred)
        return f"Mean Squared Error: {self.mse_error}"

    
    def __preprocess_new_data(self,publisher,platform,genre,year):
        if self.is_data_ready:
            X_dict = {col:0.0 for col in map(str, self.data.columns.drop("Global_Sales"))}
            X_dict[platform], X_dict[publisher], X_dict["Genre"], X_dict["Year"] = 1.0 , 1.0, genre, year
            self.X_user = pd.DataFrame([X_dict])
        else:
            self.preprocess_data()

    
    def predict(self,publisher: str, platform: str, genre: int, year: int):
        self.__preprocess_new_data(publisher,platform,genre,year)
        p_value = self.model.predict(self.X_user)
        return p_value
    
    
    def do_all(self, algorithm: str):
        self.preprocess_data()
        if algorithm=="dt":
            self.train_dt()
        self.evaluate_model()