/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
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
      // method = params.__ow_method;
        
      try {  
          
         if (params.state) {  return getState(cloudant,params.state)}
         if (params.id) {  return getOne(cloudant,params.id)}
         return getAll(cloudant)
 
        // return getAll(cloudant);
         
         
       } catch (error)
       
       {
           return { error: error.description };
       }
 }
 
 async function getState(cloudant,state){
 
     let selector = {   "state": {     "$eq": state   }};
     
     let query =  await cloudant.postFind({ db: 'dealerships', selector});
     
     console.log("query:",Object.keys(query));  
     
     console.log("filterState .total_rows:", query.result.docs.length);
     let statusCode=200;
     if ( query.result.docs.length==0) statusCode=404;
     
     let body= { statusCode ,'length': query.result.docs.length, 'filter':selector, dealerships:query.result.docs };
        
         
     let headers= { 'Content-Type': 'application/json' };
     return  {statusCode,headers,body};
 }
 
 async function getOne(cloudant,id){
 
     let selector = {   "id": {     "$eq": parseInt(id)   }};
     
     let query =  await cloudant.postFind({ db: 'dealerships', selector});
     
     console.log("query:",Object.keys(query));  
     
     console.log("filterState length:", query.result.docs.length);
     
     let statusCode=200;
     if ( query.result.docs.length==0) statusCode=404;
     
     let body= {statusCode, 'length': query.result.docs.length, 'filter':selector, dealerships:query.result.docs };
          
         
     let headers= { 'Content-Type': 'application/json' };
     return  {statusCode,headers,body};
 }
 
 
 async function getAll(cloudant){
     
     let query = await cloudant.postAllDocs({  db: 'dealerships' ,includeDocs: true});        
     
     let statusCode=200;
     if ( query.result.rows.length==0) statusCode=404;
     let items  = query.result.docs.map(e=>  e.doc);     
     let body= { statusCode ,'length': query.result.rows.length, dealerships:items };
     
     //let body= { statusCode, 'length': query.result.rows.length , dealerships:query.result.rows};
     let headers= { 'Content-Type': 'application/json' };
     return  {statusCode,headers,body};
 }          
           
 