# Source: https://developer.adobe.com/firefly-services/docs/firefly-api/guides/

[**Adobe Developer**](/)

[Products](/apis/)

[Products](/apis/)

[ All Firefly Services ](/firefly-services/docs/guides/)[ Firefly API ](/firefly-services/docs/firefly-api/)[ Photoshop API ](https://developer.adobe.com/firefly-services/docs/photoshop/?aio%5Finternal)[ Lightroom API ](/firefly-services/docs/lightroom/)[ Audio/Video API ](https://developer.adobe.com/audio-video-firefly-services/?aio%5Finternal)[ InDesign API ](/firefly-services/docs/indesign-apis/)[ Substance 3D API ](https://developer.adobe.com/firefly-services/docs/s3dapi/?aio%5Finternal)[ Content Tagging API ](https://experienceleague.adobe.com/docs/experience-platform/intelligent-services/content-commerce-ai/overview.html)

[Console](/console)

Sign in

---

[Edit Profile](https://account.adobe.com/)Sign out

* [Overview](/firefly-services/docs/firefly-api/)
* [Quickstart](/firefly-services/docs/firefly-api/guides/)
* [Concepts](/firefly-services/docs/firefly-api/guides/concepts/authentication/)  
   * [Adobe Developer Console](/firefly-services/docs/firefly-api/guides/concepts/dev-console/)  
   * [Authentication](/firefly-services/docs/firefly-api/guides/concepts/authentication/)  
   * [Image Upload](/firefly-services/docs/firefly-api/guides/concepts/image-upload/)  
   * [Masking](/firefly-services/docs/firefly-api/guides/concepts/masking/)  
   * [Placement](/firefly-services/docs/firefly-api/guides/concepts/placement/)  
   * [Rate limits](/firefly-services/docs/firefly-api/guides/concepts/rate-limits/)  
   * [Seeds](/firefly-services/docs/firefly-api/guides/concepts/seeds/)  
   * [Structure Image Reference](/firefly-services/docs/firefly-api/guides/concepts/structure-image-reference/)  
   * [Style Image Reference](/firefly-services/docs/firefly-api/guides/concepts/style-image-reference/)  
   * [Style Presets](/firefly-services/docs/firefly-api/guides/concepts/style-presets/)  
   * [Custom Models](/firefly-services/docs/firefly-api/guides/concepts/custom-models/)
* [How-Tos](/firefly-services/docs/firefly-api/guides/how-tos/firefly-generate-image-api-tutorial/)  
   * [Generate Image API Tutorial](/firefly-services/docs/firefly-api/guides/how-tos/firefly-generate-image-api-tutorial/)  
   * [Generate Image from Custom Model Tutorial](/firefly-services/docs/firefly-api/guides/how-tos/cm-generate-image/)  
   * [Expand Image API Tutorial](/firefly-services/docs/firefly-api/guides/how-tos/firefly-expand-image-api-tutorial/)  
   * [Fill Image API Tutorial](/firefly-services/docs/firefly-api/guides/how-tos/firefly-fill-image-api-tutorial/)  
   * [Grant Access to a Custom Model](/firefly-services/docs/firefly-api/guides/how-tos/cm-share-model/)  
   * [Using the Firefly Asynchronous APIs](/firefly-services/docs/firefly-api/guides/how-tos/using-async-apis/)
* [API Reference](/firefly-services/docs/firefly-api/guides/api/image%5Fgeneration/V3/)  
   * [List Custom Models](/firefly-services/docs/firefly-api/guides/api/list%5Fcustom%5Fmodels/)  
   * [Generate Images](/firefly-services/docs/firefly-api/guides/api/image%5Fgeneration/V3/)  
         * [V3 async](/firefly-services/docs/firefly-api/guides/api/image%5Fgeneration/V3%5FAsync/)  
         * [V3 (deprecated)](/firefly-services/docs/firefly-api/guides/api/image%5Fgeneration/V3/)  
   * [Generate Similar Images](/firefly-services/docs/firefly-api/guides/api/generate-similar/V3/)  
         * [V3 async](/firefly-services/docs/firefly-api/guides/api/generate-similar/V3%5FAsync/)  
         * [V3 (deprecated)](/firefly-services/docs/firefly-api/guides/api/generate-similar/V3/)  
   * [Generate Object Composite](/firefly-services/docs/firefly-api/guides/api/generate-object-composite/V3/)  
         * [V3 async](/firefly-services/docs/firefly-api/guides/api/generate-object-composite/V3%5FAsync/)  
         * [V3 (deprecated)](/firefly-services/docs/firefly-api/guides/api/generate-object-composite/V3/)  
   * [Expand Image](/firefly-services/docs/firefly-api/guides/api/generative%5Fexpand/V3/)  
         * [V3 async](/firefly-services/docs/firefly-api/guides/api/generative%5Fexpand/V3%5FAsync/)  
         * [V3 (deprecated)](/firefly-services/docs/firefly-api/guides/api/generative%5Fexpand/V3/)  
   * [Fill Image](/firefly-services/docs/firefly-api/guides/api/generative%5Ffill/V3/)  
         * [V3 async](/firefly-services/docs/firefly-api/guides/api/generative%5Ffill/V3%5FAsync/)  
         * [V3 (deprecated)](/firefly-services/docs/firefly-api/guides/api/generative%5Ffill/V3/)  
   * [Upload](/firefly-services/docs/firefly-api/guides/api/upload%5Fimage/V2/)  
         * [V2](/firefly-services/docs/firefly-api/guides/api/upload%5Fimage/V2/)  
   * [Generate Video](/firefly-services/docs/firefly-api/guides/api/generate%5Fvideo/V3%5FAsync/)  
         * [V3 async](/firefly-services/docs/firefly-api/guides/api/generate%5Fvideo/V3%5FAsync/)
* [Changelog](/firefly-services/docs/firefly-api/guides/changelog/)
* [Help](/firefly-services/docs/firefly-api/guides/help/best-practices/)  
   * [Best Practices](/firefly-services/docs/firefly-api/guides/help/best-practices/)  
   * [Troubleshooting](/firefly-services/docs/firefly-api/guides/help/troubleshooting/)  
   * [Usage Notes](/firefly-services/docs/firefly-api/guides/help/usage%5Fnotes/)

[Edit in GitHub](https://github.com/AdobeDocs/ff-services-docs/edit/main/src/pages/firefly-api/guides/index.md)[Log an issue](https://github.com/AdobeDocs/ff-services-docs/issues/new?title=Issue%20in%20/src/pages/firefly-api/guides/index.md)

# Quickstart Guide

Generate your first image with Firefly Services

![an illustration of a cat coding on a laptop](/firefly-services/docs/static/82044b6fe3cf44ec68c4872f784cd82d/62aaf/cat-coding.jpg "an illustration of a cat coding on a laptop") 

## Prerequisites

---

### Credentials

If you don't already have a Firefly API or Firefly Services **Client ID** and **Client Secret**, retrieve them from your [Adobe Developer Console project](https://developer.adobe.com/developer-console/docs/guides/services/services-add-api-oauth-s2s/#api-overview) before reading further. **Securely store these credentials and never expose them in client-side or public code.**

### Set Up Your Environment

Before we begin this tutorial, run the following in a secure terminal:

JavaScript

Python

Copy

mkdir firefly-api-generate-images-tutorial
cd firefly-api-generate-images-tutorial
npm init --y
npm install axios qs
touch index.js
Copied to your clipboard

mkdir firefly-api-generate-images-tutorial

cd firefly-api-generate-images-tutorial

npm init --y

npm install axios qs

touch index.js

Copy

mkdir firefly-api-generate-images-tutorial
cd firefly-api-generate-images-tutorial
python -m pip install requests
touch main.py
Copied to your clipboard

mkdir firefly-api-generate-images-tutorial

cd firefly-api-generate-images-tutorial

python -m pip install requests

touch main.py

Depending on your learning style, you may prefer to walk through this tutorial step-by-step or [jump immediately to the full source code](/firefly-services/docs/firefly-api/guides/#full-example).

## Retrieve an Access Token

---

Open a secure terminal and `export` your **Client ID** and **Client Secret** as environment variables so that your later commands can access them:

Copy

export FIREFLY_SERVICES_CLIENT_ID=yourClientIdAsdf123
export FIREFLY_SERVICES_CLIENT_SECRET=yourClientSecretAsdf123
Copied to your clipboard

export FIREFLY_SERVICES_CLIENT_ID=yourClientIdAsdf123

export FIREFLY_SERVICES_CLIENT_SECRET=yourClientSecretAsdf123

Generate an access token:

cURL

Python

JavaScript

Copy

curl --location 'https://ims-na1.adobelogin.com/ims/token/v3' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=client_credentials' \
--data-urlencode "client_id=$FIREFLY_SERVICES_CLIENT_ID" \
--data-urlencode "client_secret=$FIREFLY_SERVICES_CLIENT_SECRET" \
--data-urlencode 'scope=openid,AdobeID,session,additional_info,read_organizations,firefly_api,ff_apis'
Copied to your clipboard

curl --location 'https://ims-na1.adobelogin.com/ims/token/v3' \

--header 'Content-Type: application/x-www-form-urlencoded' \

--data-urlencode 'grant_type=client_credentials' \

--data-urlencode "client_id=$FIREFLY_SERVICES_CLIENT_ID" \

--data-urlencode "client_secret=$FIREFLY_SERVICES_CLIENT_SECRET" \

--data-urlencode 'scope=openid,AdobeID,session,additional_info,read_organizations,firefly_api,ff_apis'

Copy

def retrieve_access_token():
    client_id = os.environ['FIREFLY_SERVICES_CLIENT_ID']
    client_secret = os.environ['FIREFLY_SERVICES_CLIENT_SECRET']

    token_url = 'https://ims-na1.adobelogin.com/ims/token/v3'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'openid,AdobeID,session,additional_info,read_organizations,firefly_api,ff_apis'
    }

    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    token_data = response.json()
    print("Access Token Retrieved")
    return token_data['access_token']
Copied to your clipboard

def retrieve_access_token():

    client_id = os.environ['FIREFLY_SERVICES_CLIENT_ID']

    client_secret = os.environ['FIREFLY_SERVICES_CLIENT_SECRET']


    token_url = 'https://ims-na1.adobelogin.com/ims/token/v3'

    payload = {

        'grant_type': 'client_credentials',

        'client_id': client_id,

        'client_secret': client_secret,

        'scope': 'openid,AdobeID,session,additional_info,read_organizations,firefly_api,ff_apis'

    }


    response = requests.post(token_url, data=payload)

    response.raise_for_status()

    token_data = response.json()

    print("Access Token Retrieved")

    return token_data['access_token']

Copy

async function retrieveAccessToken() {
  const data = qs.stringify({
    grant_type: 'client_credentials',
    client_id: process.env.FIREFLY_SERVICES_CLIENT_ID,
    client_secret: process.env.FIREFLY_SERVICES_CLIENT_SECRET,
    scope: 'openid,AdobeID,session,additional_info,read_organizations,firefly_api,ff_apis',
  });

  const config = {
    method: 'post',
    url: 'https://ims-na1.adobelogin.com/ims/token/v3',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    data: data,
  };

  try {
    const response = await axios.request(config);
    console.log('Access Token Retrieved');
    return response.data.access_token;
  } catch (error) {
    console.error('Error retrieving access token:', error.response.data);
  }
}
Copied to your clipboard

async function retrieveAccessToken() {

  const data = qs.stringify({

    grant_type: 'client_credentials',

    client_id: process.env.FIREFLY_SERVICES_CLIENT_ID,

    client_secret: process.env.FIREFLY_SERVICES_CLIENT_SECRET,

    scope: 'openid,AdobeID,session,additional_info,read_organizations,firefly_api,ff_apis',

  });


  const config = {

    method: 'post',

    url: 'https://ims-na1.adobelogin.com/ims/token/v3',

    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },

    data: data,

  };


  try {

    const response = await axios.request(config);

    console.log('Access Token Retrieved');

    return response.data.access_token;

  } catch (error) {

    console.error('Error retrieving access token:', error.response.data);

  }

}

The response will look like this:

Copy

{"access_token":"yourAccessTokenAsdf123","token_type":"bearer","expires_in":86399}
Copied to your clipboard

{"access_token":"yourAccessTokenAsdf123","token_type":"bearer","expires_in":86399}

Export this access token so that the next script can conveniently access it:

Copy

export FIREFLY_SERVICES_ACCESS_TOKEN=yourAccessTokenAsdf123
Copied to your clipboard

export FIREFLY_SERVICES_ACCESS_TOKEN=yourAccessTokenAsdf123

## Generate an Image

---

Next, call the [Firefly Generate Images API](/firefly-services/docs/firefly-api/guides/api/image%5Fgeneration/V3/):

cURL

Python

JavaScript

Copy

curl --location 'https://firefly-api.adobe.io/v3/images/generate' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--header "x-api-key: $FIREFLY_SERVICES_CLIENT_ID" \
--header "Authorization: Bearer $FIREFLY_SERVICES_ACCESS_TOKEN" \
--data '{
    "prompt": "a realistic illustration of a cat coding"
}'
Copied to your clipboard

curl --location 'https://firefly-api.adobe.io/v3/images/generate' \

--header 'Content-Type: application/json' \

--header 'Accept: application/json' \

--header "x-api-key: $FIREFLY_SERVICES_CLIENT_ID" \

--header "Authorization: Bearer $FIREFLY_SERVICES_ACCESS_TOKEN" \

--data '{

    "prompt": "a realistic illustration of a cat coding"

}'

