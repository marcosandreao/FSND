/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'https://coffee-shop-maao.herokuapp.com', // the running FLASK api server url
  auth0: {
    url: 'maao.us', // the auth0 domain prefix
    audience: 'dev', // the audience set for the auth0 app
    clientId: 'ARJMsoX5bPaLBg2TpBQ5KUvm10r4Kpbt', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
