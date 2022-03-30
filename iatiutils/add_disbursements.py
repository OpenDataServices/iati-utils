"""
Copyright (c) 2021-2022 Open Data Services Co-operative Limited

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
import datetime as dt
from dateutil.relativedelta import relativedelta


# Copied from https://github.com/OpenDataServices/iati-colab/blob/main/iati_colab.py#L68
def is_current(activity):
    status_check = False
    planned_end_date_check = False
    actual_end_date_check = False
    transaction_date_check = False

    # print("Activity {} of {}".format(count, len(big_iati)))

    if activity.xpath("activity-status[@code=2]"):
        status_check = True

    if activity.xpath("activity-date[@type=3]/@iso-date"):
        date_time_obj = dt.datetime.strptime(activity.xpath("activity-date[@type=3]/@iso-date")[0], "%Y-%m-%d")
        if date_time_obj > (dt.datetime.now() - relativedelta(years=1)):
            planned_end_date_check = True

    if activity.xpath("activity-date[@type=4]/@iso-date"):
        date_time_obj = dt.datetime.strptime(activity.xpath("activity-date[@type=4]/@iso-date")[0], "%Y-%m-%d")
        if date_time_obj > (dt.datetime.now() - relativedelta(years=1)):
            actual_end_date_check = True

    if activity.xpath("transaction/transaction-type[@code=2 or @code=3 or @code=4]"):
        dates = activity.xpath(
            "transaction[transaction-type[@code=2 or @code=3 or @code=4]]/transaction-date/@iso-date"
        )
        date_truths = [
            dt.datetime.strptime(date, "%Y-%m-%d") > (dt.datetime.now() - relativedelta(years=1)) for date in dates
        ]
        if True in date_truths:
            transaction_date_check = True

    pwyf_current = status_check or planned_end_date_check or actual_end_date_check or transaction_date_check

    return pwyf_current


@click.command()
@click.help_option()
@click.option(
    "-i",
    "--input_file",
    type=click.Path(exists=True),
    help="Provide a path for the input XML file",
)
@click.option("-o", "--output_file", type=click.File("wb"), help="The output file")
def add_disbursements(input_file, output_file):
    root = etree.parse(input_file)

    for activity in root.iter("iati-activity"):
        if is_current(activity) and len(activity.xpath("activity-status[@code=1]")) == 0 and len(activity.xpath("transaction[transaction-type/@code='3']")) == 0:
            transactions = activity.xpath("transaction")
            transactions[-1].addnext(etree.XML("""
                <transaction>
                    <transaction-type code="3" />
                    <transaction-date iso-date="2022-02-28" />
                    <value currency="XDR" value-date="2022-02-28">5000</value>
                    <description>
                        <narrative>Disbursement in February 2022</narrative>
                    </description>
                </transaction>
            """))
            print(activity.find('iati-identifier').text)

    output_file.write(etree.tostring(root, pretty_print=True))


if __name__ == '__main__':
    add_disbursements()
