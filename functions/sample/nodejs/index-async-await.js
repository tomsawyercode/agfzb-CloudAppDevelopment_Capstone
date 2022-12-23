/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');


async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(params.URL);
       console.log("params:",Object.keys(params));

      try {
        let query = await cloudant.postAllDocs({  db: 'dealerships' ,includeDocs: true})        
        console.log("dealerships",query.result.rows.length)
        //return { "dealerships": query.result}
        //return { "dealerships": query.result.rows}
        return { "dealerships": query.result.rows.map((r) => { return r.doc }) };
      } catch (error) {
          return { error: error.description };
      }
}