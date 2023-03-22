import os, sys, ctypes, glob
import winreg as reg
import tkinter as tk
from tkinter import filedialog
    
# Init perfreport filepath var
perf_report_tool_filepath = 'none'

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Add to context menu command that opens this script with specified args
def add_context_menu_command():
    # Create key for the context menu commands
    dir_back_key_path = r"Directory\\Background\\shell\\CSVtoTables"
    dir_back_key = reg.CreateKeyEx(reg.HKEY_CLASSES_ROOT, dir_back_key_path)
    reg.SetValue(dir_back_key, '', reg.REG_SZ, 'Create tables from CSV')
    
    dir_key_path = r"Directory\\shell\\CSVtoTables"
    dir_key = reg.CreateKeyEx(reg.HKEY_CLASSES_ROOT, dir_key_path)
    reg.SetValue(dir_key, '', reg.REG_SZ, 'Create tables from CSV')
    
    csv_key_path = r"SystemFileAssociations\\.csv\\Shell\\CSVtoTables"
    csv_key = reg.CreateKeyEx(reg.HKEY_CLASSES_ROOT, csv_key_path)
    reg.SetValue(csv_key, '', reg.REG_SZ, 'Create tables from CSV')
    
    # Create a subkeys for context menu commands
    python_exe = '"' + sys.executable + '"'
    
    dir_back_command_key = reg.CreateKeyEx(dir_back_key, r"command")
    reg.SetValue(dir_back_command_key, '', reg.REG_SZ,
                 python_exe + ' "' + os.path.abspath(__file__) + '" "%V"' + ' "' + perf_report_tool_filepath + '"')

    dir_command_key = reg.CreateKeyEx(dir_key, r"command")
    reg.SetValue(dir_command_key, '', reg.REG_SZ,
                 python_exe + ' "' + os.path.abspath(__file__) + '" "%V"' + ' "' + perf_report_tool_filepath + '"')
    
    csv_command_key = reg.CreateKeyEx(csv_key, r"command")
    reg.SetValue(csv_command_key, '', reg.REG_SZ,
                 python_exe + ' "' + os.path.abspath(__file__) + '" "%1"' + ' "' + perf_report_tool_filepath + '"')

# Remove last directory or file from filpath
def remove_last_dir_from(filepath):
    dirs_and_file = filepath.split("\\")
    dirs_and_file.pop()
    new_filepath = "\\".join(dirs_and_file)
    return new_filepath

# Function to choose UE folder
def choose_folder():
    global perf_report_tool_filepath
    perf_report_tool_filepath = filedialog.askdirectory() + '\\Engine\\Binaries\\DotNET\\CsvTools\\PerfreportTool.exe'
    perf_report_tool_filepath = perf_report_tool_filepath.replace('/', '\\')
    curent_perfreport_fp_txt.configure(text='Current PerfReportTools Filepath:\n' + perf_report_tool_filepath)

def run_csv_generator(csv_filepath, output):
    stream = os.popen('"' + perf_report_tool_filepath + '"'
                      + ' -csv "' + csv_filepath + '"'
                      + ' -o "' + output + '"')
    output = stream.read()
    stream.close()
    return output
    
def run_llm_csv_generator(csv_filepath, output):
    stream = os.popen('"' + perf_report_tool_filepath + '"'
                      + ' -csv "' + csv_filepath + '"'
                      + ' -o "' + output + '"'
                      + ' -reporttype LLM -topng. -graphxml LLMReportGraphs.xml -reportxml LLMReportTypes.xml -nostripevents')
    output = stream.read()
    stream.close()
    return output


# When program was started with command line arguments
if len(sys.argv) > 1:
    print(sys.argv)
    csv_files_list = glob.glob(sys.argv[1] + '\*.csv')
    perf_report_tool_filepath = sys.argv[2]
    
    # File
    if not csv_files_list and sys.argv[1].endswith('.csv'):
        if sys.argv[1].find('LLM') != -1 or sys.argv[1].find('llm') != -1:
            print(run_llm_csv_generator(sys.argv[1], remove_last_dir_from(sys.argv[1])))
        else:
            print(run_csv_generator(sys.argv[1], remove_last_dir_from(sys.argv[1])))        
    # Folder
    elif csv_files_list:
        for file in csv_files_list:
            if file.find('LLM') != -1 or file.find('llm') != -1:
                print(run_llm_csv_generator(file, sys.argv[1]))
            else:
                print(run_csv_generator(file, sys.argv[1]))
    else:
        print('There\'s no csv')
        
    input('Press enter to exit...')
   
# When programm was started without command line args
else:
    if is_admin():
        # Set up the GUI window
        root = tk.Tk()
        root.attributes('-alpha', 0.0)
        root.eval('tk::PlaceWindow . center')        
        root.attributes('-alpha', 1)
        root.title("CSV-PerfReportTool")
        root.resizable(False, False)
        
        # Set up the GUI elements
        curent_perfreport_fp_txt = tk.Label(root, text='PerfReportTools Filepath:\n' + perf_report_tool_filepath, font='Arial 12')
        #curent_perfreport_fp_txt.grid(row=0, column=0, sticky="nsew", padx=5, pady=2)
        choose_folder_btn = tk.Button(root, text="Choose UE folder", font='Arial 10', command=choose_folder)
        #choose_folder_btn.grid(row=1, column=0, sticky="nsew", padx=50, pady=25)
        add_commmand_btn = tk.Button(root, text="Add command to context menu", font='Arial 10', command=add_context_menu_command)
        #add_commmand_btn.grid(row=2, column=0, sticky="nsew", padx=50, pady=5)

        curent_perfreport_fp_txt.pack(padx=15, pady=(15, 5))
        choose_folder_btn.pack(padx=15, pady=5,)
        add_commmand_btn.pack(padx=15, pady=(5, 15))
        
        # Run the GUI loop
        root.mainloop()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
