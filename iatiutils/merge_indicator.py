import sys

from lxml import etree

def merge_indicator(input_file):
    """ Merge all indicators into a single result that have the same result title."""
    root = etree.parse(input_file)

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

    for activity in list(root.iter("iati-activity")):
        for result in list(activity.iter("result")):
            actual_indicators = {}
            for num, indicator in enumerate(list(result.iter("indicator"))):
                title = num
                title_element = indicator.find("title")
                if title_element is not None:
                    narrative_element = title_element.find("narrative")
                    if narrative_element is not None:
                        title = narrative_element.text.strip()

                if title in actual_indicators:
                    indicator_element = actual_indicators[title]
                    for period_element in indicator.iter("period"):
                        indicator_element.append(period_element)
                    indicator.getparent().remove(indicator) 
                else:
                    actual_indicators[title] = indicator

    output = etree.tostring(root, pretty_print=True).decode()
    return output
