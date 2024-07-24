# run this script after merging the single allele count files
# for file in allelecount_with_H12_chr*; do tail -n +2 "$file" >> allelecounts_H12_all.txt; done
# 
# use Agam gene space and gene IDs + names extracted from VectorBase-64_AgambiaePEST.gff
# grep -P "\tprotein_coding_gene\t" VectorBase-64_AgambiaePEST.gff | cut -f 1,4,5,9 | sed 's/AgamP4_//' | sed 's/;description.*//' | awk '{gsub("ID=","",$4); gsub(";Name=","\t", $4); print $1"\t"$2"\t"$3"\t"$4}' > genes_AgamPest.bed
#
# before starting, load a module that incorporates Panda:
# module load starfile/0.5.8-foss-2023a-pandas-2.1.4

import pandas as pd

# File paths
file_a="allelecounts_H12_all.txt"
file_b="genes_AgamPest.bed"
output_file="allelecounts_H12_geneID.txt"

# Read File A into a DataFrame
df_a = pd.read_csv(file_a, sep='\t')

# Read File B into a DataFrame
df_b = pd.read_csv(file_b, sep='\t', header=None, names=['chr', 'start', 'end', 'gene_ID', 'gene_name'])

# Initialize new columns for the merged information
df_a['gene_ID'] = 'NA'
df_a['gene_name'] = 'NA'

# Convert File B DataFrame to a list of dictionaries for faster lookups
ranges = df_b.to_dict('records')

# Function to find and add the info from File B to File A
def find_and_add_info(row):
    for range_info in ranges:
        if row['chr'] == range_info['chr'] and range_info['start'] <= row['position'] <= range_info['end']:
            row['gene_ID'] = range_info['gene_ID']
            row['gene_name'] = range_info['gene_name']
            break
    return row

# Apply the function to each row in File A DataFrame
df_a = df_a.apply(find_and_add_info, axis=1)

# Write the result to the output file
df_a.to_csv(output_file, sep='\t', index=False)