Copy

def generate_image(access_token):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-api-key': os.environ['FIREFLY_SERVICES_CLIENT_ID'],
        'Authorization': f'Bearer {access_token}'
    }

    data = {
        'prompt': 'a realistic illustration of a cat coding',  # Replace with your actual prompt
    }

    response = requests.post(
        'https://firefly-api.adobe.io/v3/images/generate',
        headers=headers,
        json=data
    )
    response.raise_for_status()
    job_response = response.json()
    print("Generate Image Response:", job_response)
    return job_response
Copied to your clipboard

def generate_image(access_token):

    headers = {

        'Content-Type': 'application/json',

        'Accept': 'application/json',

        'x-api-key': os.environ['FIREFLY_SERVICES_CLIENT_ID'],

        'Authorization': f'Bearer {access_token}'

    }


    data = {

        'prompt': 'a realistic illustration of a cat coding',  # Replace with your actual prompt

    }


    response = requests.post(

        'https://firefly-api.adobe.io/v3/images/generate',

        headers=headers,

        json=data

    )

    response.raise_for_status()

    job_response = response.json()

    print("Generate Image Response:", job_response)

    return job_response

Copy

async function generateImage(accessToken) {
  const headers = {
    "Content-Type": "application/json",
    Accept: "application/json",
    "x-api-key": process.env.FIREFLY_SERVICES_CLIENT_ID,
    Authorization: `Bearer ${accessToken}`,
  };

  const data = {
    prompt: "a realistic illustration of a cat coding", // Replace with your actual prompt
  };

  const config = {
    method: "post",
    url: "https://firefly-api.adobe.io/v3/images/generate",
    headers: headers,
    data: data,
  };

  try {
    const response = await axios.request(config);
    return response.data;
  } catch (error) {
    console.error("Error during generateImage:", error);
  }
}
Copied to your clipboard

