from celery import shared_task
import requests
from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from .models import CryptoPrice
from organizations.models import Organization


@shared_task
def fetch_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"

    crypto_ids = [
        "bitcoin", "ethereum", "tether", "bnb", "xrp", "usdc", "solana",
        "cardano", "avalanche", "dogecoin", "polkadot", "chainlink",
        "polygon", "binance-usd", "tron", "dai", "litecoin", "uniswap",
        "bitcoin-cash", "stellar", "monero", "ethereum-classic", "cosmos",
        "filecoin", "hedera", "cronos", "arbitrum", "near", "vechain",
        "aave", "algo", "maker", "graph", "fantom", "eos", "decentraland",
        "theta-token", "flow", "tezos", "axie-infinity", "iota", "threshold",
        "neo", "kava", "gala", "celo", "waves", "compound"
    ]

    params = {
        "ids": ",".join(crypto_ids),
        "vs_currencies": "usd"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        organizations = Organization.objects.all()
        current_time = timezone.now()

        crypto_prices = []

        with transaction.atomic():
            for org in organizations:
                for crypto_id, price_info in data.items():
                    if 'usd' in price_info:
                        crypto_prices.append(
                            CryptoPrice(
                                org_id=org,
                                symbol=crypto_id.upper(),
                                price=Decimal(str(price_info['usd'])),
                                timestamp=current_time
                            )
                        )

            if crypto_prices:
                CryptoPrice.objects.bulk_create(crypto_prices)

        return (f"Successfully recorded {len(crypto_prices)} historical crypto price entries "
                f"for {len(organizations)} organizations at {current_time}")

    except requests.RequestException as e:
        return f"Error fetching crypto prices: {str(e)}"
    except Exception as e:
        return f"Error processing crypto prices: {str(e)}"
