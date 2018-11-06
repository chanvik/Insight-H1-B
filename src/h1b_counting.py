import csv
import sys


def write_output_txt(op_file, columns, dict_data):
    """
    Function to write output to text file
    :param op_file: output filename path
    :param columns: header of the output file
    :param dict_data: list to write to output file
    :return text file: output text file with header and data
    """
    try:
        with open(op_file, 'w') as output_file:
            writer = csv.writer(output_file, delimiter=';')
            dict_data = [columns] + dict_data
            for data in dict_data:
                writer.writerow(data)
    except IOError as err:
        print(str(err), "Error in writing output to file")
    return


def read_file(path):
    """
    Function to read the input file and return as a data list
    :param path: path of the input file
    :return list: list of input data read from the file
    """
    data_lst = []
    with open(path) as f:
        data = f.read()
        rows = data.split('\n')
        for row in rows:
            if len(row) > 0:
                values = row.split(';')
                data_lst.append(values)
    return data_lst


def certified_visa(input_list, header):
    """
    Function which returns a list of certified visa applicants with case status "CERTIFIED"
    :param input_list: data list without header
    :param header: header list
    :return list: list of data of  certified applicants
    """
    idx = header.index('CASE_STATUS')
    certified_list = []
    try:
        for values in input_list:
            if values[idx] == 'CERTIFIED':
                certified_list.append(values)
    except Exception as er:
        print(str(er), "Unable to process the list of certified applicants")
    return certified_list


def top_10(approved_list, header, label):
    """
    Function which returns top 10 list of applicants by state or occupation
    :param approved_list: list of certified applicants
    :param header: header list
    :param label: occupation or state label to retrieve specific output list
    :return dictionary: dictionary of top 10 occupations or state applicants
     with key as top 10 occupations or state and
     value count of certified applicants against state or occupation
    """
    idx = header.index(label)
    top10_list = dict()
    try:
        for values in approved_list:
            key = values[idx].replace('"', '').strip()
            if key not in top10_list:
                top10_list[key] = 0
            top10_list[key] += 1
        top10_list = sorted(top10_list.items(), key=lambda x: (-x[1], x[0]))[:10]
    except Exception as er:
        print(str(er), " Unable to find the top 10 certified applicants")
    return top10_list


def top_10_percentage(top_list, total):
    """
     Function which returns top 10 list of applicants by state or occupation
     with percentage of certified applicants
    :param top_list: top 10 state or occupation list
    :param total: no of total applicants
    :return dictionary: dictionary of top 10 occupations or state applicants
     with key as top 10 occupations or state and
     values count and percentage of certified applicants against state or occupation
    """
    result = []
    try:
        for values in top_list:
            p = '{0:.1f}%'.format((float(values[1]) / total) * 100)
            result.append([values[0], values[1], p])
    except Exception as e:
        print(str(e), "Unable to calculate the percentage of top 10 certified applicants")
    return result


if __name__ == '__main__':
    input_path = sys.argv[1]
    data_list = read_file(input_path)
    header_list = data_list[0]
    data_list = data_list[1:]
    certified_visa_list = certified_visa(data_list, header_list)
    occupation = top_10(certified_visa_list, header_list, 'SOC_NAME')
    states = top_10(certified_visa_list, header_list, 'WORKSITE_STATE')
    total_applicants = len(certified_visa_list)
    occupation_percentage = top_10_percentage(occupation, total_applicants)
    states_percentage = top_10_percentage(states, total_applicants)
    occupations_header_columns = ['TOP_OCCUPATIONS', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE']
    states_header_columns = ['TOP_STATES', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE']
    list_occupation = occupation_percentage
    list_states = states_percentage
    top10_occupations_file = sys.argv[2]
    top10_states_file = sys.argv[3]
    write_output_txt(top10_occupations_file, occupations_header_columns, list_occupation)
    write_output_txt(top10_states_file, states_header_columns, list_states)
