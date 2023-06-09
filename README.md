# Auto CSV PerfReportTool
![image](https://user-images.githubusercontent.com/88453288/227159524-c72f2746-72c3-4179-b46d-4eb114621cf7.png)

## What it do
This program is a Python script that utilizes the PerfReportTool utility from Unreal Engine to process CSV files and generate performance reports. The script provides a GUI for users to choose the folder containing the PerfReportTool.exe, and it also adds a context menu command to allow users to generate performance reports directly from the Windows context menu (folders, backgorund of folders and files with .csv extension).

## How to use it
1. Run script. It will ask administration rights to be able to edit Windows registry.
2. Click "Choose UE folder" button and choose any folder wich contains Unreal Engine. It must contains "Engine" folder.

![image](https://user-images.githubusercontent.com/88453288/227186023-c618df73-5b14-4971-8678-08e73dfa0a43.png)

3. After that PerfReportTools Filepath should change to what you choose. Click "Add command to context menu" and close program.

![image](https://user-images.githubusercontent.com/88453288/227163482-c73be269-0e94-4e72-ae5a-b0cbc90d106e.png)

4. On any folder that contains csv file or on csv file click right button and click "Create tables from CSV". If everything setted up right in same folder will be generated html file.

## How it works
When script started without command line arguments (from icon) window will shows up. Here you can choose Unreal Engine's folder and add command to Windows context menu. When you click button "Add command to context menu" script adds commands to Windows registry. So when you click in a context menu on "Create tables from CSV" it will run this script with such arguments as clicked **File/Folder filepath** and **PerfReportTools filepath**. Then script will run PerfReportTools wich generates tables. 

![image](https://user-images.githubusercontent.com/88453288/227180237-0fd86771-7d0b-4b57-a0a3-4833f544305d.png)