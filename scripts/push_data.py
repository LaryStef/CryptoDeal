# run from collector's root

import os
import csv
from random import uniform, randint
from string import ascii_letters, digits

from sqlalchemy import create_engine, Engine, MetaData
from sqlalchemy.orm import Session

from src.database.models import CryptoCourse, CryptoCurrency, Fiat


SQLALCHEMY_DATABASE_URI: str = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/{os.getenv('POSTGRES_NAME')}"  # noqa: E501

engine: Engine = create_engine(SQLALCHEMY_DATABASE_URI)
metadata: MetaData = MetaData()


def _add_fiat_currencies() -> None:
    session.add(
        Fiat(
            iso="USD",
            name="United States Dollar",
            description="Dollar description",
            volume=1_000_000
        )
    )


def _add_cryptocurrencies() -> None:
    # session.add(
    #     CryptoCurrency(
    #         ticker="BTC",
    #         name="Bitcoin",
    #         description="""
    #             <h3>What is Bitcoin?</h3>
    #             <p>
    #                 Bitcoin (BTC) is the world's first globally viable
    #                 cryptocurrency built with blockchain technology. Outlined
    #                 in 2008 by an anonymous developer under the pseudonym
    #                 Satoshi Nakamoto, Bitcoin remains the most widely accepted
    #                 and traded cryptocurrency today. Nakamoto conceived
    #                 Bitcoin as a peer-to-peer electronic cash system that had
    #                 no need for a central authority or single administrator. A
    #                 global team of developers continues to maintain and work
    #                 on the improvement of the Bitcoin protocol.
    #             </p>
    #             <h3>Who created Bitcoin?</h3>
    #             <p>
    #                 An unknown programmer published the Bitcoin white paper
    #                 under the pseudonym "Satoshi Nakamoto" in 2008. Satoshi
    #                 Nakamoto may be an individual or a group of people.
    #                 Despite the widespread use and popularity of Bitcoin, the
    #                 true identity of Satoshi Nakamoto remains a mystery. Over
    #                 the years, many people have claimed to be the real Satoshi
    #                 Nakamoto, but none of them have been able to provide
    #                 definitive evidence to support their claims. Whoever
    #                 Nakamoto is or was, they went to great lengths to remain
    #                 anonymous. This mystery has helped increase the appeal of
    #                 bitcoin as a global currency and fascination surrounding
    #                 the origins of Bitcoin. Those closely related to
    #                 cryptography around the time of Bitcoin's conception
    #                 remain the most prominent suspects. These include computer
    #                 programmers Nick Szabo and the late Hal Finney. Miners
    #                 created the Bitcoin genesis block on January 3, 2009.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="ETH",
    #         name="Ethereum",
    #         description="""
    #             <h3>What is Ethereum?</h3>
    #             <p>
    #                 Ethereum is a decentralized, open-source blockchain
    #                 platform established in 2013. Unlike Bitcoin, which
    #                 focuses mainly on digital payments, Ethereum empowers
    #                 developers to create decentralized applications (dApps)
    #                 for diverse purposes, such as finance, gaming, and supply
    #                 chain management. Smart contracts, which are
    #                 self-executing programs containing the terms of agreements
    #                 in code, underpin these applications. Ethereum was the
    #                 first platform to introduce smart contract functionality.
    #                 It operates using Ether (ETH), its native cryptocurrency,
    #                 necessary for executing smart contracts and transactions
    #                 on the network. Ether, the second largest cryptocurrency
    #                 by market capitalization, can be traded on exchanges and
    #                 serves as a store of value, akin to Bitcoin. Users of the
    #                 Ethereum blockchain pay gas fees, denominated in ETH, for
    #                 transaction validation.
    #             </p>
    #             <h3>Creator</h3>
    #             <p>
    #                 Vitalik Buterin, a Russian-Canadian programmer, created
    #                 Ethereum. At just 19, he recognized the limitations of
    #                 centralized systems after a frustrating change to his
    #                 favorite World of Warcraft character. This inspired his
    #                 vision of a decentralized digital network enabling the
    #                 development of applications interacting with digital
    #                 currencies. Before Ethereum, Buterin co-founded Bitcoin
    #                 Magazine, one of the earliest Bitcoin publications. He
    #                 published the Ethereum white paper in 2014 and launched
    #                 the project in 2015, mining the genesis block on July 30,
    #                 2015. Buterin's vision attracted several passionate
    #                 co-founders, including Gavin Wood, Joseph Lubin, Anthony
    #                 Di Iorio, and Charles Hoskinson. Together, they founded
    #                 the Ethereum Foundation, a non-profit organization aimed
    #                 at supporting the platform's development and ecosystem.
    #                 Notably, only Buterin remains with the project from the
    #                 original co-founders.
    #             </p>
    #             <a href="https://www.youtube.com/shorts/LtrgP17dw_E">
    #                 His best video ever.
    #             </a>""",
    #         volume=7_865_323_997.26
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="USDT",
    #         name="Tether",
    #         description="""
    #             <h3>What is Tether?</h3>
    #             <p>
    #                 Tether (USDT) is a stablecoin, which is a type of
    #                 cryptocurrency that actively works to keep its valuation
    #                 stable through market mechanisms. It's used by investors
    #                 who want to hedge against the inherent volatility of their
    #                 cryptocurrency investments while still keeping value
    #                 inside the crypto market, ready to be used without hassle.
    #                 Tether is a fiat-collateralized stablecoin, which is a
    #                 type of stablecoin that is backed by a fiat currency like
    #                 USD, CAD, AUD, or even Yen (JPY). Tether was created to
    #                 bridge the gaps between fiat currencies and blockchain
    #                 assets while offering transparency, stability, and low
    #                 fees for USDT users. Tether is pegged against the U.S.
    #                 Dollar at a 1:1 ratio. There is no guarantee from Tether
    #                 Ltd. for any right of redemption or exchange of Tether to
    #                 USD. USDT cannot be exchanged directly for USD through the
    #                 Tether company.
    #             </p>
    #             <h3>How does Tether work?</h3>
    #             <p>
    #                 Each Tether issued is backed by one US dollar worth
    #                 of assets. All Tether was initially issued on the Bitcoin
    #                 blockchain via the Omni Layer protocol, but can now be
    #                 issued on any chain that Tether currently supports. Once a
    #                 tether (a single unit of USDT) has been issued, it can be
    #                 used the same as any other currency or token on the chain
    #                 that it has been issued on. Tether currently supports the
    #                 Bitcoin, Ethereum, EOS, Tron, Algorand, and OMG Network
    #                 blockchains. Tether uses Proof Of Reserves, which means
    #                 that at any time their reserves will be equal to or
    #                 greater than the number of Tether in circulation. This can
    #                 be verified via their website.
    #             </p>""",
    #         volume=42_177_103_848.39
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="XRP",
    #         name="Ripple",
    #         description="""
    #             <h3>What is Ripple?</h3>
    #             <p>
    #                 The XRP Ledger, or XRPL is an open-source distributed
    #                 ledger powered by a network of peer-to-peer servers. XRPis
    #                 the digital asset native to the network, which is designed
    #                 to function as a bridge currency. The goal of the network
    #                 is to “power innovative technology across the payments
    #                 space” and enable “seamless, real-time, final, and
    #                 cost-effective” global payments, as stated on the project
    #                 website.
    #             </p>
    #             <h3>Uses for Ripple</h3>
    #             <p>
    #                 The network seeks to achieveimproved currency utility over
    #                 legacy payment channels, asXRP can be used by a wide range
    #                 of third parties that seekto augment their value through
    #                 decentralized means. TheXRP Ledger operates on the basis of
    #                 validator nodes thatcollect the set of all candidate
    #                 transactions and reachconsensus on transactions that
    #                 occurred before the cut-offtime for any given ledger. Once
    #                 the set of transactions isagreed upon, they are executed in
    #                 a deterministic order,subject to the objective rules of the
    #                 network, as imposedby every server independently. The
    #                 ledger reachesconsensus on all outstanding transactions
    #                 every 3-5seconds.
    #             </p>
    #             <h3>How does Ripple Work?</h3>
    #             <p>
    #                 The ledger features a decentralized exchange that allows
    #                 the trading of IOUs and XRP. It also features some smart
    #                 contract functionality and supports the network-agnostic
    #                 Interledger Protocol. XRPL was released in 2012 and has
    #                 since been maintained by community participants, including
    #                 Ripple, which holds a large amount of XRP, though its
    #                 holdings are largely locked and purpose-bound.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="ADA",
    #         name="Cardano",
    #         description="""
    #             <h3>What is Cardano?</h3>
    #             <p>
    #                 Cardano is a public blockchain platform and smart contract
    #                 development platform that is similar to Ethereum. Founded
    #                 in 2015, Cardano touts itself as the first blockchain
    #                 platform in the crypto industry to be founded on
    #                 peer-reviewed research. Its blockchain is powered by
    #                 Ouroboros, a proof-of-stake protocol that its proponents
    #                 claim has improved upon the foundations of other consensus
    #                 mechanisms. ADA is the multi-purpose native token of
    #                 Cardano and powers all transactions on the network. It
    #                 also provides rewards to network validators (also called
    #                 stakers). These users help secure the network and verify
    #                 new transactions entering the Cardano blockchain. The
    #                 Cardano blockchain provides a secure way for users to
    #                 store and send ADA over the network. This factor includes
    #                 native tokens created on top of the Cardano blockchain.
    #                 Additionally, it provides functionality for developing
    #                 decentralized applications.
    #             </p>
    #             <h3>How does Cardano work?</h3>
    #             <p>
    #                 The native coin of the Cardano blockchain is ADA, which
    #                 has a maximum supply of 45 billion coins. Cardano's
    #                 tokenomics include a built-in treasury system and a
    #                 mechanism for funding future development through a
    #                 decentralized governance system. Validators process
    #                 transactions on the Cardano blockchain. To do this, they
    #                 must first lock away an amount of native tokens in a
    #                 staking smart contract. Holders use specific crypto wallets
    #                 to store ADA. These can be either hardware wallet or
    #                 software-based wallets. Cardano allows users to stake
    #                 Cardano ADA coins to earn rewards and participate in the
    #                 management of its blockchain network. Soon, holders of ADA
    #                 will be able to vote on changes made within the protocol,
    #                 giving them direct control over its features and operation.
    #                 Cryptocurrencies that allow holders to vote on the future
    #                 development of the blockchain protocol they are associated
    #                 with are known as governance tokens. Governance features
    #                 are expected to go live once the Voltaire phase of
    #                 Cardano's development begins.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="AVAX",
    #         name="Avalanche",
    #         description="""
    #             <h3>What is Avalanche?</h3>
    #             <p>
    #                 Avalanche is a blockchain platform that aims to address the
    #                 blockchain trilemma of scalability, security and
    #                 decentralization thanks to its unique Proof of Stake (PoS)
    #                 mechanism. Like Ethereum, Avalanche supports smart
    #                 contracts to run decentralized applications (dApps) on its
    #                 network. Since Avalanche's smart contracts are written in
    #                 the Solidity language also used by Ethereum, it aims to
    #                 create greater blockchain interoperably by integrating a
    #                 number of decentralized finance (DeFi) ecosystems,
    #                 including well-established projects like Aave and Curve.
    #                 AVAX, the native token of the Avalanche platform, is used
    #                 to power transactions in its ecosystem. AVAX serves as the
    #                 means to distribute system rewards, participate in
    #                 governance and facilitate transactions on the network by
    #                 paying fees.
    #             </p>
    #             <h3>Who created Avalanche?</h3>
    #             <p>
    #                 In May 2018, Team Rocket — a pseudonymous group of software
    #                 developers — published an article that detailed the basis
    #                 for the Avalanche protocol. Soon afterwards, Emin Gün Sirer
    #                 founded AVA Labs with the goal of creating and developing
    #                 the Avalanche blockchain. Sirer is a professor of computer
    #                 science at Cornell University and was a notable member of
    #                 the Initiative for Cryptocurrencies and Contracts (IC3). In
    #                 2003, he also created Karma, a Proof of Work virtual
    #                 currency for peer-to-peer file sharing systems that
    #                 predated Bitcoin. Avalanche raised $42 million through an
    #                 ICO in July 2020 and has continued to draw big investments
    #                 since. In July 2021, the Avalanche Foundation held a token
    #                 sale raising $230 million, with participants including
    #                 large VC companies such as Polychain and Three Arrows
    #                 Capital.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="DOGE",
    #         name="Dogecoin",
    #         description="""
    #             <h3>What is Dogecoin?</h3>
    #             <p>
    #                 Dogecoin is a decentralized, peer-to-peer cryptocurrency
    #                 centering around the "Doge" meme, which serves as its
    #                 mascot. Built using blockchain technology, Dogecoin (DOGE)
    #                 was once a popular tipping cryptocurrency and fundraising
    #                 mechanism for multiple charitable causes. Dogecoin features
    #                 the likeness of the Shiba Inu dog popularized in the "Doge"
    #                 meme. The cryptocurrency first appeared as a light-hearted
    #                 marketing experiment in 2013. DOGE quickly gained a massive
    #                 audience in the crypto market and now boasts one of the
    #                 largest market caps in the industry. Doge is pleased. The
    #                 success and virality of Dogecoin spurred the creation of
    #                 other Shiba Inu-themed projects thereby launching an
    #                 entirely new crypto industry sector of "meme coins." Shiba
    #                 Inu Coin (SHIB) is a leading example of a popular spin-off
    #                 with a similarly large market capitalization.
    #             </p>
    #             <h3>How does Dogecoin work?</h3>
    #             <p>
    #                 Dogecoin operates using a proof-of-work-based (PoW)
    #                 consensus mechanism and has an inflationary supply of
    #                 coins. This fact means that there is no cap on the maximum
    #                 supply of coins that the protocol can create. Initially,
    #                 Palmer and Markus agreed to set the max supply at 100
    #                 billion coins. However, the co-founders later removed this
    #                 feature to keep prices low and encourage users to send
    #                 tokens to one another. Dogecoin's inflationary nature means
    #                 its native digital asset DOGE, is not typically recommended
    #                 as a reliable store of value. As of April 2023, the current
    #                 supply of Dogecoins is over 130 billion DOGE, with a
    #                 maximum supply of 10,000 DOGE per block. The balance of
    #                 supply is constantly changing as new coins are minted
    #                 through mining. This steady influx of fixed block rewards
    #                 means the inflation rate technically decreases over
    #                 time. Dogecoin's inflationary supply allows for a more
    #                 flexible and adaptable ecosystem that can respond to market
    #                 demands. Palmer and Markus created Dogecoin as a fork of
    #                 Lucky Coin, an open-source proof-of-work project forked
    #                 from Litecoin. Because of this, Dogecoin uses the Scrypt
    #                 mining algorithm instead of the SHA-256 mining algorithm
    #                 used by Bitcoin.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="SOL",
    #         name="Solana",
    #         description="""
    #             <h3>What is Solana?</h3>
    #             <p>
    #                 Solana is a leading blockchain-based platform that provides
    #                 smart contract functionality for developers to create their
    #                 own decentralized applications. Blockchains like Solana
    #                 allow a network of users to track information in a
    #                 peer-to-peer way. Solana is not reliant on a single
    #                 intermediary, like a person or a company, to verify
    #                 information stored on its blockchain. Instead, this
    #                 information is collectively shared and updated across the
    #                 blockchain network itself. Smart contracts, like those used
    #                 on Solana, allow individuals to define and automatically
    #                 execute actions based on pre-defined conditions. Smart
    #                 contracts are the building blocks of much of the
    #                 functionality on the Solana blockchain. Leveraging these
    #                 smart contracts, blockchain developers can create their own
    #                 unique decentralized applications (dApps), crypto tokens,
    #                 and other services on the Solana blockchain for others to
    #                 use.
    #             </p>
    #             <h3>What makes Solana unique?</h3>
    #             <p>
    #                 Solana has differentiated itself from other blockchain
    #                 networks by offering a platform that has faster transaction
    #                 speeds and lower fees than many other blockchains. Although
    #                 Bitcoin and Ethereum are still the projects with the
    #                 largest market capitalizations in the cryptocurrency
    #                 market, Solana's focus on increasing speed and lowering
    #                 fees has helped it rise within the blockchain space.
    #                 Solana's ability to process a comparatively high number of
    #                 transactions per second with lower transaction fees has
    #                 helped it become a popular choice for decentralized finance
    #                 (DeFi) and non-fungible token (NFT) projects. In contrast
    #                 to many newer blockchains that still developing an
    #                 ecosystem of apps and projects, Solana offers a vibrant
    #                 community of different products and services. This ability
    #                 to integrate with and build alongside projects with
    #                 existing userbases has made Solana an attractive blockchain
    #                 for many new crypto project developers.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="TON",
    #         name="Toncoin",
    #         description="""
    #             <h3>What is Toncoin?</h3>
    #             <p>
    #                 Toncoin (TON) is a decentralized cryptocurrency that powers
    #                 the Ton blockchain, which was designed to be fast,
    #                 scalable, and secure. Originally developed as part of the
    #                 Telegram Open Network (TON) by the team behind the
    #                 messaging app Telegram, TON aims to provide a platform for
    #                 decentralized applications (dApps), fast payments, and
    #                 secure data storage. The blockchain features a
    #                 multi-layered structure and sharding technology, allowing
    #                 it to handle millions of transactions per second. Toncoin
    #                 is used for transaction fees, staking, and governance
    #                 within the network. With its focus on low-cost, high-speed
    #                 transactions and the ability to support a wide range of
    #                 decentralized services, Toncoin has gained popularity in
    #                 the cryptocurrency community. After the project's split
    #                 from Telegram, the TON Foundation continued its
    #                 development, ensuring the blockchain remains
    #                 community-driven and open-source.
    #             </p>
    #             <h3>Who created Toncoin?</h3>
    #             <p>
    #                 Toncoin was initially created by the team behind Telegram,
    #                 including Pavel and Nikolai Durov, the founders of the
    #                 messaging app. The project was launched in 2018 under the
    #                 name Telegram Open Network (TON) and was designed to
    #                 integrate blockchain technology with Telegram's vast user
    #                 base. However, after legal challenges from the U.S.
    #                 Securities and Exchange Commission (SEC), Telegram halted
    #                 its involvement with the project in 2020. Despite this, the
    #                 community continued to develop the project independently,
    #                 leading to the rebranding of TON as Toncoin. The Toncoin
    #                 blockchain is now maintained by the TON Foundation, a
    #                 decentralized organization that oversees the network's
    #                 growth and development, ensuring that it remains
    #                 open-source and community-driven.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="TRX",
    #         name="Tron",
    #         description="""
    #             <h3>What is Tron?</h3>
    #             <p>
    #                 Launched at the height of 2017's crypto mania, Tron has
    #                 since galvanized a global group of investors and developers
    #                 around a vision for how cryptocurrencies could reshape the
    #                 internet. But if the goal of using blockchains to create a
    #                 distributed web was common among projects launching at the
    #                 time, Tron distinguished its offering with communications
    #                 that resonated, even as criticisms about its technology
    #                 persisted. For instance, Tron was rare among
    #                 cryptocurrencies launching in 2017 in that it did not seek
    #                 to advertise any advances in cryptography or network
    #                 design. Rather, the basic building blocks of Tron -
    #                 decentralized applications, smart contracts, tokens,
    #                 delegated proof-of-stake consensus - were pioneered by
    #                 other projects prior to its launch. Tron even went so far
    #                 as to make components of its technology compatible with
    #                 Ethereum (ETH) (which sparked accusations it went too far
    #                 in borrowing its ideas).Tron would further differentiate
    #                 with an Asia-focused go-to-market strategy that heavily
    #                 relied on publicizing its creator Justin Sun and
    #                 translating its technical documents into a wider variety of
    #                 languages than generally targeted by cryptocurrency
    #                 projects.
    #             </p>
    #             <h3>Who created Tron?</h3>
    #             <p>
    #                 Tron was created by entrepreneur Sun Yuchen (Justin Sun), a
    #                 two-time recipient of Forbes' “30-Under-30” award in Asia,
    #                 in early 2017. An established presence in China, Sun had
    #                 earlier founded the audio content application Peiwo and
    #                 served in 2015 as a representative for Ripple, the
    #                 for-profit company that stewards the XRP cryptocurrency,
    #                 before founding the Tron Foundation that year. Sun's
    #                 business background succeeded in attracting early interest
    #                 from investors including Clash of Kings founder Tang Binsen
    #                 and CEO of bike sharing startup OFO Dai Wei, among others.
    #                 These supporters, in turn, boosted visibility of the
    #                 project's September ICO, which raised millions in
    #                 cryptocurrency from the public using a token on the
    #                 ethereum blockchain. A second version of the white paper
    #                 further outlining Tron's technology was released in 2018.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="NEAR",
    #         name="NEAR Protocol",
    #         description="""
    #             <h3>What is NEAR Protocol?</h3>
    #             <p>
    #                 NEAR Protocol is a sharded, proof-of-stake blockchain
    #                 designed for usability and scalability, aiming to bridge
    #                 the gap between the complex world of blockchain technology
    #                 and the mainstream user. It achieves this through its
    #                 innovative “Nightshade” sharding mechanism, which divides
    #                 the network into smaller, more manageable segments,
    #                 allowing for parallel processing of transactions and a much
    #                 higher transaction throughput compared to traditional
    #                 blockchains. NEAR emphasizes a developer-friendly
    #                 environment with its focus on easy onboarding,
    #                 human-readable account names, and a robust suite of tools.
    #                 This makes it simpler for developers to build and deploy
    #                 decentralized applications (dApps), potentially encouraging
    #                 wider adoption of blockchain technology by making it more
    #                 accessible. The protocol also prioritizes a user-centric
    #                 approach, with features designed to streamline the user
    #                 experience, such as intuitive wallet management and clear
    #                 explanations of complex processes.
    #             </p>
    #             <h3>Key features and interoperability</h3>
    #             <p>
    #                 A key aspect of NEAR's functionality is its “Rainbow
    #                 Bridge”, a trustless bridge that enables seamless
    #                 interoperability with the Ethereum network. This allows
    #                 users to transfer assets and data between the two
    #                 blockchains, expanding the reach and utility of
    #                 applications built on NEAR. Furthermore, the protocol's
    #                 governance is decentralized, with token holders able to
    #                 participate in proposals and shape the future development
    #                 of the network. NEAR's focus on community-driven innovation
    #                 is reflected in its open-source ethos and the active
    #                 participation of its ecosystem members. The protocol also
    #                 utilizes a gas fee model where fees are used to reward
    #                 validators. These features and a strong focus on
    #                 user-friendliness make NEAR a significant player in the
    #                 blockchain space.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="USDC",
    #         name="USD Coin",
    #         description="""
    #             <h3>What is USDC?</h3>
    #             <p>
    #                 USDC, or USD Coin, is a stablecoin pegged to the US dollar.
    #                 Operating on various blockchain networks including
    #                 Ethereum, Solana, and Algorand, it strives to maintain a
    #                 consistent 1:1 value with the dollar, meaning each USDC
    #                 token should be worth one US dollar. Unlike volatile
    #                 cryptocurrencies subject to significant price swings, USDC
    #                 provides a relatively stable store of value, making it
    #                 attractive for transactions, trading, and holding assets
    #                 within the cryptocurrency ecosystem. It's designed with
    #                 transparency in mind, backed by reserves primarily
    #                 consisting of cash and short-term U.S. Treasury bonds. This
    #                 backing, alongside regular audits, helps ensure its peg to
    #                 the dollar, providing users with confidence in its
    #                 stability and facilitating easy exchange between USDC and
    #                 fiat currency. USDC serves as a crucial bridge connecting
    #                 the traditional financial system with the decentralized
    #                 world of blockchain, offering a more familiar and less
    #                 risky entry point for many.
    #             </p>
    #             <h3>The creators and mechanics of USDC</h3>
    #             <p>
    #                 USDC was jointly created by Centre, a consortium formed by
    #                 the prominent cryptocurrency exchange Coinbase and the
    #                 financial technology firm Circle. This partnership aimed to
    #                 establish a more regulated and trustworthy stablecoin
    #                 compared to existing alternatives in the market. The
    #                 creation and redemption of USDC involves a straightforward
    #                 process: users deposit U.S. dollars into Centre's banking
    #                 partners, and an equivalent amount of USDC tokens is then
    #                 minted and added to the relevant blockchain. Conversely,
    #                 when a user wants to redeem their USDC, the tokens are
    #                 burned, and the corresponding value in U.S. dollars is
    #                 transferred to their bank account. This system of minting
    #                 and burning, combined with regular, independent audits of
    #                 the reserve assets, is critical in upholding USDC's peg to
    #                 the dollar. By prioritizing transparency and regulatory
    #                 compliance, USDC aims to foster broader acceptance and
    #                 utilization of blockchain technology within the financial
    #                 sector.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="LINK",
    #         name="Chainlink",
    #         description="""
    #             <h3>What is Chainlink?</h3>
    #             <p>
    #                 Chainlink is a decentralized oracle network designed to
    #                 bridge the gap between smart contracts on blockchains and
    #                 the real world. Essentially, smart contracts, which are
    #                 self-executing agreements on blockchains, often require
    #                 real-world data to function properly. This data could range
    #                 from weather forecasts and stock prices to shipping
    #                 information and election results. Chainlink provides a
    #                 secure and reliable way to feed this external information
    #                 into smart contracts. It achieves this by connecting to
    #                 various Application Programming Interfaces (APIs) and data
    #                 providers, aggregating data from multiple sources, and then
    #                 verifying that information before relaying it to the
    #                 blockchain. This system ensures that smart contracts can
    #                 function accurately, avoiding reliance on a single point of
    #                 failure, and thus making them more useful and trustworthy.
    #             </p>
    #             <h3>How Chainlink's network operates</h3>
    #             <p>
    #                 Chainlink's decentralized network comprises independent
    #                 node operators who are responsible for fetching data from
    #                 off-chain sources and delivering it to on-chain smart
    #                 contracts. These operators stake LINK tokens, Chainlink's
    #                 native cryptocurrency, as a form of collateral,
    #                 incentivizing good behavior and penalizing malicious or
    #                 inaccurate data reporting through slashing. When a smart
    #                 contract requests specific off-chain data, the Chainlink
    #                 network automatically selects a group of node operators to
    #                 gather and verify that information. These operators fetch
    #                 the data from the designated APIs, which are then validated
    #                 via a process that aggregates and averages them before
    #                 relaying the resulting information on-chain. This
    #                 decentralized approach not only strengthens the system
    #                 against manipulation but also provides a cost-efficient
    #                 method of accessing accurate and reliable information from
    #                 diverse sources.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="SUI",
    #         name="Sui",
    #         description="""
    #             <h3>What is Sui?</h3>
    #             <p>
    #                 Sui is a relatively new, layer-1 blockchain designed for a
    #                 more scalable and efficient decentralized future. It
    #                 differentiates itself by utilizing the Move programming
    #                 language and a unique object-centric data model. Instead of
    #                 treating transactions as sequences of actions that modify
    #                 accounts, Sui focuses on individual objects which can be
    #                 owned and manipulated by addresses. This allows for
    #                 transactions to be processed in parallel, significantly
    #                 increasing throughput and lowering latency. Moreover, Sui's
    #                 architecture minimizes consensus overhead and focuses on
    #                 achieving high performance, making it suitable for
    #                 applications with demanding requirements, such as gaming
    #                 and decentralized finance. Sui aims to provide developers
    #                 with a powerful platform for building complex applications
    #                 while maintaining a user-friendly and fast experience.
    #             </p>
    #             <h3>Sui's object-centric approach and move language</h3>
    #             <p>
    #                 The foundation of Sui's groundbreaking performance is
    #                 heavily reliant on its object-centric data model, deviating
    #                 from traditional account-based models. Instead of
    #                 manipulating whole account balances, Sui operates on
    #                 independent objects that possess their own unique
    #                 identifiers and properties, meaning transactions involving
    #                 them can often be executed concurrently. The smart contract
    #                 language of Sui, Move, further enhances security and
    #                 efficiency. Move is designed to prevent common
    #                 vulnerabilities like double-spending and re-entrancy
    #                 attacks, providing better guarantees for asset security. By
    #                 being optimized for this object-based model, Move enables
    #                 developers to create more efficient and secure applications
    #                 within the Sui ecosystem. This combination of novel data
    #                 handling and a custom language is what sets Sui apart,
    #                 allowing it to achieve high throughput, low latency, and
    #                 robust security in a decentralized manner.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="XLM",
    #         name="Stellar",
    #         description="""
    #             <h3>What is Stellar?</h3>
    #             <p>
    #                 Stellar is an open-source, decentralized payment protocol
    #                 designed to facilitate fast and low-cost cross-border
    #                 transactions. It functions as a hybrid between a
    #                 traditional cryptocurrency and a payment network, aiming to
    #                 connect individuals and financial institutions globally.
    #                 The network's native currency is Lumen (XLM), used for
    #                 paying transaction fees and as a bridge currency for
    #                 trading different fiat and cryptocurrencies. Unlike some
    #                 blockchains that rely on proof-of-work, Stellar uses a
    #                 unique consensus mechanism known as the Stellar Consensus
    #                 Protocol (SCP), which prioritizes speed, efficiency, and
    #                 security. This makes it ideal for a variety of use cases,
    #                 including remittances, micro-payments, and asset
    #                 tokenization. Stellar's mission is to promote financial
    #                 inclusion and accessibility worldwide, making global
    #                 transactions as easy as sending an email.
    #             </p>
    #             <h3>The origins and innovation of Stellar</h3>
    #             <p>
    #                 Stellar was co-founded by Jed McCaleb, one of the original
    #                 founders of Ripple, in 2014, after he left that project.
    #                 While it shares some initial concepts with Ripple, Stellar
    #                 was created with a different focus, explicitly prioritizing
    #                 individual users and developing nations with a non-profit
    #                 organization at its core. Unlike blockchains that often
    #                 have complex and computationally-intensive consensus
    #                 methods, Stellar's SCP employs a system of federated
    #                 byzantine agreement. This relies on a network of trusted
    #                 validators to quickly and efficiently reach consensus on
    #                 transactions, resulting in processing times of mere seconds
    #                 and minuscule transaction costs. This innovation is what
    #                 allows Stellar to be so effective in facilitating global
    #                 payments and asset exchange, especially for those currently
    #                 underserved by traditional banking systems.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="DOT",
    #         name="Polkadot",
    #         description="""
    #             <h3>Polkadot: a network of networks</h3>
    #             <p>
    #                 Polkadot is a blockchain platform designed to foster
    #                 interoperability between different blockchains. Think of it
    #                 as a “blockchain of blockchains,” aiming to solve the
    #                 problem of isolated chains that can't communicate with each
    #                 other. Instead of a single monolithic chain, Polkadot
    #                 employs a central “Relay Chain” that provides security and
    #                 consensus, and allows multiple specialized blockchains,
    #                 called “parachains,” to connect and interact. These
    #                 parachains can be built for specific purposes, customized
    #                 with unique features, and still benefit from the robust
    #                 security of the main Relay Chain. This structure allows for
    #                 a highly scalable and adaptable ecosystem, opening up new
    #                 possibilities for decentralized applications and services
    #                 by enabling the seamless transfer of data and assets
    #                 between different networks.
    #             </p>
    #             <h3>The visionary behind Polkadot: Gavin Wood</h3>
    #             <p>
    #                 Polkadot was created by Gavin Wood, a key figure in the
    #                 development of Ethereum. Wood co-founded Ethereum and
    #                 created Solidity, the programming language used to build
    #                 Ethereum smart contracts. Frustrated with the limitations
    #                 of Ethereum's scalability and the lack of interoperability
    #                 in the blockchain space, he envisioned Polkadot as a more
    #                 flexible and future-proof alternative. Wood's background as
    #                 a renowned computer scientist and experienced blockchain
    #                 architect led to Polkadot's unique design, which
    #                 prioritizes modularity and scalability through its
    #                 parachain model. His vision is not merely to create another
    #                 blockchain, but to establish an interconnected web of
    #                 blockchains that work together to build a more robust and
    #                 versatile decentralized future, ultimately pushing the
    #                 capabilities of blockchain technology itself.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="LTC",
    #         name="Litecoin",
    #         description="""
    #             <h3>A silver to Bitcoin's gold</h3>
    #             <p>
    #                 Litecoin is a cryptocurrency often described as the “silver
    #                 to Bitcoin's gold.” It's a peer-to-peer digital currency
    #                 that enables instant, near-zero cost payments to anyone in
    #                 the world. Like Bitcoin, it operates on a decentralized
    #                 blockchain network, meaning no single entity controls it.
    #                 The main aim of Litecoin was to address some of Bitcoin's
    #                 perceived limitations, particularly in transaction
    #                 processing speed. It utilizes a different hashing algorithm
    #                 called Scrypt, which was designed to be more ASIC-resistant
    #                 initially, making mining accessible to more users with
    #                 consumer-grade hardware. This quicker block generation time
    #                 means that transactions are confirmed roughly four times
    #                 faster than Bitcoin, making it a more suitable choice for
    #                 everyday transactions.
    #             </p>
    #             <h3>Charlie Lee and the faster alternative</h3>
    #             <p>
    #                 Litecoin was created by Charlie Lee, a former OpenAI
    #                 employee, who aimed to provide a more accessible and faster
    #                 alternative to Bitcoin. He launched Litecoin in 2011,
    #                 drawing heavily on Bitcoin's open-source code but with key
    #                 adjustments. One key change was a modification of Bitcoin's
    #                 hashing algorithm, transitioning to Scrypt which at the
    #                 time was more memory intensive and less efficient for
    #                 specialized mining hardware. This intended to create a more
    #                 egalitarian distribution of Litecoin, preventing the
    #                 dominance of large mining operations. This did not last as
    #                 the evolution of mining lead to the creation of ASICS for
    #                 Litecoin as well. Lee later became a prominent voice in the
    #                 crypto space, advocating for the advantages of Litecoin and
    #                 fostering its community. His motivations stemmed from the
    #                 belief in the importance of decentralized digital
    #                 currencies, and his work contributed significantly to the
    #                 broader acceptance of cryptocurrencies as viable
    #                 alternatives to traditional financial systems.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="UNI",
    #         name="Uniswap",
    #         description="""
    #             <h3>What is Uniswap?</h3>
    #             <p>
    #                 Uniswap is a decentralized cryptocurrency exchange, often
    #                 referred to as a DEX, operating on the Ethereum blockchain.
    #                 Unlike traditional exchanges, Uniswap doesn't rely on a
    #                 central intermediary to match buyers and sellers. Instead,
    #                 it uses automated smart contracts and liquidity pools to
    #                 facilitate trading of various ERC-20 tokens. Users can
    #                 directly swap one token for another by interacting with
    #                 these pools, which are essentially large reserves of token
    #                 pairs. The price for each swap is algorithmically
    #                 determined by the ratio of tokens within the pool, creating
    #                 a constantly evolving and self-balancing marketplace. This
    #                 innovative approach makes Uniswap a permissionless,
    #                 transparent, and highly accessible platform for trading
    #                 cryptocurrencies. It has been instrumental in fostering
    #                 decentralized finance (DeFi) adoption.
    #             </p>
    #             <h3>Automated market makers and the power of pools</h3>
    #             <p>
    #                 One of the key innovations of Uniswap is its use of
    #                 automated market makers (AMMs). Instead of relying on order
    #                 books like traditional exchanges, Uniswap uses algorithms
    #                 to set prices, based on the ratios of tokens within its
    #                 liquidity pools. Liquidity providers are users who
    #                 contribute their tokens to these pools, earning trading
    #                 fees in return. This system allows for trades to occur
    #                 without the need for a counterparty to be actively present
    #                 on the platform. This system allows for continuous trading,
    #                 as opposed to waiting for a corresponding order to be
    #                 placed, resulting in a more fluid trading experience and is
    #                 critical for the DeFi ecosystem, allowing new projects to
    #                 gain access to liquidity, or existing projects to move
    #                 liquidity from centralized exchanges, this dynamic
    #                 incentivization mechanism has made it a core component of
    #                 the DeFi movement.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="AAVE",
    #         name="Aave",
    #         description="""
    #             <h3>What is Aave?</h3>
    #             <p>
    #                 Aave is a decentralized finance (DeFi) protocol that allows
    #                 users to lend and borrow a variety of cryptocurrencies
    #                 without intermediaries. Functioning on the Ethereum
    #                 blockchain, it employs smart contracts to automate the
    #                 lending and borrowing process, removing the need for
    #                 traditional financial institutions. Users can earn interest
    #                 by depositing their crypto assets into lending pools, and
    #                 these assets are then used to provide loans to borrowers.
    #                 Aave operates using an overcollateralized loan model,
    #                 meaning borrowers must deposit assets worth more than the
    #                 loan they take out, reducing the risk for lenders. This
    #                 system enables users to earn passive income on their crypto
    #                 holdings and allows others to access liquidity without
    #                 selling their assets. The protocol's core principles are
    #                 transparency, security, and accessibility, striving to
    #                 provide a fairer and more efficient lending platform.
    #             </p>
    #             <h3>Aave's innovative features and governance</h3>
    #             <p>
    #                 Aave is more than just a simple lending and borrowing
    #                 platform; it's also known for innovative features. Notably,
    #                 it pioneered “flash loans,” which enable users to borrow
    #                 funds for brief periods without providing collateral, but
    #                 they must be returned within the same transaction. These
    #                 are often used for arbitrage opportunities. Further, Aave
    #                 implemented a governance token, AAVE, that allows holders
    #                 to vote on proposals, influencing changes to the protocol,
    #                 interest rates, and the addition of new assets, truly
    #                 placing the power of the platform into the hands of its
    #                 users. This decentralized governance model ensures Aave
    #                 remains adaptable to evolving market dynamics and community
    #                 needs. The team's constant work on new features and
    #                 integrations allows Aave to stay relevant and competitive
    #                 in the dynamic world of DeFi.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    # session.add(
    #     CryptoCurrency(
    #         ticker="XMR",
    #         name="Monero",
    #         description="""
    #             <h3>What is Monero?</h3>
    #             <p>
    #                 Monero (XMR) is a privacy-focused cryptocurrency that
    #                 distinguishes itself by prioritizing anonymity and
    #                 untraceability in transactions. Unlike many other
    #                 cryptocurrencies where transaction details are publicly
    #                 viewable on a blockchain, Monero utilizes advanced
    #                 cryptographic techniques to obscure the sender, receiver,
    #                 and amount of each transaction. This means that when you
    #                 send or receive XMR, no one can definitively link that
    #                 activity back to your specific wallet or identify the
    #                 transaction's value. This enhanced privacy makes Monero a
    #                 popular choice for individuals and entities who seek to
    #                 keep their financial activities confidential, offering a
    #                 higher level of financial freedom and security compared to
    #                 more transparent cryptocurrencies. It aims to be truly
    #                 fungible, meaning one XMR is indistinguishable from
    #                 another, just like physical cash.
    #             </p>
    #             <h3>How Monero achieves anonymity</h3>
    #             <p>
    #                 Monero achieves its strong privacy features through a
    #                 combination of innovative technologies. One key element is
    #                 Ring Signatures, which mix the sender's digital signature
    #                 with those of other users, making it nearly impossible to
    #                 determine the true originator. Another is Stealth
    #                 Addresses, which generate unique, one-time recipient
    #                 addresses for each transaction, preventing external parties
    #                 from linking multiple transactions to the same receiver.
    #                 Additionally, Ring Confidential Transactions (RingCT) are
    #                 employed to hide the amount being transferred, making it
    #                 impossible to track specific values. These technologies
    #                 work together to create an opaque and private blockchain,
    #                 ensuring that both user identities and transaction details
    #                 remain confidential. This complex layering of security
    #                 features provides Monero with its reputation as one of the
    #                 most anonymous and private cryptocurrencies currently
    #                 available.
    #             </p>""",
    #         volume=28_388_811_901.29
    #     )
    # )
    session.add(
        CryptoCurrency(
            ticker="OKB",
            name="OKB",
            description="""
                <h3>OKB: The utility token of the OKX ecosystem</h3>
                <p>
                    OKB is the utility token of the OKX cryptocurrency exchange
                    (formerly known as OKEx), one of the world's leading
                    digital asset trading platforms. OKB provides various
                    benefits and utilities within the OKX ecosystem, enhancing
                    the user experience and offering incentives for
                    participation. Holders of OKB can enjoy discounted trading
                    fees on the OKX exchange, access exclusive trading events,
                    and participate in token sales through the OKX Jumpstart
                    platform. OKB also plays a role in the governance of the
                    OKX Chain, a decentralized blockchain platform developed by
                    OKX. The token is burned periodically to reduce its total
                    supply, which aims to increase its scarcity and potentially
                    drive its value higher. OKB's functionalities extend beyond
                    the OKX exchange, as it can be used for various purposes,
                    including payments for services and participation in
                    ecosystem initiatives. As the OKX platform continues to
                    evolve and expand its offerings, OKB remains a central
                    component of its ecosystem, fostering growth and engagement
                    within the community.
                </p>
                <h3>OKX and Star Xu: building a global crypto powerhouse</h3>
                <p>
                    OKX was founded by Star Xu, a Chinese entrepreneur who has
                    been involved in the cryptocurrency space since its early
                    days. Star Xu is considered a visionary leader who
                    recognized the potential of digital assets and the need for
                    a reliable and innovative trading platform. Under his
                    guidance, OKX has grown from a relatively small exchange
                    into a global powerhouse, offering a wide range of trading
                    products and services, including spot trading, futures
                    trading, options trading, and margin trading. OKX has
                    consistently focused on innovation and technological
                    advancements, striving to provide users with a seamless and
                    secure trading experience. While Star Xu may not be the
                    public face of OKX as much as some other crypto CEOs, his
                    strategic vision and leadership have been crucial to the
                    exchange's success. OKX continues to expand its global
                    reach and develop new products, solidifying its position as
                    a major player in the cryptocurrency industry. The success
                    of OKB is directly tied to the growth and innovation of the
                    OKX platform under Star Xu's leadership.
                </p>""",
            volume=28_388_811_901.29
        )
    )
    session.add(
        CryptoCurrency(
            ticker="OM",
            name="MANTRA DAO",
            description="""
                <h3>MANTRA: a regulatory-compliant DeFi ecosystem</h3>
                <p>
                    MANTRA (OM) is a decentralized finance (DeFi) platform
                    focused on providing regulatory-compliant services and
                    products. It aims to bridge the gap between traditional
                    finance and the world of decentralized finance by offering
                    a secure and transparent platform for institutional and
                    retail investors alike. MANTRA Chain, its core component,
                    is a permissioned blockchain built on the Cosmos SDK,
                    designed to facilitate cross-chain interoperability and
                    enable the creation of compliant DeFi applications. The
                    platform emphasizes security and compliance with
                    regulations, offering services like staking, lending,
                    borrowing, and asset management within a framework that
                    adheres to industry standards. MANTRA's native token, OM,
                    is used for governance, staking, and incentivizing
                    participation within the ecosystem. The project aims to
                    create a DeFi environment where traditional finance
                    principles are integrated with blockchain technology,
                    fostering wider adoption and trust in the decentralized
                    space. Ultimately, MANTRA strives to build a robust and
                    sustainable ecosystem that offers secure and compliant
                    financial services for a global audience.
                </p>
                <h3>The vision of MANTRA DAO and its founders</h3>
                <p>
                    MANTRA was originally founded as MANTRA DAO, a
                    community-governed decentralized autonomous organization
                    (DAO) focused on building a secure and transparent DeFi
                    ecosystem. The project was launched by a team of
                    experienced professionals from various backgrounds,
                    including finance, technology, and regulation. The founders
                    aimed to create a platform that empowers users to
                    participate in the DeFi revolution while adhering to
                    regulatory requirements. MANTRA's focus on compliance and
                    security stems from the team's belief that these are
                    essential for the long-term sustainability and widespread
                    adoption of DeFi. The transition from MANTRA DAO to MANTRA
                    reflects the project's evolution and its commitment to
                    building a robust and scalable platform. The core team
                    continues to drive the development and expansion of the
                    MANTRA ecosystem, focusing on innovation, regulatory
                    compliance, and community engagement. Their vision is to
                    create a bridge between traditional finance and DeFi,
                    fostering a future where decentralized financial services
                    are accessible and trusted by all.
                </p>""",
            volume=28_388_811_901.29
        )
    )
    session.add(
        CryptoCurrency(
            ticker="APT",
            name="Aptos",
            description="""
                <h3>Aptos: A new blockchain built for scalability</h3>
                <p>
                    Aptos is a relatively new Layer 1 blockchain that aims to
                    address the scalability, security, and reliability
                    challenges that hinder the widespread adoption of
                    blockchain technology. Developed by Aptos Labs, founded by
                    former Meta (Facebook) employees who worked on the Diem
                    blockchain project, Aptos utilizes a novel programming
                    language called Move. This language is designed to enhance
                    security and provide a more flexible and robust framework
                    for smart contract development. Aptos also employs a
                    parallel execution engine called Block-STM, which allows
                    for the processing of multiple transactions simultaneously,
                    significantly improving transaction throughput and reducing
                    latency. The blockchain's architecture is designed to be
                    modular and upgradeable, enabling it to adapt to future
                    technological advancements and evolving user needs. Aptos
                    focuses on creating a more accessible and efficient
                    blockchain environment for developers and users, striving
                    to power the next generation of decentralized applications.
                </p>
                <h3>The Diem Legacy and Aptos Labs</h3>
                <p>
                    Aptos owes its origins to the Diem project, Facebook's
                    ambitious attempt to create a global stablecoin and
                    payments infrastructure. When the Diem project was
                    ultimately discontinued due to regulatory hurdles, a team
                    of its core developers, including Mo Shaikh and Avery
                    Ching, decided to continue their work and build a new
                    blockchain from the ground up. This led to the formation of
                    Aptos Labs and the creation of the Aptos blockchain. The
                    team leveraged their expertise and insights gained from
                    developing Diem to create a blockchain that is more secure,
                    scalable, and user-friendly. The decision to build on the
                    Move programming language, originally developed for Diem,
                    reflects the team's commitment to building a robust and
                    reliable platform. Aptos Labs has attracted significant
                    venture capital funding, demonstrating strong investor
                    confidence in its vision and potential to disrupt the
                    blockchain landscape. The project represents a continuation
                    of the Diem's vision for a more efficient and accessible
                    financial system, albeit in a more decentralized and
                    permissionless manner.
                </p>""",
            volume=28_388_811_901.29
        )
    )
    session.add(
        CryptoCurrency(
            ticker="BNB",
            name="BNB",
            description="""
                <h3>BNB: the fuel of the Binance ecosystem</h3>
                <p>
                    BNB, originally known as Binance Coin, is the native
                    cryptocurrency of the Binance exchange, one of the world's
                    largest cryptocurrency platforms. Initially launched in
                    2017 as an ERC-20 token on the Ethereum blockchain, BNB
                    later migrated to Binance's own blockchain, the Binance
                    Chain, and subsequently the Binance Smart Chain (now known
                    as the BNB Chain). BNB serves multiple purposes within the
                    Binance ecosystem. Firstly, it provides discounts on
                    trading fees for users on the Binance exchange. Secondly,
                    it can be used to pay for transaction fees on the BNB
                    Chain. Thirdly, BNB is used for staking to earn rewards and
                    participate in governance within the BNB Chain ecosystem.
                    Beyond the Binance platform, BNB can be used to pay for
                    goods and services from various merchants who accept it as
                    a form of payment. This utility has helped to drive
                    adoption and increase the overall value of the BNB token.
                </p>
                <h3>Changpeng Zhao and the rise of Binance</h3>
                <p>
                    BNB's success is intrinsically linked to the vision and
                    leadership of Changpeng Zhao (CZ), the founder and CEO of
                    Binance. CZ's background in software development and his
                    early involvement in the crypto space led him to identify a
                    gap in the market for a user-friendly and efficient
                    cryptocurrency exchange. Binance quickly gained popularity
                    due to its low fees, wide range of supported
                    cryptocurrencies, and innovative features. CZ's focus on
                    building a strong community, promoting transparency, and
                    continuously developing new products and services has been
                    instrumental in Binance's growth. Under his leadership,
                    Binance has expanded beyond just an exchange to encompass a
                    vast ecosystem of products and services, including the BNB
                    Chain, Binance Launchpad, and various DeFi platforms. CZ's
                    influence extends beyond Binance, as he is a prominent
                    figure in the crypto industry, advocating for regulatory
                    clarity and promoting the adoption of blockchain technology
                    globally.
                </p>""",
            volume=28_388_811_901.29
        )
    )
    session.add(
        CryptoCurrency(
            ticker="BGB",
            name="Bitget Token",
            description="""
                <h3>What is Bitget Token (BGB)?</h3>
                <p>
                    Bitget Token (BGB) is the native utility token of the
                    Bitget cryptocurrency exchange, a platform known for its
                    copy trading features and diverse range of digital asset
                    offerings. Launched in July 2022, BGB is designed to
                    enhance the user experience within the Bitget ecosystem and
                    provide various benefits to its holders. These benefits
                    include discounts on trading fees, access to exclusive
                    promotions and airdrops, and increased opportunities to
                    participate in platform governance. BGB holders can also
                    use their tokens to participate in the Bitget Launchpad, a
                    platform for early-stage crypto projects, and earn staking
                    rewards. The token aims to create a more engaged and loyal
                    user base by incentivizing participation and rewarding
                    users for their support of the Bitget exchange. BGB plays a
                    vital role in the Bitget ecosystem, driving engagement,
                    fostering community, and providing users with tangible
                    benefits. With a growing user base and expanding platform
                    features, BGB continues to evolve as a key component of the
                    Bitget exchange.
                </p>
                <h3>About Bitget and its expansion</h3>
                <p>
                    Bitget is a cryptocurrency exchange that was founded in
                    2018. The company has been expanding rapidly in recent
                    years, and now offers a wide range of services, including
                    spot trading, futures trading, and copy trading. Copy
                    trading is one of Bitget's most popular features, which
                    allows users to automatically copy the trades of
                    experienced traders. This can be a great way for new
                    traders to learn about the markets and make profitable
                    trades. Bitget has also been investing heavily in marketing
                    and partnerships, which has helped to increase its brand
                    awareness and attract new users. The exchange actively
                    seeks partnerships with other projects and organizations to
                    promote adoption and innovation in the crypto space.
                    Bitget's vision is to become a leading global
                    cryptocurrency exchange by providing innovative products
                    and services, fostering a strong community, and promoting
                    the widespread adoption of digital assets. The future plans
                    of Bitget include expanding into new markets and developing
                    new products and services.
                </p>""",
            volume=28_388_811_901.29
        )
    )


