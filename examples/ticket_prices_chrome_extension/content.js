const FROM_EMAIL = '' 
const TO_EMAIL = '' 
const EMAIL_API_KEY = ''

function sendElasticEmail(subject, body) {
    // mock email if email client isn't set up yet
    //if (typeof EMAIL_API_KEY == 'undefined') {
    //  console.log(`sendElasticEmail mock: subject: ${subject}, body: ${body}`);
    //  return;
    //}

    const params = new URLSearchParams();
    params.append('apikey', EMAIL_API_KEY);
    params.append('subject', subject);
    params.append('from', FROM_EMAIL); 
    params.append('to', TO_EMAIL);
    params.append('bodyHtml', body);
    params.append('isTransactional', true);
  
    fetch('https://api.elasticemail.com/v2/email/send', {
      method: 'POST',
      body: params
    })
    .then(response => response.json())
    .then(data => {
      console.log('Email sent successfully:', data);
    })
    .catch(error => {
      console.error('Error sending email:', error);
    });
  }

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "findPrices") {
        console.log("findPrices called")

        setInterval(function() {
          const button = document.getElementById('quickpick-buy-button-qp-0');
          if (button) {
            let parts = button.innerHTML.split('$');
            let numericPart = parts[1];
            let price = Number(numericPart);
            if (price < 275) {
              sendElasticEmail('Price update', `New price is: ${price}`);
            }
          } else {
            console.log('Button not found');
          }
      }, 10000); // 10K milliseconds = 10 seconds
    }
});