async function generateImage(accessToken) {

  const headers = {

    "Content-Type": "application/json",

    Accept: "application/json",

    "x-api-key": process.env.FIREFLY_SERVICES_CLIENT_ID,

    Authorization: `Bearer ${accessToken}`,

  };


  const data = {

    prompt: "a realistic illustration of a cat coding", // Replace with your actual prompt

  };


  const config = {

    method: "post",

    url: "https://firefly-api.adobe.io/v3/images/generate",

    headers: headers,

    data: data,

  };


  try {

    const response = await axios.request(config);

    return response.data;

  } catch (error) {

    console.error("Error during generateImage:", error);

  }

}

The response will look like this:

Copy

{
    "size": {
        "width": 2048,
        "height": 2048
    },
    "outputs": [
        {
            "seed": 1779323515,
            "image": {
                "url": "https://pre-signed-firefly-prod.s3-accelerate.amazonaws.com/images/asdf-12345?lots=of&query=params..."
            }
        }
    ],
    "contentClass": "art"
}
Copied to your clipboard

{

    "size": {

        "width": 2048,

        "height": 2048

    },

    "outputs": [

        {

            "seed": 1779323515,

            "image": {

                "url": "https://pre-signed-firefly-prod.s3-accelerate.amazonaws.com/images/asdf-12345?lots=of&query=params..."

            }

        }

    ],

    "contentClass": "art"

}

