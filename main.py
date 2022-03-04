import os #import os module to run linux based commands
import csv #import csv module

SRR = 'SRR8185310' #insert SRR accession number here of organism of interest
os.mkdir('results') #iniatilize a directory called results to hold the important outputs generated by this wrapper

sra_path='$HOME/sratoolkit.2.11.2-ubuntu64/bin/' #Accessing SRA Toolkit after installing it within home directory
sra_out_path='$HOME/results/PrefetchFileDump/sra/' #Output for .fastq file of SRR accession

#1 Use Prefetch command and get Illumina Reads
def getData(SRR):
    Prefetch_command = sra_path+'prefetch ' + SRR #retreiving Illumina reads corresponding to SRR accession
    os.system(Prefetch_command) #system execution
    Fastq_dump_command = sra_path+'fastq-dump -I --split-files '+sra_out_path+SRR+ '.sra' #unpacking Illumina reads
    os.system(Fastq_dump_command) #system execution

getData(SRR) #function to retrieve and unpack reads

spades_path = '$HOME/SPAdes-3.15.4-Linux/bin/' #Accessing SPAdes after installing it within home directory
spades_out_path = '$HOME/results/SPAdes_Assembly/' #Output for SPAdes command stored within results folder

#2 Use SPAdes to assemble reads
def spades(SRR):
    spades_command = spades_path+'spades.py -k 55,77,99,127 -t 2 --only-assembler -s '+ SRR + '_1.fastq -o '+spades_out_path #Assembling reads
    os.system(spades_command) #system execution
    with open(os.path.expanduser('~/results/miniproject.log'), 'w') as f: #Generation of log file holding significant results
         f.write(spades_command + '\n') #write SPAdes command to log file
spades(SRR) #function to assemble reads


#3 and #4 are contig calculations
def read_fasta_file(infile): #code to read in .fasta files
    name, seq = None, []
    for line in infile:
        line = line.rstrip()
        if line.startswith(">"):
            if name: yield (name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name: yield (name, ''.join(seq))

def contigLengthCounter():
    infile = open(os.path.expanduser('~/results/SPAdes_Assembly/contigs.fasta')) #open SPAdes output
    outfile = open(os.path.expanduser('~/results/contigsLength1000.fasta'), 'w') #create a new file to hold output

    counter = 0 #counter

    for name, seq in read_fasta_file(infile): #read .fasta file
        if len(seq) > 1000: #if contig is greater than 1000 bp,
            counter += 1 #increase counter
            outfile.write(str(name)+'\n') #write the contig to the outfile in fasta format
            outfile.write(str(seq)+'\n')
    with open(os.path.expanduser('~/results/miniproject.log'), 'a') as f: #annotation of log file
         f.write("There are "+str(counter)+" contigs > 1000 in the assembly" + '\n') #indicate the number of large contigs
contigLengthCounter() #function to create file holding all contigs of length greater than 1000

def assemblyLength():
    infile = open(os.path.expanduser('~/results/contigsLength1000.fasta'), 'r') #open new contig file
    base_pairs = 0 #counter

    for name, seq in read_fasta_file(infile): #read .fasta file
        base_pairs += len(seq) #increase counter by sequence length
    with open(os.path.expanduser('~/results/miniproject.log'), 'a') as f: #annotation of log file
         f.write("There are "+str(base_pairs)+" bp in the assembly" + '\n') #indicate length of assembly
assemblyLength() #function to generate assembly length

GeneMark2_path = '$HOME/gms2_linux_64' #Accessing GeneMarkS-2 after installing it within home directory
GeneMark2_outfile = '$HOME/results/GeneMark2_output.fasta' #output from GMS2 stored within

#5 is using GeneMark2 to find predicted protein sequences
def GeneMark2Prediction():
    GeneMark2_command = 'perl '+GeneMark2_path+'/gms2.pl --seq contigsLength1000.fasta --genome-type bacteria --faa '+GeneMark2_outfile #Finding predicted Protein Sequences
    os.system(GeneMark2_command) #system execution
GeneMark2Prediction() #function to find predicted protein sequences

#6 use BLAST+
def makeBlastDB(infile):
    makeBlastDB_command = 'makeblastdb -in '+infile+' -out Ecoli -title Ecoli -dbtype prot' #making a database to run BLAST+
    os.system(makeBlastDB_command) #system execution
makeBlastDB(os.path.expanduser('~/Ecoli.fasta')) #function for local database creation

def blast(infile, outfile):
    blast_command = 'blastp -query '+infile+' -db Ecoli -out '+outfile+' -outfmt "10 qseqid sseqid pident qcovs" -max_target_seqs 1 -max_hsps 1' #run BLAST+ on our predicted protein sequences
    os.system(blast_command) #system execution
blast(os.path.expanduser('~/results/GeneMark2_output.fasta'), os.path.expanduser('~/results/predicted_functionality.csv')) #function to run BLAST+

#7 Make note of any discrepancies
def discrepancy(infile):
    handle = open(infile) #open csv file
    reader = csv.reader(handle) #read in csv file
    CDS_counter = len(list(reader)) #length of csv file

    with open(os.path.expanduser('~/results/miniproject.log'), 'a') as f: #annotating log file
         f.write("GeneMarkS found "+str(CDS_counter-4140)+" additional CDS than the RefSeq" + '\n') #Indicate any discrepancies between RefSeq and our sequence
discrepancy(os.path.expanduser('~/results/predicted_functionality.csv')) #function to note any discrepancies