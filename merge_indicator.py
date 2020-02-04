"""
Merge all indicators into a single result that have the same result title.

Instructions for Ubuntu:
sudo apt-get install python3-lxml
python3 merge_indicator.py input_file.xml > output_file.xml

Copyright (c) 2018 Open Data Services Co-operative Limited

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""


import sys

from lxml import etree

root = etree.parse(sys.argv[1])

for activity in list(root.iter("iati-activity")):
    actual_results = {}
    for num, result in enumerate(list(activity.iter("result"))):
        title = num
        title_element = result.find("title")
        if title_element is not None:
            narrative_element = title_element.find("narrative")
            if narrative_element is not None:
                title = narrative_element.text.strip()

        if title in actual_results:
            result_element = actual_results[title]
            for indicator_element in result.iter("indicator"):
                result_element.append(indicator_element)
            result.getparent().remove(result) 
        else:
            actual_results[title] = result

print(etree.tostring(root, pretty_print=True).decode())