## View the Generated Image

---

Open the URL in your browser to see the image you generated with Firefly 🎉

## Full Example

---

You can review the [prerequisites](/firefly-services/docs/firefly-api/guides/#prerequisites) section to understand how to set up your environment prior to running this code. Note that this is an example only and is not production-ready and requires additional error handling, logging, security measures, and more before you can run it at scale in a live application.

Python

JavaScript

Copy

import os
import requests

def main():
    access_token = retrieve_access_token()
    generate_image(access_token)

def retrieve_access_token():
    client_id = os.environ['FIREFLY_SERVICES_CLIENT_ID']
    client_secret = os.environ['FIREFLY_SERVICES_CLIENT_SECRET']

    token_url = 'https://ims-na1.adobelogin.com/ims/token/v3'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'openid,AdobeID,session,additional_info,read_organizations,firefly_api,ff_apis'
    }

    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    token_data = response.json()
    print("Access Token Retrieved")
    return token_data['access_token']

def generate_image(access_token):
    client_id = os.environ['FIREFLY_SERVICES_CLIENT_ID']

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-api-key': client_id,
        'Authorization': f'Bearer {access_token}'
    }

    data = {
        'prompt': 'a realistic illustration of a cat coding',  # Replace with your actual prompt
    }

    response = requests.post(
        'https://firefly-api.adobe.io/v3/images/generate',
        headers=headers,
        json=data
    )
    response.raise_for_status()
    job_response = response.json()
    print("Generate Image Response:", job_response)

    # Access the generated image URL
    image_url = job_response['outputs'][0]['image']['url']
    print(f"You can view the generated image at: {image_url}")

