from random import uniform

from app.database.postgre import db
from app.database.postgre.models import (
    CryptoCourse, CryptoCurrency, CryptocurrencyWallet, CryptoTransaction,
    Fiat, FiatWallet, Session, User
)
from app.utils.generators import generate_id


def push_day_course(min_: float, max_: float, ticker: str):
    for hour in range(24):
        db.session.add(
            CryptoCourse(
                ID=generate_id(16),
                ticker=ticker,
                type_="hour",
                number=hour,
                price=uniform(min_, max_)
            )
        )


def push_month_course(min_: float, max_: float, ticker: str):
    for day in range(1, 32):
        db.session.add(
            CryptoCourse(
                ID=generate_id(16),
                ticker=ticker,
                type_="day",
                number=day,
                price=uniform(min_, max_)
            )
        )


def push_year_course(min_: float, max_: float, ticker: str):
    for month in range(1, 13):
        db.session.add(
            CryptoCourse(
                ID=generate_id(16),
                ticker=ticker,
                type_="month",
                number=month*2,
                price=uniform(min_, max_)
            )
        )
        db.session.add(
            CryptoCourse(
                ID=generate_id(16),
                ticker=ticker,
                type_="month",
                number=month*2-1,
                price=uniform(min_, max_)
            )
        )


def push_cryptocurrencies():
    db.session.add(
        CryptoCurrency(
            ticker="BTC",
            name="Bitcoin",
            description="""
                <h3 class="desc-header">Overview</h3>
                <p class="desc-text">
                    Bitcoin (BTC) is the world's first globally viable
                    cryptocurrency built with blockchain technology. Outlined
                    in 2008 by an anonymous developer under the pseudonym
                    Satoshi Nakamoto, Bitcoin remains the most widely accepted
                    and traded cryptocurrency today. Nakamoto conceived
                    Bitcoin as a peer-to-peer electronic cash system that had
                    no need for a central authority or single administrator. A
                    global team of developers continues to maintain and work
                    on the improvement of the Bitcoin protocol.
                </p>
                <h3 class="desc-header">Who created Bitcoin?</h3>
                <p class="desc-text">
                    An unknown programmer published the Bitcoin white paper
                    under the pseudonym "Satoshi Nakamoto'' in 2008. Satoshi
                    Nakamoto may be an individual or a group of people.
                    Despite the widespread use and popularity of Bitcoin, the
                    true identity of Satoshi Nakamoto remains a mystery. Over
                    the years, many people have claimed to be the real Satoshi
                    Nakamoto, but none of them have been able to provide
                    definitive evidence to support their claims. Whoever
                    Nakamoto is or was, they went to great lengths to remain
                    anonymous. This mystery has helped increase the appeal of
                    bitcoin as a global currency and fascination surrounding
                    the origins of Bitcoin. Those closely related to
                    cryptography around the time of Bitcoin's conception
                    remain the most prominent suspects. These include computer
                    programmers Nick Szabo and the late Hal Finney. Miners
                    created the Bitcoin genesis block on January 3, 2009.
                </p>""",
            volume=28_388_811_901.291_736
        )
    )
    push_day_course(38928.0, 82931.0, "BTC")
    push_month_course(33928.0, 89931.0, "BTC")
    push_year_course(27928.0, 101931.0, "BTC")

    db.session.add(
        CryptoCurrency(
            ticker="ETH",
            name="Ethereum",
            description="""
                <h3 class="desc-header">Overview</h3>
                <p class="desc-text">
                    Ethereum is a decentralized, open-source blockchain
                    platform established in 2013. Unlike Bitcoin, which
                    focuses mainly on digital payments, Ethereum empowers
                    developers to create decentralized applications (dApps)
                    for diverse purposes, such as finance, gaming, and supply
                    chain management. Smart contracts, which are
                    self-executing programs containing the terms of agreements
                    in code, underpin these applications. Ethereum was the
                    first platform to introduce smart contract functionality.
                    It operates using Ether (ETH), its native cryptocurrency,
                    necessary for executing smart contracts and transactions
                    on the network. Ether, the second largest cryptocurrency
                    by market capitalization, can be traded on exchanges and
                    serves as a store of value, akin to Bitcoin. Users of the
                    Ethereum blockchain pay gas fees, denominated in ETH, for
                    transaction validation.
                </p>
                <h3 class="desc-header">Creator</h3>
                <p class="desc-text">
                    Vitalik Buterin, a Russian-Canadian programmer, created
                    Ethereum. At just 19, he recognized the limitations of
                    centralized systems after a frustrating change to his
                    favorite World of Warcraft character. This inspired his
                    vision of a decentralized digital network enabling the
                    development of applications interacting with digital
                    currencies. Before Ethereum, Buterin co-founded Bitcoin
                    Magazine, one of the earliest Bitcoin publications. He
                    published the Ethereum white paper in 2014 and launched
                    the project in 2015, mining the genesis block on July 30,
                    2015. Buterin’s vision attracted several passionate
                    co-founders, including Gavin Wood, Joseph Lubin, Anthony
                    Di Iorio, and Charles Hoskinson. Together, they founded
                    the Ethereum Foundation, a non-profit organization aimed
                    at supporting the platform's development and ecosystem.
                    Notably, only Buterin remains with the project from the
                    original co-founders.
                </p>
                <a href="https://www.youtube.com/shorts/LtrgP17dw_E">
                    His best video ever.
                </a>""",
            volume=7_865_323_997.264_321
        )
    )
    push_day_course(2373.0, 2963.0, "ETH")
    push_month_course(2173.0, 3263.0, "ETH")
    push_year_course(1973.0, 3463.0, "ETH")

    db.session.add(
        CryptoCurrency(
            ticker="USDT",
            name="Tether",
            description="""
                <h3 class="desc-header">Overview</h3>
                <p class="desc-text">
                    Tether (USDT) is a stablecoin, which is a type of
                    cryptocurrency that actively works to keep its valuation
                    stable through market mechanisms. It’s used by investors
                    who want to hedge against the inherent volatility of their
                    cryptocurrency investments while still keeping value
                    inside the crypto market, ready to be used without hassle.
                    Tether is a fiat-collateralized stablecoin, which is a
                    type of stablecoin that is backed by a fiat currency like
                    USD, CAD, AUD, or even Yen (JPY). Tether was created to
                    bridge the gaps between fiat currencies and blockchain
                    assets while offering transparency, stability, and low
                    fees for USDT users. Tether is pegged against the U.S.
                    Dollar at a 1:1 ratio. There is no guarantee from Tether
                    Ltd. for any right of redemption or exchange of Tether to
                    USD. USDT cannot be exchanged directly for USD through the
                    Tether company.
                </p>
                <h3 class="desc-header">How does Tether work?</h3>
                <p class="desc-text">
                    Each Tether issued is backed by one US dollar worth
                    of assets. All Tether was initially issued on the Bitcoin
                    blockchain via the Omni Layer protocol, but can now be
                    issued on any chain that Tether currently supports. Once a
                    tether (a single unit of USDT) has been issued, it can be
                    used the same as any other currency or token on the chain
                    that it has been issued on. Tether currently supports the
                    Bitcoin, Ethereum, EOS, Tron, Algorand, and OMG Network
                    blockchains. Tether uses Proof Of Reserves, which means
                    that at any time their reserves will be equal to or
                    greater than the number of Tether in circulation. This can
                    be verified via their website.
                </p>""",
            volume=42_177_103_848.376_772
        )
    )
    push_day_course(0.983_813, 1.011_362, "USDT")
    push_month_course(0.983_813, 1.011_362, "USDT")
    push_year_course(0.983_813, 1.011_362, "USDT")

    db.session.add(
        User(
            uuid="1e383b66-5612-4590-98b6-865967fc3f8f",
            name="Chirill",
            password_hash=(
                "$2b$12$pFGpw0EWOBUQpQSps4ozgeanaMu7YmfYf/hKerT87pOzZOYSabkBy"
            ),
            role="admin",
            email="37289dejk",
            alien_number=2
        )
    )

    db.session.add(
        Session(
            session_id=generate_id(16),
            user_id="1e383b66-5612-4590-98b6-865967fc3f8f",
            device="Linux, Chrome"
        )
    )

    db.session.add(
        CryptocurrencyWallet(
            ID=generate_id(36),
            ticker="BTC",
            amount=12,
            income=100000,
            invested=100000,
            user_id="1e383b66-5612-4590-98b6-865967fc3f8f"
        )
    )

    db.session.add(
        CryptoTransaction(
            ID=generate_id(36),
            ticker="BTC",
            amount=12,
            type_="buy",
            price=100000,
            user_id="1e383b66-5612-4590-98b6-865967fc3f8f"
        )
    )

    db.session.add(
        Fiat(
            iso="USD",
            name="United States Dollar",
            description="dollar description",
            volume=1_000_000.372832
        )
    )

    db.session.add(
        FiatWallet(
            ID=generate_id(36),
            iso="USD",
            amount=1_000_000.372832,
            user_id="1e383b66-5612-4590-98b6-865967fc3f8f"
        )
    )

    db.session.commit()
