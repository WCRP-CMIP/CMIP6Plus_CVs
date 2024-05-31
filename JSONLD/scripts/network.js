
// Load the jsonld.js library
const cld = require('cmip_jld');

// push each function into the global scope
Object.keys(cld).forEach(key => {
  global[key] = cld[key];
});



async function main() {
  try {


    // Read graph data
    const jsonldData = await readFileFS('./graph_data.min.json');
    rdf = await jsonld.toRDF(jsonldData)

    filtered = rdf.filter(
        (d) =>
        //   (d.subject.termType === d.object.termType) &
          (d.object.termType === "NamedNode") 
        
      )


    console.log(filtered.length)

    // overview for description
    csv = 'source,target,link\n'
    filtered.forEach(d=>{

        if ((d.graph.value) 
        //     & (d.predicate.value != 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
        )
            csv+=`"${d.graph.value}","${d.object.value.substring(0, d.object.value.lastIndexOf("/")).replace('mip-cmor-tables:','https://github.com/PCMDI/mip-cmor-tables/blob/main/JSONLD/').replace('cmip6plus:','https://github.com/WCRP-CMIP/CMIP6Plus_CVs/blob/main/JSONLD/')}","${d.predicate.value}"\n`

    })

   console.log(csv)
    
   const fs = require('fs');


   
   // Write data to the file
   fs.writeFile(filePath='./links.csv', csv, (err) => {
     if (err) {
       console.error('Error writing to file:', err);
       return;
     }
     console.log('Data has been written to', filePath);
   });



  }catch(err){
    console.log(err)
  }
}

main()