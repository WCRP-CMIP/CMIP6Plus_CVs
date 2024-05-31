

// Load the jsonld.js library
const cld = require('cmip_jld');

// push each function into the global scope
Object.keys(cld).forEach(key => {
  global[key] = cld[key];
});



async function main() {
  try {


    // Read graph data
    const graphData = await readFileFS('./graph_data.min.json');
    const contextData = await readFileFS('./context_data.json');



    console.warn('-----------------------')


    const mapframe = {
      // "@context": 
      //   { "@vocab": "experiment-id:"
      // },

      "@type": "cmip:experiment_id",
      "@explicit": false,
      "experiment-id:model_components": { "experiment-id:additional_allowed": { "@explicit": true, "source-type:name": "" } ,
      "experiment-id:required": { "experiment-id:additional_allowed": { "@explicit": true, "source-type:name": "" } }
    }

    };



    jsonld.frame(graphData, mapframe)
      .then(graphOnly)
      // .then(cld.printState)
      .then(stringify)
      .then(untag)
      .then(rmld)
      .then(flatten)
      .then(str2JSON)
      // .then(cld.printState)
      .then(d => {
        console.log(d[4]['model_components'])

      })



  } catch (error) {
    console.error('Error:', error);
  }


}

main();
