// Load the jsonld.js library
const cld = require('cmip_jld');
const { flatten } = require('jsonld/lib/flatten');

// push each function into the global scope
Object.keys(cld).forEach(key => {
    global[key] = cld[key];
});


async function main() {

    const graphData = await readFileFS('./compiled/graph_data.json');

    // if using directly, do not remove graph, else remove graph in parsing. 


    const frame = {
        "@context": {
        },
        "@type": ["mip:institution", "mip:consortium"],
        "@explicit": true,

        "consortium:cmip_acronym": "",
        "institution:cmip_acronym": "",
        "consortium:description": "",
        "institution:name": "",
        "institution:ror": "",
        // "consortium:description": "",
        // "consortium:url": "",
        // "consortium:members": {
        //     "@explicit": true,
        //     "consortia:institution": {
        //         "@explicit": true,
        //         // "institution:name":"",
        //         "refid": "@id"
        // }
        // }


    }


    jsonld.frame(graphData, frame)
        // .then(cld.printState)
        .then(graphOnly)
        .then(cld.stringify)
        .then(cld.flatten)
        .then(cld.rmld)
        .then(cld.rmnull)
        .then(cld.untag)
        .then(str2JSON)
        .then(d => {

            var output = {}
            d.forEach(element => {

                element["institution"] = (element["ror"]) ? true : false

                output[element["cmip_acronym"]] = element
            });

            // console.log(output)
            console.log(__filename);

            cld.writeFile(output, './output/MIP_organisations.json')
        })

    // .then(file=>
    //     console.log(file[4])
    // )





}

main()