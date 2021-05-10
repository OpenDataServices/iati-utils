import csv
import requests
import time
import click

# input_file="test/gavi.csv"
# output_file="test.csv"
CSV_DELIMITER = ','
CSV_QUOTECHAR = '"'
LATLNG_FIELD_INDEX = 5
LATLNG_FIELD_SPLIT_CHAR = ' '
# Free account gives you 1000 lookups an hour so you need this high
SLEEP = 4
GEONAMES_USERNAME = 'demo'

@click.command()
@click.help_option()
@click.option('-i', '--input_file', help='Provide a path for the input CSV file')
@click.option('-o', '--output_file', help='Specify a filename for the output CSV')
def country_lookup(input_file, output_file):
    # Load existing output into memory
    # This is so if script crashes half way through it picks up where it left off.
    # (Touch output file before starting)
    existingOutput = []
    with open(output_file) as read_out_fp:
        csvreader = csv.reader(read_out_fp, delimiter=CSV_DELIMITER, quotechar=CSV_QUOTECHAR)
        print(csvreader)
        header = next(csvreader)
        for row in csvreader:
            existingOutput.append(row)

    # Main loop over input
    with open(input_file) as in_fp:
        with open(output_file, "w", newline="") as out_fp:
            csvreader = csv.reader(in_fp, delimiter=CSV_DELIMITER, quotechar=CSV_QUOTECHAR)
            csvwriter = csv.writer(out_fp, delimiter=CSV_DELIMITER,  quotechar=CSV_QUOTECHAR, quoting=csv.QUOTE_MINIMAL)
            header = next(csvreader)
            header.append('COUNTRY-FROM-LAT-LNG')
            csvwriter.writerow(header)

            for row in csvreader:

                # If there is data for this already in output, just use that and don't look up again
                if len(existingOutput) > 0:

                    existing_row = existingOutput.pop(0)

                    # The existing row we got from output should match the input row we are trying to process
                    # Let's check that!
                    if existing_row[0] != row[0] or \
                        existing_row[1] != row[1] or \
                        existing_row[2] != row[2] or \
                        existing_row[3] != row[3] or \
                        existing_row[4] != row[4] or \
                        existing_row[5] != row[5]:
                        print("EXISTING ROW PROBLEM")
                        print(', '.join(existing_row))
                        print(', '.join(row))
                        exit(-1)

                    csvwriter.writerow(existing_row)

                # No data already - we need to look up ourselves
                else:

                    # Some rows are empty latlng
                    if row[LATLNG_FIELD_INDEX].strip():

                        latlngfielddata = row[LATLNG_FIELD_INDEX].strip()
                        # Some data entries have multiple spaces between lat lng, some have 3,
                        # So this line is done twice to always bring it back to 1 space.
                        latlngfielddata = latlngfielddata.replace(LATLNG_FIELD_SPLIT_CHAR+LATLNG_FIELD_SPLIT_CHAR, LATLNG_FIELD_SPLIT_CHAR)
                        latlngfielddata = latlngfielddata.replace(LATLNG_FIELD_SPLIT_CHAR+LATLNG_FIELD_SPLIT_CHAR, LATLNG_FIELD_SPLIT_CHAR)
                        lat, lng = latlngfielddata.split(LATLNG_FIELD_SPLIT_CHAR)
                        url = 'http://api.geonames.org/countryCode?lat={}&lng={}&username={}'.format(lat.strip(), lng.strip(), GEONAMES_USERNAME)
                        r = requests.get(url)
                        if r.status_code != 200:
                            print("API PROBLEM")
                            print(', '.join(row))
                            print(r.status_code)
                            print(r.text)
                            exit(-1)

                        if r.text.strip() == 'ERR:15:no country code found':
                            row.append('')
                        elif r.text.startswith("ERR"):
                            print("API PROBLEM")
                            print(', '.join(row))
                            print(r.status_code)
                            print(r.text)
                            exit(-1)
                        else:
                            row.append(r.text.strip())
                    else:
                        row.append('')

                    csvwriter.writerow(row)

                    time.sleep(SLEEP)

                    #exit()

if __name__ == '__main__':
    country_lookup()
