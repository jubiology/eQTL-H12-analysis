#!/bin/bash

#########################
# merge allelecounts with H12 stats for chr 3L

# read files
allelecount_file="RESULTS_allelecount_Chr3L.tsv"
h12_coluzzii_file="H12stats_95qoutliers_coluzzii_Chr3L.tsv"
h12_gambiae_file="H12stats_95qoutliers_gambiae_Chr3L.tsv"
output_file="allelecount_with_H12_chr3L.txt"

# 
temp_file=$(mktemp)

# create header for output file
awk 'NR==1 {print $0, "H12_coluzzii", "H12_gambiae"}' $allelecount_file > $temp_file

# reading allelecount file and find H12 values
awk 'NR > 1' $allelecount_file | while read -r line; do
    chr=$(echo $line | awk '{print $1}')
    pos=$(echo $line | awk '{print $2}')

    # Find H12 values for coluzzii
    h12_value_coluzzii=$(awk -v chr="$chr" -v pos="$pos" '
        NR > 1 && $1 == chr && $2 <= pos && $3 >= pos {print $5}' $h12_coluzzii_file)

    # when no H12 value: "NA"
    if [ -z "$h12_value_coluzzii" ]; then
        h12_value_coluzzii="NA"
    fi

    # Find H12 value for gambiae
    h12_value_gambiae=$(awk -v chr="$chr" -v pos="$pos" '
        NR > 1 && $1 == chr && $2 <= pos && $3 >= pos {print $5}' $h12_gambiae_file)

    # when no H12 value: "NA"
    if [ -z "$h12_value_gambiae" ]; then
        h12_value_gambiae="NA"
    fi

    # Add line with H12-Werten to temp file
    echo "$line $h12_value_coluzzii $h12_value_gambiae" >> $temp_file
done

# Move temp file to output file
mv $temp_file $output_file

# clean up
trap "rm -f $temp_file" EXIT
