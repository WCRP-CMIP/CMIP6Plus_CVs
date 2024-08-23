// Load the jsonld.js library
const cld = require('cmip_jld');

// push each function into the global scope
Object.keys(cld).forEach(key => {
    global[key] = cld[key];
});


async function main() {

    const graphData = await readFileFS('./compiled/data_request.min.json');

    const frame = {
        "@type": "cmip:dr-table"
    }


    jsonld.frame(graphData,frame)
        // .then(graphOnly)
        .then(cld.printState)
        .then(file=>
            console.log(file[4])
        )





}

main()