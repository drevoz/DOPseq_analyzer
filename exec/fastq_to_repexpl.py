#!/usr/bin/env python

import sys
import argparse

def parse_command_line_arguments():

    parser = argparse.ArgumentParser(description=    
                    """
                    Converts paired reads from Illumina 1.8+ fastq processed with cutadapt to interleaved fasta. 
                    Suitable as input for RepeatExplorer with 'All sequence reads are paired' option.
                    """
                    )
    #parser.add_argument("fastq_F_file", help="fastq file with forward reads (.fastq)")
    #parser.add_argument("fastq_R_file", help="fastq file with reverse reads (.fastq)")
    parser.add_argument("cutadapt_prefix", help="prefix of fastq files processed with cutadapt. Format <prefix>.<F|R.ca.fastq>")    
    parser.add_argument("-r","--rename", action="store_true",help="rename reads to numeric")
    return parser.parse_args()
   
def fastq_to_re_fasta(args):

    # From two fastq files generate interleaved fasta file with added '/1' for forward and '/2' for reverse read
    
    f_fastq = args.cutadapt_prefix + '.F.ca.fastq'
    r_fastq = args.cutadapt_prefix + '.R.ca.fastq'
    o_fasta = args.cutadapt_prefix + '.re.fasta'
    rename = args.rename
    
    i=0 # read number
    k=0 # line number
    fname = ''
    rname = ''
    with open(f_fastq, 'rU') as f_file, open(r_fastq, 'rU') as r_file, open(o_fasta, 'w') as out:
        for fline in f_file:
            rline = r_file.next()
            if fname != '' and rname != '': # read sequence - next line after name
                if len(fline) > 1 and len(rline) > 1: # exclude pairs with emtpy reads
                    out.write(fname+fline+rname+rline)
                fname = ''
                rname = ''
            elif fline.startswith('@') and k%4 == 0: # get read name
                i+=1
                if rename:
                    fname='>%d/1\n'%i
                    rname='>%d/2\n'%i
                else:
                    fname='>'+fline[1:-1]+'/1\n'
                    rname='>'+rline[1:-1]+'/2\n'
            k+=1

if __name__ == '__main__':
    fastq_to_re_fasta(parse_command_line_arguments())

    
