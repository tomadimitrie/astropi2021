def get_file_name_from_path(file_path):
    """
    Function that computes the file name from the path given
    :param file_path: the path to the file
    :return: the file name (str)
    """
    return file_path.split("/")[-1].split(".")[0]