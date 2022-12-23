/**
 * Reviews API
 */

/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */


//const selector: CloudantV1.JsonObject =  {   "state": {     "$eq": state   }};
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
async function main(params) {
  const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
  const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
  });
  cloudant.setServiceUrl(params.URL);
  //console.log("params:",Object.keys(params));      
  //console.log("method:",params.__ow_method);
   
 try {
    
     
    if (params.__ow_method.toUpperCase()=='GET' && params.id) return getReviews(cloudant,params.id); 
    
    if (params.__ow_method.toUpperCase()=='POST' && params.review ) return postOne(cloudant,params.review.review);
    
    // Test
    //return getReviews(cloudant,"15");
    //return postOne(cloudant,test_review.review);
    
    let body= { method: params.__ow_method, action:'no op' };
    let headers= { 'Content-Type': 'application/json' };
    return  {statusCode:200,headers,body};
    
    
  } catch (error)
  
  {
      return { error: error.description };
  }
}

async function getReviews(cloudant, dealership){

let selector = {   "dealership": {     "$eq": parseInt(dealership)   }};

let query =  await cloudant.postFind({ db: 'reviews', selector});

console.log("query:",Object.keys(query));  
console.log("getReviews length:", query.result.docs.length);

let statusCode=200;
if ( query.result.docs.length==0) statusCode=404;

let body= { statusCode ,'length': query.result.docs.length, 'filter':selector, reviews:query.result.docs };
 
let headers= { 'Content-Type': 'application/json' };
return  {statusCode,headers,body};
}

test_review= {
  "review": 
      {
          "id": 1114,
          "name": "Upkar Lidder",
          "dealership": 15,
          "review": "Great service!",
          "purchase": false,
          "another": "field",
          "purchase_date": "02/16/2021",
          "car_make": "Audi",
          "car_model": "Car",
          "car_year": 2021
      }
  };


async function postOne(cloudant,review){

let query =  await cloudant.postDocument({ db: 'reviews',document:review});

//console.log("query:",Object.keys(query.result));  //'status', 'statusText', 'headers', 'result'

let statusCode=200;
body={'status':query.status, 'result':query.result};   
let headers= { 'Content-Type': 'application/json' };
return  {statusCode,headers,body};
}