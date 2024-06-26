export const AWSDEV='https://13.60.18.208:5000/'
const AWSDOMAIN= 'http://devs-md.com/5000'
export const AWSPROD='https://16.171.19.211:5000/'
export const VERCEL= 'https://marketsdojo.vercel.app/'

const PRODSERVER= "https://mdprodserver.com:5000/"
const DEVSERVER= "https://mddevelopmentserver.com:5000/"

 export const BASE_URL = PRODSERVER;
 export const ENDPOINT = {
  REGISTER: 'v1/users',
  LOGIN: 'v1/users/login',
  PORTFOLIO: "v1/users/portfolio",
  BUY_SELL:'v1/users/history',

  PRODUCTLIST:'v1/api/product_list',
  ASSETSLIST:'v1/api/assets_list',

};
//  export const ENDPOINT = {
//     REGISTER: 'v1/api/register',
//     LOGIN: 'v1/api/login',
//     PORTFOLIO: 'v1/api/portfolio',
//     BUY:'v1/api/buy',
//     SELL:'v1/api/sell',
//     PRODUCTLIST:'v1/api/product_list',
//     ASSETSLIST:'v1/api/assets_list',

// };

 export const FMPENDPOINT = {
    MARKETOPEN: 'v3/is-the-market-open',
    FOREXNEWS:  'v4/forex_news?page=0&apikey=',
    STOCKDATA:  'v3/quote/AAPL?apikey=',

};
export const STOCKNEWSENDPOINT = {
  NEWS: 'v1?tickers=',
};
export const FMPAPIURL='https://financialmodelingprep.com/api/'
export const STOCKNEWSAPIURL='https://stocknewsapi.com/api/'
export const FMPAPIKEY = '6fbceaefb411ee907e9062098ef0fd66'
export const NEWSAPIKEY = 'qvgfptpokzmfkdag1opnwj9c2svtukxyseprol1n'
export const SETTING = {
  CURRENCY: '$',
  INITIALSYMBOL: "AAPL"
};

export const SWA='https://virtserver.swaggerhub.com/ARMANJASUJA_1/marketsdojo/'
export const COMANYWEBSOCKET= 'wss://websockets.financialmodelingprep.com'
export const STOCKLIST="v3/quote/AAPL,META,GOOG,AMZN,TSLA,MSFT,NVDA, HSBC, LLY,TSM,AVGO, JPM, UNH, WMT, MA, XOM, JNJ, ASML,PG, HD";
export const CRYPTOLIST= "v3/quote/ETH,SOL,BTCUSD,BTC";