if __name__ == '__main__':
    main()
Copied to your clipboard

import os

import requests


def main():

    access_token = retrieve_access_token()

    generate_image(access_token)


def retrieve_access_token():

    client_id = os.environ['FIREFLY_SERVICES_CLIENT_ID']

    client_secret = os.environ['FIREFLY_SERVICES_CLIENT_SECRET']


    token_url = 'https://ims-na1.adobelogin.com/ims/token/v3'

    payload = {

        'grant_type': 'client_credentials',

        'client_id': client_id,

        'client_secret': client_secret,

        'scope': 'openid,AdobeID,session,additional_info,read_organizations,firefly_api,ff_apis'

    }


    response = requests.post(token_url, data=payload)

    response.raise_for_status()

    token_data = response.json()

    print("Access Token Retrieved")

    return token_data['access_token']


def generate_image(access_token):

    client_id = os.environ['FIREFLY_SERVICES_CLIENT_ID']


    headers = {

        'Content-Type': 'application/json',

        'Accept': 'application/json',

        'x-api-key': client_id,

        'Authorization': f'Bearer {access_token}'

    }


    data = {

        'prompt': 'a realistic illustration of a cat coding',  # Replace with your actual prompt

    }


    response = requests.post(

        'https://firefly-api.adobe.io/v3/images/generate',

        headers=headers,

        json=data

    )

    response.raise_for_status()

    job_response = response.json()

    print("Generate Image Response:", job_response)


    # Access the generated image URL

    image_url = job_response['outputs'][0]['image']['url']

    print(f"You can view the generated image at: {image_url}")


if __name__ == '__main__':

    main()

Copy

const axios = require('axios');
const qs = require('qs');

(async () => {
  const accessToken = await retrieveAccessToken();
  await generateImage(accessToken);
})();

async function retrieveAccessToken() {
  const data = qs.stringify({
    grant_type: 'client_credentials',
    client_id: process.env.FIREFLY_SERVICES_CLIENT_ID,
    client_secret: process.env.FIREFLY_SERVICES_CLIENT_SECRET,
    scope: 'openid,AdobeID,session,additional_info,read_organizations,firefly_api,ff_apis',
  });

  const config = {
    method: 'post',
    url: 'https://ims-na1.adobelogin.com/ims/token/v3',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    data: data,
  };

  try {
    const response = await axios.request(config);
    console.log('Access Token Retrieved');
    return response.data.access_token;
  } catch (error) {
    console.error('Error retrieving access token:', error.response.data);
  }
}

async function generateImage(accessToken) {
  const headers = {
    'Content-Type': 'application/json',
    Accept: 'application/json',
    'x-api-key': process.env.FIREFLY_SERVICES_CLIENT_ID,
    Authorization: `Bearer ${accessToken}`,
  };

  const data = {
    prompt: 'a realistic illustration of a cat coding', // Replace with your actual prompt
  };

  const config = {
    method: 'post',
    url: 'https://firefly-api.adobe.io/v3/images/generate',
    headers: headers,
    data: data,
  };

  try {
    const response = await axios.request(config);
    console.log('Generate Image Response:', response.data);

    // Access the generated image URL
    const imageUrl = response.data.outputs[0].image.url;
    console.log(`You can view the generated image at: ${imageUrl}`);
  } catch (error) {
    console.error('Error during generateImage:', error.response.data);
  }
}
Copied to your clipboard

const axios = require('axios');

const qs = require('qs');


(async () => {

  const accessToken = await retrieveAccessToken();

  await generateImage(accessToken);

})();


