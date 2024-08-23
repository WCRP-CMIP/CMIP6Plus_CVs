// Load the jsonld.js library
const cld = require('cmip_jld');
const { flatten } = require('jsonld/lib/flatten');

// push each function into the global scope
Object.keys(cld).forEach(key => {
    global[key] = cld[key];
});


async function main() {

    let cmip6plusData = readFileFS('./compiled/graph_data.json');

    let mipData = readFileURL('https://raw.githubusercontent.com/PCMDI/mip-cmor-tables/jsonld/JSONLD/scripts/compiled/graph_data.min.json');

    const graphData = await mergeFiles([cmip6plusData, mipData]);

    // if using directly, do not remove graph, else remove graph in parsing. 


    const frame = {
        "@context": {
        },
        "@type": ["mip:core-descriptors"],
        "core:mip-era": {"mip:name":{},"@explicit":true},
        "core:product": {"product:kind":{},"@explicit":true},
        "core:drs": {},

        // "core:mip-era":{"mip:name":{}},
        // "@explicit": true,



    }


    jsonld.frame(graphData, frame)
        // .then(cld.printState)
        // .then(graphOnly)
        .then(cld.stringify)
        
        .then(cld.rmld)
        .then(cld.rmnull)
        .then(cld.flatten)
        .then(cld.untag)
        .then(printState)
        .then(str2JSON)
        .then(output => {

            // var output = {}
            // d.forEach(element => {


            //     output[element["name"]] = element
            // });

            // console.log(d)
            console.log(__filename);

            cld.writeFile(output, './output/CMIP6Plus_core-descriptors.json')
        })

    // .then(file=>
    //     console.log(file[4])
    // )





}

main()