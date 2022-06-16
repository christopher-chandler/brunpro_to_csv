import pandas as pd


def tsv_to_csv(tsv_file, save_file) -> None:
    """
    This function reshapes the text exported by anki relating to the bunpro
    deck into a .csv file so that it can be easily imported into notion as a
    database.

    :param tsv_file (str): The location of the file to be transformed.
    :param save_file (str): The name of the save file.
    :return: None
    """

    tsv_table = pd.read_table(tsv_file, sep="\t")

    tsv_table.columns = [
        "Sentence",
        "Translation",
        "Sentence Nuance",
        "JLPT Level",
        "Grammar",
        "Grammar Meaning",
        "Grammar Structure",
        "Grammar Nuance",
        "Supplemental Links",
        "Offline Resources"
    ]

    # Add extra table headers
    tsv_table["Learning Status"] = "In Progress"
    tsv_table["Examples"] = "Examples"

    # Restructure table
    tsv_table = tsv_table[[
        "Grammar",
        "JLPT Level",
        "Sentence",
        "Translation",
        "Examples",
        "Learning Status",
        "Grammar Meaning",
        "Grammar Structure",
        "Grammar Nuance",
        "Sentence Nuance",
        "Supplemental Links",
        "Offline Resources"
    ]]

    # Remove cloze markers
    tsv_table["Sentence"] = tsv_table["Sentence"].str.replace(r"[{{}}:]", "")
    tsv_table["Sentence"] = tsv_table["Sentence"].str.replace(r"c[0-9]", "")

    # Remove html markers
    tsv_table["Grammar Structure"] = tsv_table["Grammar Structure"].str.replace(
        r"<[^>]*>", ""
    )
    tsv_table["Grammar Meaning"] = tsv_table["Grammar Meaning"].str.replace(
        r"<[^>]*>", "")
    tsv_table["Supplemental Links"] = tsv_table[
        "Supplemental Links"].str.replace(
        r"<[^>]*>", ""
    )
    tsv_table["Offline Resources"] = tsv_table["Offline Resources"].str.replace(
        r"<[^>]*>", "\n"
    )
    tsv_table["Offline Resources"] = tsv_table["Offline Resources"].str.replace(
        r"&#x27;s", "'S"
    )
    # Remove long empty spaces
    tsv_table["Grammar Meaning"] = tsv_table["Grammar Meaning"].str.replace(
        r"                     ", " "
    )
    duplicate_grammar = tsv_table[tsv_table["Grammar"].duplicated() == True].to_dict()
    duplicate_info = {}

    """
    Every grammar point has an example sentence which leads to 
    there being many rows all relating to the same grammar point, 
    but only differ due to the the examples. The examples are removed from the examples 
    and the duplicate grammar entries are deleted. 
    """
    for _ in duplicate_grammar:
        grammar = duplicate_grammar["Grammar"]
        sentence = duplicate_grammar["Sentence"]
        for example in grammar:
            point = grammar.get(example)
            duplicate_info[point] = []

        for example in grammar:
            sen = sentence.get(example)
            point = grammar.get(example)
            duplicate_info[point].append(sen)

    tsv_table.drop_duplicates(subset="Grammar", keep="first", inplace=True)

    # Move the grammar point examples to the main grammar point entry
    for i in range(len(tsv_table)):
        grammar = tsv_table.iloc[i]["Grammar"]
        sen = duplicate_info[grammar]
        tsv_table.iloc[i]["Examples"] = "\n ".join(sen)

    tsv_table.to_csv(save_file, index=False)

    # output
    print("Successfully made .csv file. Check the directory. ")


tsv_file = "bunpro.tsv"
tsv_to_csv(tsv_file, "brunpro_results.csv")
