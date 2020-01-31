# The seed/tip url is declared as a constant.
SEED = 'http://info.sjsu.edu/web-dbgen/artic/all-course-to-course.html'

import urllib.request
import bs4
import re


def get_links(top_url):
    """

    To generate absolute links from base url
    :param top_url: The info.html web page that will be parsed
    :return: Return a list of links found on the info.html web page
    """
    # absolute_links = []
    # Extract list of relevant (absolute) links referenced in top_url
    try:
        with urllib.request.urlopen(top_url) as url_file:
            bytes = url_file.read()
    except urllib.error.URLError as url_err:
        print(f'Error opening url: {top_url}\n{url_err}')
    else:
        soup = bs4.BeautifulSoup(bytes, "html.parser")
        tables = soup.find_all('table')
        table = tables[2]
        absolute_links = [
            urllib.parse.urljoin(top_url, anchor.get('href', None))
            for anchor in table('a')]
    return absolute_links


def extract_info(url, course_regex):
    """

    To extract college and course information from url based on course regex
    :param url: URL is being used to extract information
    :param course_regex: Regular expression to handle similar variations of
    course name
    :return: The extracted information from the webpage
    """
    # Return college and equivalent course found in the given url if any

    class_list = []
    for link in get_links(SEED):
        try:
            with urllib.request.urlopen(link) as url_file:
                bytes = url_file.read()
        except urllib.error.URLError as url_err:
            print(f'Error opening url: {url}\n{url_err}')
        else:
            soup = bs4.BeautifulSoup(bytes, "html.parser")
            table = soup.find_all('table')
            table = table[2]
            for each in table('tr'):
                var_string = str(each)
                if var_string.__contains__('"top"'):
                    var_string = var_string[17:-5]
                    split_letters = list(course_regex)
                    regex = (re.findall('\s*0*'.join(split_letters),
                                        var_string
                                        , re.IGNORECASE | re.DOTALL))
                    if regex:
                        college_name = (soup('h3')[0].get_text()[31:])
                        class_descrip = each('td')[2].get_text(separator=' ')
                        format_descrip = ' '.join(class_descrip.split())
                        if format_descrip != "No Current Equivalent":
                            class_list.append(college_name + ": " +
                                              format_descrip)
                    else:
                        pass
    return class_list


def harvest(all_links, course_regex):
    """

    To generate on string that contains all equivalency info
    :param all_links: a list that contains all related url links
    :param course_regex: regular expression to handle similar variations of
    course name
    :return: a string that invoke all equivalency info
    """
    # Invoke extract_info to get the equivalency info for each link in
    # all_links.
    # Join all the equivalency info into a single string (entries must
    # be separated by new line characters).

    new_str = '\n'.join(extract_info(all_links, course_regex))
    return new_str


def report(info, course_name):
    """

    To generate a text file which contains all equivalency info
    according to course name
    :param info: a string that invoke all equivalency info
    :param couse_name: a string that will be the file name
    """
    # Write the info harvested to a text file with the name:
    # course_name.txt where course_name is the name as entered by user.
    copy_str = harvest(info, course_name)
    str_list = list(copy_str)
    filename = str(course_name) + '.txt'
    f = open(filename, 'w+')
    for each in str_list:
        f.write(each)



def main():
    # Get all the relevant links referenced from the seed (top_url)
    get_links(SEED)
    # Prompt the user for a course name
    class_name = (input("Please enter a course number: "))

    extract_info(SEED, str(class_name))

    # Build a regex corresponding to the course name specified
    # Harvest information from all the links
    result = harvest(SEED, str(class_name))
    # Write the harvested information to the output file
    report(result, str(class_name))


if __name__ == "__main__":
    main()
