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
        "@type": ["mip:required-global-attributes"],
        "core:required-global-attributes":{},
        "@explicit": true,



    }


    jsonld.frame(graphData, frame)
        // .then(cld.printState)
        // .then(graphOnly)
        .then(cld.stringify)
        .then(console.warn)
        // .then(cld.flatten)
        .then(cld.rmld)
        .then(cld.rmnull)
        .then(cld.untag)
        .then(str2JSON)
        .then(output => {

            // var output = {}
            // d.forEach(element => {


            //     output[element["name"]] = element
            // });

            // console.log(d)
            console.log(__filename);

            cld.writeFile(output, './output/CMIP6Plus_required-global-attributes.json')
        })

    // .then(file=>
    //     console.log(file[4])
    // )





}

main()