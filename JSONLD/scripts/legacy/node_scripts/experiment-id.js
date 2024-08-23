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
        "@type": "mip:experiment-id",

        // "source-id:activity-participation": [{
        //     "activity-id:name": "",
        //     "@explicit": true,
        // }],

        // "experiment-id:activity-id": {"activity-id:name": "", "@explicit": true},


        // "@embed": "@never",
        "experiment-id:activity-id": {
            // "@embed": "@always",
            // "@id": {},
            // "@type": "mip:activity-id",
            "activity-id:name": {},
            "@explicit": true
        },

        "experiment-id:model-components": {
            "experiment-id:additional-allowed": { "source-type:name": "", "@explicit": true },
            "experiment-id:required": { "source-type:name": "", "@explicit": true },


        },






    }


    jsonld.frame(graphData, frame)
        // .then(cld.printState)
        .then(graphOnly)
        .then(cld.stringify)

        .then(cld.rmld)
        .then(cld.rmnull)
        
        .then(cld.flatten)
        // .then(printState)
        .then(cld.untag)

        .then(str2JSON)
        .then(output => {

            // var output = {}
            // d.forEach(element => {


            //     output[element["name"]] = element
            // });
            // output.forEach(d => {
            //     console.log(d['experiment-id:model-components'])
            // })

            // console.log(d)
            console.log(__filename);

            cld.writeFile(output, './output/CMIP6Plus_experiment-id.json')
        })

    // .then(file=>
    //     console.log(file[4])
    // )





}

main()