def _generate_id(length: int) -> str:
    symbols: str = ascii_letters + digits
    _id: str = ""

    for _ in range(length):
        _id += symbols[randint(0, 61)]
    return _id


def _add_test_prices() -> None:
    def _push_day_course(min_: float, max_: float, ticker: str):
        for hour in range(24):
            session.add(
                CryptoCourse(
                    ID=_generate_id(16),
                    ticker=ticker,
                    type_="hour",
                    number=hour,
                    price=round(uniform(min_, max_), ndigits=2)
                )
            )

    def _push_month_course(min_: float, max_: float, ticker: str):
        for day in range(1, 32):
            session.add(
                CryptoCourse(
                    ID=_generate_id(16),
                    ticker=ticker,
                    type_="day",
                    number=day,
                    price=round(uniform(min_, max_), ndigits=2)
                )
            )

    def _push_year_course(min_: float, max_: float, ticker: str):
        for month in range(1, 13):
            session.add(
                CryptoCourse(
                    ID=_generate_id(16),
                    ticker=ticker,
                    type_="month",
                    number=month*2,
                    price=round(uniform(min_, max_), ndigits=2)
                )
            )
            session.add(
                CryptoCourse(
                    ID=_generate_id(16),
                    ticker=ticker,
                    type_="month",
                    number=month*2-1,
                    price=round(uniform(min_, max_), ndigits=2)
                )
            )

    # _push_day_course(0.985, 1.015, "USDT")
    # _push_month_course(0.985, 1.015, "USDT")
    # _push_year_course(0.985, 1.015, "USDT")

    # _push_day_course(2373.0, 2963.0, "ETH")
    # _push_month_course(2173.0, 3263.0, "ETH")
    # _push_year_course(1973.0, 3463.0, "ETH")

    # _push_day_course(38928.0, 82931.0, "BTC")
    # _push_month_course(33928.0, 89931.0, "BTC")
    # _push_year_course(27928.0, 101931.0, "BTC")

    # _push_day_course(2.56, 3.42, "XRP")
    # _push_month_course(2.56, 3.42, "XRP")
    # _push_year_course(2.56, 3.42, "XRP")

    # _push_day_course(0.7, 1.41, "ADA")
    # _push_month_course(0.7, 1.41, "ADA")
    # _push_year_course(0.7, 1.41, "ADA")

    # _push_day_course(21.0, 63.0, "AVAX")
    # _push_month_course(21.0, 63.0, "AVAX")
    # _push_year_course(21.0, 63.0, "AVAX")

    # _push_day_course(0.08, 0.5, "DOGE")
    # _push_month_course(0.08, 0.5, "DOGE")
    # _push_year_course(0.08, 0.5, "DOGE")

    # _push_day_course(142.0, 264.0, "SOL")
    # _push_month_course(142.0, 264.0, "SOL")
    # _push_year_course(142.0, 264.0, "SOL")

    # _push_day_course(4.2, 8.1, "TON")
    # _push_month_course(4.2, 8.1, "TON")
    # _push_year_course(4.2, 8.1, "TON")

    # _push_day_course(0.18, 0.45, "TRX")
    # _push_month_course(0.18, 0.45, "TRX")
    # _push_year_course(0.18, 0.45, "TRX")

    # _push_day_course(4.88, 8.82, "NEAR")
    # _push_month_course(4.88, 8.82, "NEAR")
    # _push_year_course(4.88, 8.82, "NEAR")

    # _push_day_course(0.99, 1.01, "USDC")
    # _push_month_course(0.99, 1.01, "USDC")
    # _push_year_course(0.99, 1.01, "USDC")

    # _push_day_course(17.49, 29.99, "LINK")
    # _push_month_course(17.49, 29.99, "LINK")
    # _push_year_course(17.49, 29.99, "LINK")

    # _push_day_course(3.04, 5.3, "SUI")
    # _push_month_course(3.04, 5.3, "SUI")
    # _push_year_course(3.04, 5.3, "SUI")

    # _push_day_course(0.03, 0.54, "XLM")
    # _push_month_course(0.03, 0.54, "XLM")
    # _push_year_course(0.03, 0.54, "XLM")

    # _push_day_course(5.75, 11.46, "DOT")
    # _push_month_course(5.75, 11.46, "DOT")
    # _push_year_course(5.75, 11.46, "DOT")

    # _push_day_course(76.02, 140.86, "LTC")
    # _push_month_course(76.02, 140.86, "LTC")
    # _push_year_course(76.02, 140.86, "LTC")

    # _push_day_course(8.36, 18.31, "UNI")
    # _push_month_course(8.36, 18.31, "UNI")
    # _push_year_course(8.36, 18.31, "UNI")

    # _push_day_course(178.18, 379.79, "AAVE")
    # _push_month_course(178.18, 379.79, "AAVE")
    # _push_year_course(178.18, 379.79, "AAVE")

    # _push_day_course(124.84, 230.97, "XMR")
    # _push_month_course(124.84, 230.97, "XMR")
    # _push_year_course(124.84, 230.97, "XMR")

    _push_day_course(0.03, 0.54, "OKB")
    # _push_month_course(0.03, 0.54, "OKB")
    # _push_year_course(0.03, 0.54, "OKB")

    _push_day_course(5.75, 11.46, "OM")
    # _push_month_course(5.75, 11.46, "OM")
    # _push_year_course(5.75, 11.46, "OM")

    _push_day_course(76.02, 140.86, "APT")
    # _push_month_course(76.02, 140.86, "APT")
    # _push_year_course(76.02, 140.86, "APT")

    _push_day_course(8.36, 18.31, "BNB")
    # _push_month_course(8.36, 18.31, "BNB")
    # _push_year_course(8.36, 18.31, "BNB")

    _push_day_course(178.18, 379.79, "BGB")
    # _push_month_course(178.18, 379.79, "BGB")
    # _push_year_course(178.18, 379.79, "BGB")


