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
        "@type": ["mip:license"],
        // "@explicit": true,

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

                delete element["conditions"]

                output[element["kind"]] = element
            });

            // console.log(output)
            console.log(__filename);

            cld.writeFile(output, './output/MIP_license.json')
        })

    // .then(file=>
    //     console.log(file[4])
    // )





}

main()