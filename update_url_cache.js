const fs = require('fs');
const path = require('path');

// Read existing url_cache.json
let urlCache = {};
try {
  const urlCacheContent = fs.readFileSync('url_cache.json', 'utf8');
  urlCache = JSON.parse(urlCacheContent);
  console.log(`Loaded existing url_cache.json with ${Object.keys(urlCache).length} entries`);
} catch (err) {
  console.log('Creating new url_cache.json file');
}

// Parse the intercepted URLs from the logs
const urlsToAdd = [
  {
    key: '51240228517882000186550010000090161000270486',
    url: 'https://www.nfe.fazenda.gov.br/portal/downloadNFe.aspx?tipoConsulta=resumo&a=yT9JRhNinH0tupr3EH6g/ZGaMAykoSAS5IWG395BLrYG5oDip8S+Ub6bxFrvUheS&tipoConteudo=7PhJ%20gAVw2g=&lp=eVQ5SlJoTmluSDB0dXByM0VINmcvWkdhTUF5a29TQVM1SVdHMzk1QkxyWUc1b0RpcDhTK1VSbVhidExQM1VaU0t2RjBjbEFvSXN0Z1ViZ3Q5WkZyMmp4TVhMajcxbWhkcU1iYU1rME9SQkk90'
  },
  {
    key: '51240228517882000186550010000090221000270661',
    url: 'https://www.nfe.fazenda.gov.br/portal/downloadNFe.aspx?tipoConsulta=resumo&a=yT9JRhNinH0tupr3EH6g/ZGaMAykoSAS5IWG395BLrat3HzuLc+kdcWq7qx+EgEt&tipoConteudo=7PhJ%20gAVw2g=&lp=eVQ5SlJoTmluSDB0dXByM0VINmcvWkdhTUF5a29TQVM1SVdHMzk1QkxyYXQzSHp1TGMra2RXMUU4clo0SEU2eUlWYjZZVlU0VjdFL0M3MjB5VzR6ZWpiSEEwamZpZDFDSGprS28vU2F6dXM90'
  },
  {
    key: '51240228517882000186550010000090231000270693',
    url: 'https://www.nfe.fazenda.gov.br/portal/downloadNFe.aspx?tipoConsulta=resumo&a=yT9JRhNinH0tupr3EH6g/ZGaMAykoSAS5IWG395BLratI+WShtKguJsaYB8V2pOi&tipoConteudo=7PhJ%20gAVw2g=&lp=eVQ5SlJoTmluSDB0dXByM0VINmcvWkdhTUF5a29TQVM1SVdHMzk1QkxyYXRJK1dTaHRLZ3VJZFdiTnQ3TUVMRCtQOVFMejZ6ZENocHhtaWVrb3NJemQ0a3VWRXhTdkhKNWs5V2lkRjF1MzA90'
  },
  {
    key: '51240228517882000186550010000090251000270752',
    url: 'https://www.nfe.fazenda.gov.br/portal/downloadNFe.aspx?tipoConsulta=resumo&a=yT9JRhNinH0tupr3EH6g/ZGaMAykoSAS5IWG395BLrbJkZJ+ZLD9685k3TgQcwi0&tipoConteudo=7PhJ%20gAVw2g=&lp=eVQ5SlJoTmluSDB0dXByM0VINmcvWkdhTUF5a29TQVM1SVdHMzk1QkxyYkprWkorWkxEOTZ6QWxjZXB4Y01XTGpEN09YQjBMRVFpaU9WN1BXWldlV1RteUh2TENvUS9zRmxtOGwvOHFqTnc90'
  },
  {
    key: '51240228517882000186550010000090371000271113',
    url: 'https://www.nfe.fazenda.gov.br/portal/downloadNFe.aspx?tipoConsulta=resumo&a=yT9JRhNinH0tupr3EH6g/ZGaMAykoSAS5IWG395BLrZNWAkHcqPOYtX6AYEowi1F&tipoConteudo=7PhJ%20gAVw2g=&lp=eVQ5SlJoTmluSDB0dXByM0VINmcvWkdhTUF5a29TQVM1SVdHMzk1QkxyWk5XQWtIY3FQT1lvemhBYVh0NHo3SXEzdTZtUTVJcHo4eDE2VTFTaXRka2ZCZUJPVEZScXptS01sN2xjQUd1ZTA90'
  },
  {
    key: '51240228517882000186550010000090181000270545',
    url: 'https://www.nfe.fazenda.gov.br/portal/downloadNFe.aspx?tipoConsulta=resumo&a=yT9JRhNinH0tupr3EH6g/ZGaMAykoSAS5IWG395BLrYR4+BUF5hY2SZbq+8EVPq8&tipoConteudo=7PhJ%20gAVw2g=&lp=eVQ5SlJoTmluSDB0dXByM0VINmcvWkdhTUF5a29TQVM1SVdHMzk1QkxyWVI0K0JVRjVoWTJSVHdrWmRQeE5MMnFaUFlQdERqY1ljYnAwR2QvMzB4U051aHptUmxEeXdWRm9jaVFNVkZXTDQ90'
  }
];

// Add the new URLs to the cache
const timestamp = new Date().toISOString();
for (const item of urlsToAdd) {
  if (!urlCache[item.key]) {
    urlCache[item.key] = {
      url: item.url,
      timestamp: timestamp
    };
    console.log(`Added URL for key: ${item.key}`);
  } else {
    console.log(`URL for key ${item.key} already exists in cache`);
  }
}

// Save the updated cache back to file
fs.writeFileSync('url_cache.json', JSON.stringify(urlCache, null, 4));
console.log(`Updated url_cache.json with ${Object.keys(urlCache).length} total entries`);

// Create a backup of the original file
try {
  fs.copyFileSync('url_cache.json', 'url_cache.json.backup');
  console.log('Created backup of original file at url_cache.json.backup');
} catch (err) {
  console.error('Failed to create backup:', err);
} 