
# PyNance - Core

| PyNance      	| Status 	| Branch 	| Reference 	|
|--------------	|--------	|--------	|-----------	|
| Core         	| [![Build Status](https://www.travis-ci.com/0x78f1935/PyNance.svg?branch=master)](https://www.travis-ci.com/0x78f1935/PyNance)	| Master | [Visit](https://github.com/0x78f1935/PyNance/tree/master) |
| Core         	| [![Build Status](https://www.travis-ci.com/0x78f1935/PyNance.svg?branch=master)](https://www.travis-ci.com/0x78f1935/PyNance)	| Development | [Visit](https://github.com/0x78f1935/PyNance/tree/development) |
| Webinterface 	| [![Build Status](https://www.travis-ci.com/0x78f1935/PyNance-Webinterface.svg?branch=master)](https://www.travis-ci.com/0x78f1935/PyNance-Webinterface) | Master | [Visit](https://github.com/0x78f1935/PyNance-Webinterface/tree/master) |
| Webinterface 	| [![Build Status](https://www.travis-ci.com/0x78f1935/PyNance-Webinterface.svg?branch=master)](https://www.travis-ci.com/0x78f1935/PyNance-Webinterface) | Development | [Visit](https://github.com/0x78f1935/PyNance-Webinterface/tree/development) |

---

# binance
## Binance Account

In order to fetch the latest market information and to be able to place orders you will need a Binance account. [You can create an account here](https://www.binance.com/en/register?ref=73051759). This account also contains your wallets and API credentials. Make sure to enable 2factor authentication.

## Binance API Credentials

After you have created your [binance account](#binance-account) you need to create your API credentials. Once created make sure to save them. The secret is hidden after creation and you need the secret in order to proceed. [You can follow the steps on how to create API credentials here](https://www.binance.com/en/support/faq/360002502072-How-to-create-API).

# UNITTESTS

You can run unittests by running

    python -m unittest

Some unittests are only available in production.
If you place a file called `.env` into the root of PyNance you can add the following values to run the unittests in production

    USE_IN_UNITTEST=1
    API_KEY=<Your api key>
    API_SECRET=<Your api secret>

Note: Do not add `"` (quotes) around your values.
Tests run in production mode will have no impact on the account itself. 

# BUILDING

You need to build a whl package.

    python -m build

# COPY TO SERVER

    scp -r D:\Private\PyNance server@192.168.178.213:/home/server/PyNance

## Debian10

    sudo apt-get install python3-dev
    sudo apt-get install python3-pip
    python3 -m pip install virtualenv
    python3 -m virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