def _push_data_from_csv(tickers: list[str], session: Session) -> None:
    counter: int = 0

    year_dates: list[str] = ["01/01/2025", "01/15/2025", "02/01/2025"]
    year_dates.extend([
        f"{str(i // 2).zfill(2)}/{'01' if i % 2 == 0 else '15'}/2024"
        for i in range(5, 26)
    ])

    for ticker in tickers:
        offset: int = 1 if len(year_dates) % 2 == 0 else 0
        with open(f"../crypto_prices_data/{ticker}.csv") as file:
            reader: csv.reader = csv.reader(file)
            for row in reader:
                if row[0] in year_dates:
                    # print(
                    #     ticker,
                    #     row[0],
                    #     float(row[1]),
                    #     int(row[0].split("/")[0]) * 2 - offset,
                    #     "month"
                    # )
                    session.add(
                        CryptoCourse(
                            ID=_generate_id(16),
                            ticker=ticker,
                            price=round(
                                float(row[1].replace(",", "")),
                                ndigits=2
                            ),
                            type_="month",
                            number=int(row[0].split("/")[0]) * 2 - offset
                        )
                    )
                    offset = 0 if offset else 1
                    counter += 1

    month_dates: list[str] = []
    month_dates.extend([f"01/{str(i).zfill(2)}/2025" for i in range(9, 32)])
    month_dates.extend([
        "02/01/2025",
        "02/02/2025",
        "02/03/2025",
        "02/04/2025",
        "02/05/2025",
        "02/06/2025",
        "02/07/2025",
        "02/08/2025",
    ])

    print()
    for ticker in tickers:
        with open(f"../crypto_prices_data/{ticker}.csv") as file:
            reader: csv.reader = csv.reader(file)
            for row in reader:
                if row[0] in month_dates:
                    # print(
                    #     ticker,
                    #     row[0],
                    #     float(row[1]),
                    #     int(row[0].split("/")[1]),
                    #     "day"
                    # )
                    session.add(
                        CryptoCourse(
                            ID=_generate_id(16),
                            ticker=ticker,
                            price=round(
                                float(row[1].replace(",", "")),
                                ndigits=2
                            ),
                            type_="day",
                            number=int(row[0].split("/")[1])
                        )
                    )
                    counter += 1

    print(counter)


tickers: list[str] = [
    # "USDT",
    # "BTC",
    # "ETH",
    # "SOL",
    # "TRX",
    # "TON",
    # "DOGE",
    # "AVAX",
    # "ADA",
    # "XRP",
    # "NEAR",
    # "AAVE",
    # "DOT",
    # "LINK",
    # "LTC",
    # "SUI",
    # "UNI",
    # "USDC",
    # "XLM",
    # "XMR",
    "OKB",
    "OM",
    "APT",
    "BNB",
    "BGB",
]


if __name__ == "__main__":
    with Session(engine) as session:
        metadata.create_all(bind=engine)

        # _add_fiat_currencies()
        # _add_cryptocurrencies()
        # _add_test_prices()
        _push_data_from_csv(tickers, session)

        session.commit()
        print("Data pushed successfully.")
