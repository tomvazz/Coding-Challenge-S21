# Load Genbank file to parse
from Bio import SeqIO
# Diagram imports
from Bio.SeqFeature import SeqFeature, FeatureLocation
from reportlab.lib import colors
from reportlab.lib.units import cm
from Bio.Graphics import GenomeDiagram


# parses the Genome genbank file and retrieves its contents
virus_record = SeqIO.read("Genome.gb", "gb")
# full DNA sequence is retrieved and printed
virus_dna = virus_record.seq
print(virus_dna)

# empty diagram is created
diagram = GenomeDiagram.Diagram(
   "Tomato curly stunt virus")
# empty track is placed in diagram
bar_size = 1
track = diagram.new_track(bar_size, name="Annotated Features")
# empty feature set is implemented and placed in the track
feature_set = track.new_set()


# every other feature bar is given the same color
# labels display the gene name of each feature
def bar_display(record):
    # each feature is retrieved from the genbank file records that were retrieved
    for feature in record.features:
        # allows for the genomic placement in and out of the circle
        if feature.type != "gene":
            continue

        if len(feature_set) % 2 == 0:
            color = colors.fidred
        else:
            color = colors.indianred
        feature_set.add_feature(
            feature,
            color=color,
            label=True,
            label_size=30,
            label_position="middle",
            label_color=colors.darksalmon,
            # feature bars are displayed as arrows
            sigil="ARROW",
            arrowshaft_height=0.7,
            arrowhead_length=0.5
        )


# recognition sequences text file containing restriction enzymes are retrieved
def sequence_retrieval():
    # contents of file will be stored in this list
    enzyme_sequences = []
    with open("recognition_sequences.txt", "r") as sequences:
        color_count = 0
        for line in sequences:
            # the enzyme and its code are separated and stored in their respective variables
            line = line.split(" - ")
            code = line[0].upper()
            enzyme = line[1]
            if "\n" in enzyme:
                enzyme = enzyme.replace("\n", "")

            # different color is assigned to each of the seven selected enzymes
            if color_count == 0: enzyme_sequences.append((code, enzyme, colors.green))
            elif color_count == 1: enzyme_sequences.append((code, enzyme, colors.purple))
            elif color_count == 2: enzyme_sequences.append((code, enzyme, colors.hotpink))
            elif color_count == 3: enzyme_sequences.append((code, enzyme, colors.blue))
            elif color_count == 4: enzyme_sequences.append((code, enzyme, colors.orange))
            elif color_count == 5: enzyme_sequences.append((code, enzyme, colors.black))
            elif color_count == 6: enzyme_sequences.append((code, enzyme, colors.darkgray))
            color_count += 1

    return enzyme_sequences


# enzymes are located in their recognition sites in the genome sequence
# each enzyme sequence is displayed where they were located in the genome sequence
def sequence_placement(enzyme_sequences):
    for site, name, color in enzyme_sequences:
        index = 0
        while True:
            index = virus_record.seq.find(site, start=index)
            if index == -1:
                break
            feature = SeqFeature(FeatureLocation(index, index + len(site)))
            feature_set.add_feature(
                feature,
                color=color,
                name=name,
                label=True,
                label_size=12,
                label_color=color,
            )
            index += len(site)


# OUTPUT FILE
# diagram is drawn in a circular format using the installed ReportLab objects
def output_file():
    diagram.draw(
        format="circular",
        circular=True,
        pagesize=(25*cm, 25*cm),
        start=0,
        end=len(virus_record),
        circle_core=0.5
    )
    # drawn diagram is rendered to the requested file format
    diagram.write("genome_map.png", "PNG")
    diagram.write("genome_map.jpg", "JPG")

# main driver
if __name__ == '__main__':

    # bar display is set up
    bar_display(virus_record)

    # enzyme sequences are retrieved and placed in diagram
    enzyme_sequences = sequence_retrieval()
    sequence_placement(enzyme_sequences)

    # diagram is drawn and rendered as both a jpg and png file
    output_file()
