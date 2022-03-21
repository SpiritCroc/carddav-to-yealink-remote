# Based on
# https://gist.github.com/tsenger/ca4480235b5b29431965ee0b919ff6ad
# https://github.com/ProVuUK/yealink-xml-phonebook-example/blob/master/examples/phonebook.xml

# Convert CardDav contacts to Yealink xml

# To enable this, put it on some webserver. Then, on the yealink web interface:
# Directory / Remote Phone Book -> add URL, enable call lookup
# Directory / Settings -> Move Remote Phone Book to enabled sections

import vobject


def vcf_to_xml(config, vcf):
    vcards = vobject.readComponents(vcf)

    input_counter = 0
    output_counter = 0

    if "map_number_types" in config:
        map_number_types = config["map_number_types"]
    else:
        map_number_types = dict()
    if "country_code" in config:
        country_code = config["country_code"]
    else:
        country_code = None

    result = "<YealinkIPPhoneDirectory>\n"

    for vcard in vcards:
        input_counter += 1
        numbers = []
        givenname = ''
        familyname = ''
        for p in vcard.getChildren():
            if p.name == "N":
                givenname = p.value.given
                familyname = p.value.family
            if p.name == "TEL":
                try:
                    itype = p.type_param.lower()
                except Exception:
                    itype = "other"
                if itype in map_number_types:
                    ntype = map_number_types[itype]
                else:
                    print(f"Warn: unknown type {itype} for {p.value}")
                    ntype = itype
                t = ntype, p.value
                numbers.append(t)

        if numbers:
            output_counter += 1

            if givenname and familyname:
                name = f"{familyname}, {givenname}"
            elif givenname:
                name = givenname
            else:
                print("Unsupported name format, TODO support me... ")
                continue
            result += '  <DirectoryEntry>\n'
            result += f'    <Name>{name}</Name>\n'

            for n in numbers:
                ntype, value = n
                # Normalize numbers
                value = value.replace(" ", "")
                value = value.replace("-", "")
                if value.startswith("+"):
                    value = value.replace("+", "00", 1)
                if country_code and value.startswith(country_code):
                    value = value.replace(country_code, "0", 1)
                result += f'    <Telephone label="{ntype}">{value}</Telephone>\n'

            result += '  </DirectoryEntry>\n'

    result += "</YealinkIPPhoneDirectory>\n"
    return result
