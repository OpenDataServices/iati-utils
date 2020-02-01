import sys

from lxml import etree

root = etree.parse(sys.argv[1])

actual_indicators = {}

for num, indicator in enumerate(list(root.iter("indicator"))):
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

print(etree.tostring(root, pretty_print=True).decode())

