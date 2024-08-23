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
            "@vocab": "source-id:",
        },
        "@type": ["mip:source-id"],
        "source-id:activity-participation": [{
            "activity-id:name": "",
        "@explicit": true,
        }],

        "source-id:model-component": [{
            "model-component:name": "",
            "model-component:realm": {
                "realm:name": "",
                "@explicit": true,
            },

        "source-id:license": {
            "kind": {},
        },
        "@explicit": true,
        }],

        
        // "core:required-global-attributes":{},
        // "@explicit": true,



    }


    jsonld.frame(graphData, frame)
        // .then(cld.printState)
        .then(graphOnly)
        .then(cld.stringify)
        
        .then(cld.rmld)
        .then(cld.rmnull)
        .then(cld.untag)
        .then(cld.flatten)
        .then(str2JSON)
        .then(output => {

            // var output = {}
            // d.forEach(element => {


            //     output[element["name"]] = element
            // });
            // output.forEach(d=>{
            // console.log(d['activity-participation'])
            // })

            console.log(output[0]['activity-participation'])
            // console.log(d)
            console.log(__filename);

            cld.writeFile(output, './output/CMIP6Plus_source-id.json')
        })

    // .then(file=>
    //     console.log(file[4])
    // )





}

main()