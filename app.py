from jinja2 import Undefined
import eel
import pandas as pd
import numpy as np
from datetime import date

eel.init("src")

class Attendance_Checker:
    def __init__(self, total, roster):
        self.total = total
        self.roster = roster
        self.dates = []
        self.df = self.format_df(total, roster)

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

    def check_requirements(self, stopDate):
        df = self.select_df_cols(self.df, stopDate)
        total = (len(df.columns) - 1) / 2
        required = np.round((total)/3, 2)
        eel.goingToPractice(f"These People Have Not Been To {required} Practice(s)")
        eel.goingToPractice("")
        
        eel.goingToPractice("Practices attended by...")
        eel.goingToPractice("")
        
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
                eel.goingToPractice(f"{df.at[i, 'Name:']}: {yes_count}")
        eel.goingToPractice("")

    def check_this_form_filled(self, stopDate):
        df = self.select_df_cols(self.df, stopDate)
        if stopDate == "":
            col = df.columns[len(df.columns) - 2]
        else:
            col = df.columns[self.dates.index(stopDate) * 2 + 2]
        eel.filledOutForm("These People Did Not Fill Out The Form")
        eel.filledOutForm("")
        for i in range(len(df)):
            if(df.at[i, col]) == "No":
                eel.filledOutForm(f"{df.at[i, 'Name:']}")
        eel.filledOutForm("")

    def strikes(self, stopDate):
        df = self.select_df_cols(self.df, stopDate)
        max_strikes = 5
        strikesArr = []
        eel.strikes(f"Strikes")
        eel.strikes("")
        for i, row in df.iterrows():
            strikes = 0
            for j, col in enumerate(df.columns):
                if "Filled" in df.columns[j] and "No" in df.at[i, col]:
                    strikes += 1
            
            strikesArr.append([df.at[i, 'Name:'], strikes])
        strikesArr.sort(key=lambda x: x[1], reverse=True)
        eel.strikes(strikesArr)
        
#     def save_new_df(self):
#         self.df.to_csv('/Users/connorpepin/JupyterNotebooks/Powerlifting/total.csv', index=False)

    def display_table(self):
        eel.displayTable(f"{self.df.to_html()}")
        
    def select_df_cols(self, df, stopDate):
        stopDateCol = df.columns.get_loc([col for col in df.columns if stopDate in col][0])
        return df.iloc[:, :stopDateCol+2]

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

        eel.setDateButtons(self.dates)
        
    def run_suite(self, stopDate):
        self.df = self.format_df(self.total, self.roster)
        if(stopDate == ""):
            self.display_table()
            self.get_dates()
        self.check_requirements(stopDate)
        self.check_this_form_filled(stopDate)
        self.strikes(stopDate)

total_id = "1qDcaEYMJ0SRtzaFP59FpLEI_X5S6luGrpnr8ll3m7Ig"
total_name = "Total"

roster_id = "1J5zTgCu80vGjIlPr1C-rifmVCBNHiYg_CQOmJxTJa7o"
roster_name = "Roster"

total_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(total_id, total_name)
roster_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(roster_id, roster_name)

total = pd.read_csv(total_url)
roster = pd.read_csv(roster_url)
ac = Attendance_Checker(total, roster)

@eel.expose
def run_suite():
    ac.run_suite("")

@eel.expose
def show_up_to(date):
    ac.run_suite(date)
    

eel.start("index.html")

# this_practice = Undefined
# ac = Undefined

# def select_file():
#     filename = filedialog.askopenfilename(initialdir="/Users/connorpepin/JupyterNotebooks/Powerlifting/", title="Select File",
#                                             # filetypes=(("executables","*.csv", "all files", "*.*"))
#                                         )

#     success = tk.Label(frame, text=f"{filename} uploaded successfully", bg="white")
#     success.pack()

#     global this_practice
#     this_practice = pd.read_csv(f"{filename}")
#     global ac
#     ac = Attendance_Checker(total, this_practice)


# root = tk.Tk()

# canvas = tk.Canvas(root, height=700, width=500,bg="#ffffff")
# canvas.pack()

# frame = tk.Frame(root, bg="grey")
# frame.place(relwidth=0.7, relheight=0.7, relx=0.15, rely=0.15)

# spacer = tk.Label(frame, text="", bg="white")

# def run_functions():
#     if(ac != Undefined):
#         ac.run_suite()
#     else:
#         error = tk.Label(frame, text="It looks like you didn't pick a file to upload")
#         error.pack()

# def simple_test():
#     success = tk.Label(frame, text=f" uploaded successfully", bg="white")
#     success.pack()

# openFile = tk.Button(root, text="Open Attendance Sheet", padx=10, pady=5, fg="grey", bg="black", command=select_file)
# openFile.pack()

# runChecks = tk.Button(root, text="Run Checks", padx=10, pady=5, fg="grey", bg="black", command=run_functions)
# runChecks.pack()


# root.mainloop()
