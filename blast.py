import subprocess
from Bio import SeqIO
from Bio.Blast import NCBIXML
import os

human = "human.fa"
mouse = "mouse_blast"
output = "results.txt"

# Open the output file
with open(output, "w") as out_file:
    # Parse human sequences
    for human_record in SeqIO.parse(human, "fasta"):


        query_file = "query.fasta"
        with open(query_file, "w") as temp_query_file:
            SeqIO.write(human_record, temp_query_file, "fasta")


        try:
           
            blast_command = [
                "blastp",
                "-query", query_file,
                "-db", mouse,
                "-outfmt", "5",
                "-max_target_seqs", "13",
                "-out", "blast_results.xml"  
            ]
            subprocess.run(blast_command, check=True)

            # Parse
            with open("blast_results.xml") as result_handle:
                blast_record = NCBIXML.read(result_handle)



            # Proces the results
            if blast_record.alignments:
                
                top_hit = blast_record.alignments[0]
                for hsp in top_hit.hsps:
                    out_file.write(f"Human ID: {human_record.id}\n")
                    out_file.write(f"Mouse ID: {top_hit.hit_id}\n")
                    out_file.write(f"Alignment:\n{hsp.sbjct}\n")
                    out_file.write(f"E-value: {hsp.expect}\n")
                    out_file.write(f"Bitscore: {hsp.score}\n")
                    out_file.write("="*50 + "\n")
                    breakce
            else:
                out_file.write(f"Human ID: {human_record.id}\n")
                out_file.write("No hits found.\n")
                out_file.write("="*100 + "\n")  # Separator
        except subprocess.CalledProcessError as e:
            out_file.write(f"BLAST error for {human_record.id}: {e}\n")
        except Exception as e:
            out_file.write(f"Error processing {human_record.id}: {str(e)}\n")
        finally:
            # Clean up 
            
            try:
                os.remove(query_file)
            except OSError:
                pass  

print(f" check here: {output}. the explanation is in the markdown block of the blast.ipynb notebook")