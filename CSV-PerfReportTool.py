import os
import sys
import ctypes
import glob
import tkinter as tk
from tkinter import filedialog
import winreg as reg

# Initialize PerfReportTool filepath variable
perf_report_tool_filepath = 'none'


# Check if the program is running with admin privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# Add context menu command to open the script with specified arguments
def add_context_menu_command():
    # Create keys for the context menu commands
    key_paths = [
        r"Directory\\Background\\shell\\CSVtoTables",
        r"Directory\\shell\\CSVtoTables",
        r"SystemFileAssociations\\.csv\\Shell\\CSVtoTables"
    ]

    for key_path in key_paths:
        key = reg.CreateKeyEx(reg.HKEY_CLASSES_ROOT, key_path)
        reg.SetValue(key, '', reg.REG_SZ, 'Create tables from CSV')

        python_exe = '"' + sys.executable + '"'
        script_path = '"' + os.path.abspath(__file__) + '"'
        args = ' "%V"' if not key_path.endswith('.csv') else ' "%1"'
        command = f'{python_exe} {script_path}{args} "{perf_report_tool_filepath}"'

        command_key = reg.CreateKeyEx(key, r"command")
        reg.SetValue(command_key, '', reg.REG_SZ, command)


# Choose the Unreal Engine folder containing the PerfReportTool
def choose_folder():
    global perf_report_tool_filepath
    perf_report_tool_filepath = filedialog.askdirectory()
    perf_report_tool_filepath = os.path.join(perf_report_tool_filepath, 'Engine', 'Binaries', 'DotNET', 'CsvTools', 'PerfreportTool.exe')
    perf_report_tool_filepath = perf_report_tool_filepath.replace('/', '\\')
    current_perfreport_fp_txt.config(text='PerfReportTools Filepath:\n' + perf_report_tool_filepath)


# Run the PerfReportTool with the specified CSV file and output directory
def run_csv_generator(csv_filepath, output):
    command = f'"{perf_report_tool_filepath}" -csv "{csv_filepath}" -o "{output}"'
    stream = os.popen(command)
    output = stream.read()
    stream.close()
    return output


# Run the PerfReportTool with the specified LLM CSV file and output directory
def run_llm_csv_generator(csv_filepath, output):
    command = f'"{perf_report_tool_filepath}" -csv "{csv_filepath}" -o "{output}" -reporttype LLM -topng. -graphxml LLMReportGraphs.xml -reportxml LLMReportTypes.xml -nostripevents'
    stream = os.popen(command)
    output = stream.read()
    stream.close()
    return output


# Main logic of the program
if len(sys.argv) > 1:
    csv_files_list = glob.glob(os.path.join(sys.argv[1], '*.csv'))
    perf_report_tool_filepath = sys.argv[2]

    if not csv_files_list and sys.argv[1].endswith('.csv'):
        output_dir = os.path.dirname(sys.argv[1])
        if 'LLM' in sys.argv[1] or 'llm' in sys.argv[1]:
            print(run_llm_csv_generator(sys.argv[1], output_dir))
        else:
            print(run_csv_generator(sys.argv[1], output_dir))
    elif csv_files_list:
        for file in csv_files_list:
            if 'LLM' in file or 'llm' in file:
                print(run_llm_csv_generator(file, sys.argv[1]))
            else:
                print(run_csv_generator(file, sys.argv[1]))
    else:
        print("There's no csv")

    input("Press enter to exit...")

else:
    if is_admin():
        # Hide console window
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        
        # Set up the GUI window
        root = tk.Tk()
        root.attributes("-alpha", 0.0)
        root.eval("tk::PlaceWindow . center")
        root.attributes("-alpha", 1)
        root.title("CSV-PerfReportTool")
        root.resizable(False, False)

        # Set up the GUI elements
        current_perfreport_fp_txt = tk.Label(root, text="PerfReportTools Filepath:\n" + perf_report_tool_filepath, font="Arial 12")
        choose_folder_btn = tk.Button(root, text="Choose UE folder", font="Arial 10", command=choose_folder)
        add_command_btn = tk.Button(root, text="Add command to context menu", font="Arial 10", command=add_context_menu_command)

        current_perfreport_fp_txt.pack(padx=15, pady=(15, 5))
        choose_folder_btn.pack(padx=15, pady=5)
        add_command_btn.pack(padx=15, pady=(5, 15))

        # Run the GUI loop
        root.mainloop()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
