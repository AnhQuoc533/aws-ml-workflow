import json
import zipfile


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
        helpful_votes = float(l_object['helpful'][0])
        total_votes = l_object['helpful'][1]
        reviewText = l_object['reviewText']
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
        label = d.split()[0]        
        sentences = " ".join(d.split()[1:]).split(".") # Initially split to separate label, then separate sentences
        for s in sentences:
            if s: # Make sure sentences isn't empty. Common w/ "..."
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


if __name__ == "__main__":
    unzipped_path = unzip_data('/opt/ml/processing/input/Toys_and_Games_5.json.zip')
    labeled_data = label_data(unzipped_path)
    new_split_sentence_data = split_sentences(labeled_data)
    write_data(new_split_sentence_data, '/opt/ml/processing/output/train/hello_blaze_train_scikit.txt', '/opt/ml/processing/output/test/hello_blaze_test_scikit.txt', .9)
