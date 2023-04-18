from parallel_coordinate_finder import key_sorting
import glob


def combines_csvs(name):
    # Create a list of file paths to combine
    prefix = "outputsmall_"
    csvs = glob.glob("outputsmall*")
    csvs = sorted(csvs, key=lambda x: key_sorting(x, prefix))  # list of csvs

    # Open the all_2011_2012.csv file in append mode
    with open(f'{name.split("/")[-1]}.csv', 'a') as f:
        # Loop through each file and append its contents to all_2011_2012.csv
        for file in csvs:
            with open(file, 'r') as f1:
                contents = f1.read()
                f.write('\n')
                f.write(contents)
