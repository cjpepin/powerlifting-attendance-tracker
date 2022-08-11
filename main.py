from urllib import request
import pandas as pd
import numpy as np

from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

class Attendance_Checker:


    def __init__(self):
        total_id = "1qDcaEYMJ0SRtzaFP59FpLEI_X5S6luGrpnr8ll3m7Ig"
        total_name = "Total"

        roster_id = "1J5zTgCu80vGjIlPr1C-rifmVCBNHiYg_CQOmJxTJa7o"
        roster_name = "Roster"

        total_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(total_id, total_name)
        roster_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(roster_id, roster_name)

        total = pd.read_csv(total_url)
        roster = pd.read_csv(roster_url)

        self.total = total
        self.roster = roster
        self.dates = []
        self.df = self.format_df(total, roster)
        self.stopDate = ""

    def format_df(self, df, roster):
        dfsToMerge = []
    #     Go through each column
        for col in df.columns:
    #          If the column is a name column
            if("Name:" in col):
    #         Get the name column and following two columns
                ind = df.columns.get_loc(col)
                col1 = df.columns[ind]
                col2 = df.columns[ind+1]
                col3 = df.columns[ind+2]
    #             Get the desired sub-dataframe
                newDf = df.copy()
                newDf = newDf[[col1, col2, col3]]
                newDf = newDf[newDf[col1].notna()]
    #             Compare the name column to each name in the roster
                for i, name in roster.iterrows():
    #               If the column contains the name, continue
                    if (newDf[col1].str.contains(name[0]).any()):
                        continue
    #             Otherwise create new row
                    else:
                        newRow = [name[0], "No", "No"]
                        newDf.loc[len(newDf.index)] = newRow

                newDf = newDf.rename(columns={col1:"Name:"})
                newDf = newDf.sort_values(by="Name:")
                newDf = newDf.reset_index()
                newDf = newDf.drop(["index"], axis=1)
                if ind!= 0:
                    newDf = newDf.drop(["Name:"], axis=1)


                dfsToMerge.append(newDf)
        newestDf = self.merge_dfs(dfsToMerge).fillna("No")
        return newestDf

    def merge_dfs(self, dfs):
        return pd.concat(dfs, axis=1)

    def check_requirements(self):
        df = self.select_df_cols(self.df)
        total = (len(df.columns) - 1) / 2
        required = np.round((total)/3, 2)
        attendance_arr = []
        
        for i in range(len(df)):
            yes_count = 0
            for j, col in enumerate(df.columns):
                # if stopDate in df.columns[j+2]:
                #     return
                if("Name" in col):
                    continue
                if("Fill Out Form?" in col):
        #             idk yet
                    continue
                if("Are you coming to Practice?" in col and df.at[i, col] == "Yes"):
                    yes_count += 1
            if yes_count < required:
                attendance_arr.append([df.at[i, 'Name:'], yes_count])
        return attendance_arr

    def check_this_form_filled(self):
        df = self.select_df_cols(self.df)
        not_filled_arr = []
        if self.stopDate == "":
            col = df.columns[len(df.columns) - 2]
        else:
            col = df.columns[self.dates.index(self.stopDate) * 2 + 2]
        for i in range(len(df)):
            if(df.at[i, col]) == "No":
                not_filled_arr.append(df.at[i, 'Name:'])
        return not_filled_arr

    def strikes(self):
        df = self.select_df_cols(self.df)
        max_strikes = 5
        strikesArr = []
        for i, row in df.iterrows():
            strikes = 0
            for j, col in enumerate(df.columns):
                if "Filled" in df.columns[j] and "No" in df.at[i, col]:
                    strikes += 1
            
            strikesArr.append([df.at[i, 'Name:'], strikes])
        strikesArr.sort(key=lambda x: x[1], reverse=True)
        return strikesArr
        
#     def save_new_df(self):
#         self.df.to_csv('/Users/connorpepin/JupyterNotebooks/Powerlifting/total.csv', index=False)

    def display_table(self):
        return self.df.to_html()
        
    def select_df_cols(self, df):
        stopDateCol = df.columns.get_loc([col for col in df.columns if self.stopDate in col][0])
        return df.iloc[:, :stopDateCol+2]

    def set_stop_date(self, date):
        self.stopDate = date

    def get_dates(self):
        df = self.df
        if self.dates != []:
            return
        for col in df.columns:
            curDate = col[-10:]

            if curDate in self.dates:
                return
            if "Name:" not in curDate and "Coming" not in curDate and "Form" not in curDate:
                self.dates.append(curDate.strip())

        return self.dates
        
    # def run_suite(self, stopDate):
    #     self.df = self.format_df(self.total, self.roster)
    #     if(stopDate == ""):
    #         self.display_table()
    #         self.get_dates()
    #     self.check_requirements(stopDate)
    #     self.check_this_form_filled(stopDate)
    #     self.strikes(stopDate)

total_id = "1qDcaEYMJ0SRtzaFP59FpLEI_X5S6luGrpnr8ll3m7Ig"
total_name = "Total"

roster_id = "1J5zTgCu80vGjIlPr1C-rifmVCBNHiYg_CQOmJxTJa7o"
roster_name = "Roster"

total_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(total_id, total_name)
roster_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(roster_id, roster_name)

total = pd.read_csv(total_url)
roster = pd.read_csv(roster_url)
ac = Attendance_Checker()

@app.route("/")
def home():

    dates = ac.get_dates()
    stopDate = dates[len(dates)-1]
    ac.stopDate = stopDate
    data = {"df": ac.display_table(),
            "goingToPractice": ac.check_requirements(), 
            "filledOutForm": ac.check_this_form_filled(),
            "strikes": ac.strikes(),
            "dates": dates }
    return render_template("index.html", data=data)

@app.route("/changeDate", methods=['POST'])
def changeDate():
    output = request.get_json()
    ac.stopDate = output

    data = {"goingToPractice": ac.check_requirements(), 
            "filledOutForm": ac.check_this_form_filled(),
            "strikes": ac.strikes(),
            }
    return data


if __name__ == "__main__":
    app.run()