import json
import zipfile
import argparse


def unzip_data(input_data_path):
    # Unzip the archive to the local directory. 
    with zipfile.ZipFile(input_data_path, 'r') as input_data_zip:
        input_data_zip.extractall('.')
        return input_data_zip.namelist()[0]


def label_data(input_data):
    labeled_data = []
    HELPFUL_LABEL = "__label__1"
    UNHELPFUL_LABEL = "__label__2"
     
    for l in open(input_data, 'r'):
        l_object = json.loads(l)
        reviewText = l_object['reviewText'].strip()
        # Make sure review text is not empty
        if reviewText:
            helpful_votes = float(l_object['helpful'][0])
            total_votes = l_object['helpful'][1]
            if total_votes != 0:
                if helpful_votes / total_votes > .5:
                    labeled_data.append(" ".join([HELPFUL_LABEL, reviewText]))
                elif helpful_votes / total_votes < .5:
                    labeled_data.append(" ".join([UNHELPFUL_LABEL, reviewText]))
          
    return labeled_data


def split_sentences(labeled_data):
    # Labeled data is a list of sentences, starting with the label defined in label_data. 
    new_split_sentences = []
    for d in labeled_data:
        # Separate label, then separate sentences
        label, review = d.split(maxsplit=1)
        sentences = review.split(".")

        for s in sentences:
            s = s.strip()
            # Make sure sentence isn't empty. Common w/ "..."
            if s:
                new_split_sentences.append(" ".join([label, s]))
    return new_split_sentences


def write_data(data, train_path, test_path, proportion):
    border_index = int(proportion * len(data))
    train_f = open(train_path, 'w')
    test_f = open(test_path, 'w')
    index = 0
    for d in data:
        if index < border_index:
            train_f.write(d + '\n')
        else:
            test_f.write(d + '\n')
        index += 1

    train_f.close()
    test_f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    unzipped_path = unzip_data('/opt/ml/processing/input/data/' + args.filename)
    labeled_data = label_data(unzipped_path)
    new_split_sentence_data = split_sentences(labeled_data)

    data_name = args.filename.split(".", maxsplit=1)[0]
    write_data(new_split_sentence_data, f'/opt/ml/processing/output/train/{data_name}_train.txt', f'/opt/ml/processing/output/test/{data_name}_test.txt', .8)
