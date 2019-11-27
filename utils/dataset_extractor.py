from collections import defaultdict
import glob
import re

WORDS_PER_SEGMENT = 100 # How Many words will be in each segment. 0 set to default for each data set.
MAX_ADD_TO_LABEL = 15 # for 'chinuch_extractor' and 'noda_biyhudah_extractor'.


# Extract the data sets from Rambam text.
def rambam_extractor(path):
    return_data = defaultdict(list)
    for file in glob.glob(path + '/*'):
        # the label is the name of the file.
        label = file.rsplit('\\', 1)[1].split('.')[0]
        data = ''
        for line in open(file, 'r', encoding="utf8"):
            if line == '\n':
                continue

            line = line.strip()

            # Skip the line that indicate number of the Halacha in the file.
            if "הלכות" in line:
                continue
            else:
                # Edit the file for the data e.g. delete double space and symbols.
                line = line.split("  ", 1)[1]

                line = re.sub(r'\s\([^()]*\)', '', line)
                line = re.sub(r'\[[^()]*\]\s', '', line)

                line = re.sub('[,.;:)("]', '', line)
                line = line.replace("--", ' ')
                line = line.replace('-', ' ')
                line = line.replace("  ", ' ')

                # Add the line to the data from the file
                if data:
                    data += ' ' + line
                else:
                    data = line

        # Split the data into segment each of size NUM_OF_WORDS.
        data = data.split()
        # Set the divider by words.
        if WORDS_PER_SEGMENT < 1:
            words = 100
        else:
            words = WORDS_PER_SEGMENT

        data = [' '.join(data[word : word + words]) for word in range(0, len(data), words)]
        return_data[label] = data

    return(return_data)


# Extract the data sets from Ben Ish Hai text.
def ben_ish_hai_extractor(path):
    return_data = defaultdict(list)
    for file in glob.glob(path + '/*'):
        # the label is the name of the file.
        label = file.rsplit('\\', 1)[1].split('.')[0]
        data = ''
        for line in open(file, 'r', encoding="utf8"):
            if (line == '\n') or (line[0].isdigit()) or ("בן איש חי – הלכות" in line):
                continue

            line = line.strip()
            sline = line.split()
            # If the result is True put the segment in the set and start a new segment.
            if (len(sline) == 2) and (sline[0] == "אות"):
                if data:
                    return_data[label].append(data)
                    data = ''

            else:
                # Edit the file for the data e.g. delete utf-8 bom and symbols.
                line = re.sub('[,.;:)(]', '', line)
                # Remove utf-8 bom
                bom = line[0].encode("utf-8")
                if bom == b'\xef\xbb\xbf':
                    line = line[1:]

                # Add the line to the data.
                if data:
                    data += ' ' + line
                else:
                    data = line

        if data:
            return_data[label].append(data)

    # Check if the data need to be divided by words and not by section.
    if WORDS_PER_SEGMENT > 0:
        for label in return_data:
            # Rejoin and split the data acording to WORDS_PER_SEGMENT
            data = ' '.join(return_data[label])
            data = data.split()
            data = [' '.join(data[word : word + WORDS_PER_SEGMENT]) for word in range(0, len(data), WORDS_PER_SEGMENT)]
            return_data[label] = data

    return return_data


# Extract the data sets from Chinuch text. The number of segemnt in each label is limited
#   by MAX_ADD_TO_LABEL
def chinuch_extractor(path):
    return_data = defaultdict(list)
    data = ''
    label = ''

    for line in open(path, 'r', encoding="utf8"):
        if line == '\n':
            continue

        line = line.strip()
        sline = line.split()
        # If the result is True put the segment in the set and start a new segment.
        if sline[0] == '#':
            if label and (len(return_data[label]) < MAX_ADD_TO_LABEL):
                return_data[label].append(data)

            data = ''
            # the label is the name after the #.
            label = line.split(' ', 1)[1]

        else:
            # Edit the file for the data e.g. delete utf-8 bom and symbols.
            line = re.sub('[,.;:)(]', '', line)
            # Remove utf-8 bom
            bom = line[0].encode("utf-8")
            if bom == b'\xef\xbb\xbf':
                line = line[1:]

            # Add the line to the data.
            if data:
                data += ' ' + line
            else:
                data = line

    if label and (len(return_data[label]) < MAX_ADD_TO_LABEL):
        return_data[label].append(data)

    # Check if the data need to be divided by words and not by section.
    if WORDS_PER_SEGMENT > 0:
        for label in return_data:
            # Rejoin and split the data acording to WORDS_PER_SEGMENT
            data = ' '.join(return_data[label])
            data = data.split()
            data = [' '.join(data[word : word + WORDS_PER_SEGMENT]) for word in range(0, len(data), WORDS_PER_SEGMENT)]
            return_data[label] = data

    return return_data


