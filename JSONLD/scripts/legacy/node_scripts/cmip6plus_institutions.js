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

    // './compiled/graph_data.json');

    // if using directly, do not remove graph, else remove graph in parsing. 

    // console.log(await Promise.all([cmip6plusData, mipData]))


    // console.log(await mipData)

    


    const frame = {
        "@context": {
            "debugid": "@id",
        },



        "@type": ["mip:source-id"],
        "source-id:organisation-id": {
            "@type": ["mip:institution", "mip:consortium"],
            "@explicit": true,

            "consortium:cmip_acronym": "",
            "institution:cmip_acronym": "",
            "consortium:description": "",
            "institution:name": "",
            "institution:ror": "",
            "consortium:members":
            {
                "institution:institution": { "debugid": {},"@explicit":false },
                "@explicit": true
            },

        },
        "@explicit": true,
    }





    jsonld.frame(graphData, frame)
        // .then(cld.printState)
        .then(graphOnly)
        .then(cld.stringify)
        
        .then(cld.rmld)
        .then(cld.rmnull)
    
        .then(cld.untag)
        // .then(cld.printState)
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

            // console.log(d)
            console.log(__filename);

            cld.writeFile(output, './output/CMIP6Plus_organisations.json')
        })

    // .then(file=>
    //     console.log(file[4])
    // )


}

main()