async function retrieveAccessToken() {

  const data = qs.stringify({

    grant_type: 'client_credentials',

    client_id: process.env.FIREFLY_SERVICES_CLIENT_ID,

    client_secret: process.env.FIREFLY_SERVICES_CLIENT_SECRET,

    scope: 'openid,AdobeID,session,additional_info,read_organizations,firefly_api,ff_apis',

  });


  const config = {

    method: 'post',

    url: 'https://ims-na1.adobelogin.com/ims/token/v3',

    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },

    data: data,

  };


  try {

    const response = await axios.request(config);

    console.log('Access Token Retrieved');

    return response.data.access_token;

  } catch (error) {

    console.error('Error retrieving access token:', error.response.data);

  }

}


async function generateImage(accessToken) {

  const headers = {

    'Content-Type': 'application/json',

    Accept: 'application/json',

    'x-api-key': process.env.FIREFLY_SERVICES_CLIENT_ID,

    Authorization: `Bearer ${accessToken}`,

  };


  const data = {

    prompt: 'a realistic illustration of a cat coding', // Replace with your actual prompt

  };


  const config = {

    method: 'post',

    url: 'https://firefly-api.adobe.io/v3/images/generate',

    headers: headers,

    data: data,

  };


  try {

    const response = await axios.request(config);

    console.log('Generate Image Response:', response.data);


    // Access the generated image URL

    const imageUrl = response.data.outputs[0].image.url;

    console.log(`You can view the generated image at: ${imageUrl}`);

  } catch (error) {

    console.error('Error during generateImage:', error.response.data);

  }

}

## Deepen Your Understanding

---

Visit the [Firefly Generate Image API tutorial](/firefly-services/docs/firefly-api/guides/how-tos/firefly-generate-image-api-tutorial/) to learn more about the rich customization options available to you 🚀

[Overview](/firefly-services/docs/firefly-api/)

[Concepts](/firefly-services/docs/firefly-api/guides/concepts/authentication/)

[![Archy Posada](https://github.com/archyposada.png)![Nimitha Jalal](https://github.com/nimithajalal.png)![Holly Schinsky](https://github.com/hollyschinsky.png)![Alexander Abreu](https://github.com/AEAbreu-hub.png)![bishoysefin](https://github.com/bishoysefin.png)Last updated 9/3/2025](https://github.com/AdobeDocs/ff-services-docs/commits/main/src/pages/firefly-api/guides/index.md)

Was this helpful?

Yes

No

#### On this page

1. [Prerequisites](#prerequisites)  
   * [Credentials](#credentials)  
   * [Set Up Your Environment](#set-up-your-environment)
2. [Retrieve an Access Token](#retrieve-an-access-token)
3. [Generate an Image](#generate-an-image)
4. [View the Generated Image](#view-the-generated-image)
5. [Full Example](#full-example)
6. [Deepen Your Understanding](#deepen-your-understanding)

### APIs and Services

* [Adobe Creative Cloud](/creative-cloud)
* [Adobe Experience Platform](/experience-platform-apis)
* [Adobe Document Cloud](/document-services/homepage)
* [Adobe Cloud Manager](/experience-cloud/cloud-manager)
* [Adobe Analytics](/analytics-apis/docs/2.0)
* [App Builder](/app-builder)
* [View all APIs and Services**View all**](/apis)

---

### Community

* [Adobe Developers Blog](https://blog.developer.adobe.com/)
* [Adobe on GitHub](https://github.com/adobe)
* [Adobe Developer on YouTube](https://youtube.com/channel/UCDtYqOjS9Eq9gacLcbMwhhQ)
* [Adobe Developer on X](https://twitter.com/adobedevs)
* [Community Forums](https://community.adobe.com/)

---

### Support

* [Adobe Developer support](/developer-support)
* [Adobe Product support](https://helpx.adobe.com/contact/enterprise-support.html)

---

### Adobe Developer

* [Adobe Developer Console](/developer-console)
* [Developer Distribution](/developer-distribution/)
* [Open source at Adobe](/open)
* [Download SDKs](/console/downloads)
* [Authentication](/developer-console/docs/guides/authentication)
* [Careers](https://adobe.com/careers.html)
* [Compliance](https://developer.adobe.com/compliance/)

---

* [Privacy](https://adobe.com/privacy.html)
* [Terms of Use](https://adobe.com/legal/terms.html)
* [](#/)
* [Do not sell or share my personal information](https://adobe.com/privacy/us-rights.html)
* [AdChoices](https://adobe.com/privacy/opt-out.html#interest-based-ads)

Copyright © 2025 Adobe. All rights reserved.