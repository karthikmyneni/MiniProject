# MiniProject
MiniProject for COMP383


Software Requirements:
  Python3,
  Ubuntu/Linux,
  SRA Toolkit,
  SPAdes,
  GeneMarkS-2
  
Installation Instructions:
  1. SRA Toolkit installation, setup, and configuration can be found by following (https://github.com/ncbi/sra-tools/wiki/01.-Downloading-SRA-Toolkit). Install the toolkit into your Home/working directory. The outputs will be located within a subfolder (PrefetchFileDump) located inside the results folder. 
  2. SPAdes installation and setup instructions can be found by following (https://cab.spbu.ru/software/spades/). Install the software into your Home/working directory. The outputs will be located within a subfolder (SPAdes_Assembly) located inside the results folder.
  3. GeneMarkS-2 installation and setup instructions can be found by following (http://exon.gatech.edu/GeneMark/license_download.cgi). Install the software into your Home/working directory. The output willl be located within the results folder.
  
How to Run Wrapper:
  1. Install SRA Toolkit SPAdes, and GeneMarkS-2 into Home/working directory
  2. Clone the Repository
  3. Move into Home/working directory
  4. Update file names and locations as desired
  5. Run wrapper with "python3 main.py"

Files: 
  1. main.py: Python script with all wrappers included and ready to run

Output:
  1.  miniproject.log: Log file detailing significant results/findings
  2.  results folder: Folder to hold outputs from main.py