# Extract the data sets from Kizur Shulchan Aruch text.
def kizur_shulchan_aruch_extractor(path):
    return_data = defaultdict(list)
    for file in glob.glob(path + '/*'):
        # the label is the name of the file.
        label = file.rsplit('\\', 1)[1].split('.')[0]
        data = ''
        for line in open(file, 'r', encoding="utf8"):
            if line == '\n':
                continue

            line = line.strip()
            sline = line.split()
            # If the result is True put the segment in the set and start a new segment.
            if (len(sline) == 2) and (sline[0] == "סעיף"):
                if data:
                    return_data[label].append(data)
                    data = ''

            else:
                # Edit the file for the data e.g. delete utf-8 bom and symbols.
                line = re.sub('[,.;:)(]', '', line)
                # Remove utf-8 bom
                bom = line[0].encode("utf-8")
                if bom == b'\xef\xbb\xbf':
                    line = line[1:]

                # Add the line to the data.
                if data:
                    data += ' ' + line
                else:
                    data = line

        if data:
            return_data[label].append(data)

    # Check if the data need to be divided by words and not by section.
    if WORDS_PER_SEGMENT > 0:
        for label in return_data:
            # Rejoin and split the data acording to WORDS_PER_SEGMENT
            data = ' '.join(return_data[label])
            data = data.split()
            data = [' '.join(data[word : word + WORDS_PER_SEGMENT]) for word in range(0, len(data), WORDS_PER_SEGMENT)]
            return_data[label] = data

    return return_data


# Extract the data sets from Noda Biyhudah text. The number of segemnt in each label is limited
#   by MAX_ADD_TO_LABEL
def noda_biyhudah_extractor(path):
    return_data = defaultdict(list)
    data = ''
    label = ''

    for line in open(path, 'r', encoding="utf8"):
        if line == '\n':
            continue

        line = line.strip()
        sline = line.split()
        # If the result is True put the segment in the set and start a new segment.
        if sline[0] == "Teshuva":
            if label and (len(return_data[label]) < MAX_ADD_TO_LABEL):
                return_data[label].append(data)

            data = ''
            # the label is the after "Teshuva {i}".
            sline = line.split(' ', 2)
            if len(sline) == 3:
                label = sline[2]
            else:
                label = ''


        else:
            # Edit the file for the data e.g. delete utf-8 bom and symbols.
            line = line.replace("<b>", '')
            line = line.replace("</b>", '')
            line = re.sub('[,.;:)(]', '', line)

            # Remove utf-8 bom
            bom = line[0].encode("utf-8")
            if bom == b'\xef\xbb\xbf':
                line = line[1:]

            # Add the line to the data.
            if data:
                data += ' ' + line
            else:
                data = line

    if label and (len(return_data[label]) < MAX_ADD_TO_LABEL):
        return_data[label].append(data)

    # Check if the data need to be divided by words and not by section.
    if WORDS_PER_SEGMENT > 0:
        for label in return_data:
            # Rejoin and split the data acording to WORDS_PER_SEGMENT
            data = ' '.join(return_data[label])
            data = data.split()
            data = [' '.join(data[word : word + WORDS_PER_SEGMENT]) for word in range(0, len(data), WORDS_PER_SEGMENT)]
            return_data[label] = data

    return return_data


# Extract the data sets from Tur text.
def tur_extractor(path):
    return_data = defaultdict(list)
    for file in glob.glob(path + '/*'):
        # the label is the name of the file.
        label = file.rsplit('\\', 1)[1].split('.')[0]
        data = ''
        for line in open(file, 'r', encoding="utf8"):
            if (line == '\n') or (line[0].isdigit()) or ("www" in line):
                continue

            line = line.strip()
            sline = line.split()
            # If the result is True put the segment in the set and start a new segment.
            if (len(sline) == 2) and (sline[0] == "סימן"):
                if data:
                    return_data[label].append(data)
                    data = ''

            else:
                # Edit the file for the data e.g. delete utf-8 bom and symbols.
                line = re.sub('[,.;:)(]', '', line)
                # Remove utf-8 bom
                bom = line[0].encode("utf-8")
                if bom == b'\xef\xbb\xbf':
                    line = line[1:]

                # Add the line to the data.
                if data:
                    data += ' ' + line
                else:
                    data = line

        if data:
            return_data[label].append(data)

    # Check if the data need to be divided by words and not by section.
    if WORDS_PER_SEGMENT > 0:
        for label in return_data:
            # Rejoin and split the data acording to WORDS_PER_SEGMENT
            data = ' '.join(return_data[label])
            data = data.split()
            data = [' '.join(data[word : word + WORDS_PER_SEGMENT]) for word in range(0, len(data), WORDS_PER_SEGMENT)]
            return_data[label] = data

    return return_data
