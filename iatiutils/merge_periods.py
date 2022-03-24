"""
Merge periods of indicators. Makes some assumptions about the structure of the
data, so only suitable for some publishers.

Copyright (c) 2022 Open Data Services Co-operative Limited

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

import click
from lxml import etree


@click.command()
@click.help_option()
@click.option(
    "-i",
    "--input_file",
    type=click.Path(exists=True),
    help="Provide a path for the input XML file",
)
@click.option("-o", "--output_file", type=click.File("wb"), help="The output file")
def merge_indicator_periods(input_file, output_file):
    root = etree.parse(input_file)

    for activity in list(root.iter("iati-activity")):
        for result in list(activity.iter("result")):
            for indicator in result.iter("indicator"):
                periods = indicator.findall("period")
                if len(periods) != 2:
                    print(activity.find('iati-identifier').text, "has an indicator with", len(periods), "periods")
                    continue
                actual_period = periods[0] if periods[0].find('actual') is not None else periods[1]
                target_period = periods[0] if periods[0].find('target') is not None else periods[1]
                assert actual_period is not None
                assert target_period is not None
                assert actual_period.find('target') is None
                assert target_period.find('actual') is None

                target_period.find('period-end').attrib['iso-date'] = actual_period.find('period-end').attrib['iso-date']
                target_period.append(actual_period.find('actual'))
                indicator.remove(actual_period)

    output_file.write(etree.tostring(root, pretty_print=True))


if __name__ == '__main__':
    merge_indicator_periods()
