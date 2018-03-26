from fmi_getter import *

def write_sampler_geojson(response,directory=".",geojson_file="auto"):
    wfs_response = ElementTree.fromstring(response.read())
    gml_points = wfs_response.findall('.//{%s}Point' % gml_namespace)
    # read location names 
    locations = {}
    geojson_str = geojson_template
    for n, point in enumerate(gml_points):
        point_id = point.attrib['{%s}id' % gml_namespace].split("-")[-1]
        name = point.findall('{%s}name' % gml_namespace)[0].text
        pos = point.findall('{%s}pos' % gml_namespace)[0].text
        longitude = float(pos.split()[1])
        latitude = float(pos.split()[0])
        locations[pos.strip()] = {"site": name,
                                  "longitude": longitude,
                                  "latitude": latitude,
                                  "id": point_id
                                  }
    print ( locations )
    # store values 
    values = []
    try:
        values_el = wfs_response.findall('.//{%s}doubleOrNilReasonTupleList'\
                                         % gml_namespace)[0].text.split("\n")[1:-1]
    except IndexError:
        raise Exception ( "No features" )
    for line in values_el:
        l = line.strip()
        l = l.split()
        values.append( float(l[0]) )
    # iterate over the measurements
    N = 0
    for line in wfs_response.findall('.//{%s}positions'\
                                     % gmlcov_namespace)[0].text.split("\n")[1:-1]:
        l = line.strip()
        l = l.split()
        coords = line.split("  ")[-2]
        timestamp = datetime.utcfromtimestamp(int(l[-1]))
        feature = {
            "type": "Feature", 
            "properties": {},
            "geometry": {"type": "Point"}
        }
        feature["properties"] = {
            "doseRate": values[N],
            "id": locations[coords]["id"],
            "site": locations[coords]["site"],
            "timestamp": datetime.strftime(timestamp,
                                           "%Y-%m-%dT%H:%M:%SZ")
        }
        feature["geometry"]["coordinates"] = [
            locations[coords]["longitude"],
            locations[coords]["latitude"]
        ]
        geojson_str["features"].append(feature)
        N += 1
    if geojson_file=="auto":
        outfile = directory + "/" + datetime.strftime(
            timestamp,"%Y-%m-%dT%H:%M:%S") + ".json"
    else:
        outfile = result_dir + "/stuk_open_data_doserates.json"
    # write output
    with open(outfile, 'w') as fp:
        json.dump(geojson_str, fp)
    return outfile

if __name__=="__main__":
    # TODO: read from command line
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=15)
    result_dir = "samplers"
    tries = 3
    while tries!=0:
        try:
            wfs_response = wfs_request( start_time, end_time, "samplers" )
            tries = 0
        except ReadTimeout:
            tries +- 1
            time.sleep ( 10 )
    geojson = write_sampler_geojson ( wfs_response, result_dir )