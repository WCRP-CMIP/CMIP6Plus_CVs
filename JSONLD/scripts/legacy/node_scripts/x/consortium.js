// // Load the jsonld.js library
// const cld = require('cmip_jld');
// const { flatten } = require('jsonld/lib/flatten');

// // push each function into the global scope
// Object.keys(cld).forEach(key => {
//     global[key] = cld[key];
// });


// async function main() {

//     const graphData = await readFileFS('../organisations/consortia/graph.jsonld');

//     const frame = {
//         "@context": {
//         },
//         "@type": "consortium",
//         "explicit": true,
//         "consortium:cmip_acronym": "",
//         "consortium:description": "",
//         "consortium:url": "",
//         "consortium:members": {
//             "@explicit": true,
//             "consortia:institution": {
//                 "@explicit": true,
//                 // "institution:name":"",
//                 "refid": "@id"
//             }


//         }
//     }


//     jsonld.frame(graphData, frame)
//         // .then(graphOnly)
//         .then(cld.stringify)
//         .then(cld.flatten)
//         .then(cld.rmld)
//         .then(cld.untag)
//         .then(str2JSON)
//         .then(cld.printState)
//         .then(d => {
//             cld.writeFile(d, './output/consortia.json')
//         })

//     // .then(file=>
//     //     console.log(file[4])
//     // )





// }

// main()