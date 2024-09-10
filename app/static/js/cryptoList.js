import "./navbar.js";

const tableDataUrl = new URL("api/crypto/list", origin);

loadCryptoTable();

function loadCryptoTable() {
    fetch(tableDataUrl, {
        method: "GET",
        credentials: "same-origin"
    })
        .then((response) => response.json())
        .then((data) => {
            const currencyList = data.CryptoCurrencyList;
            const table = document.getElementById("crypto-list");
            
            let num = 1;
            currencyList.forEach((currency) => {
                let volume;
                if (currency.volume > 1_000_000_000) {
                    volume = (Math.round(currency.volume / 1_000_000) / 1000).toString() + "B"
                } else {
                    volume = (Math.round(currency.volume / 1000) / 1000).toString() + "M"
                }
                
                let change;
                let changeClass;
                if (currency.change >= 0) {
                    change = "+" + (Math.round(currency.change * 1000) / 1000) + "%";
                    changeClass = "change-pos";
                } else {
                    change = (Math.round(currency.change * 1000) / 1000) + "%";
                    changeClass = "change-neg";
                }

                table.innerHTML += `        
                    <tr class="row">
                        <td class="tc col1">${num}</td>
                        <td class="tc col2">
                            <div class="crypto-name-wrap">
                                <img class="crypto-logo" src="${currency.logo_url}" alt="">
                                <span class="crypto-name">${currency.name}</span>
                            </div>
                        </td>
                        <td class="tc col3">${currency.ticker}</td>
                        <td class="tc col4">${Math.round(currency.price * 1000) / 1000}</td>
                        <td class="tc col5 ${changeClass}">${change}</td>
                        <td class="tc col6">${volume}</td>
                        <td class="tc col7">
                            <a class="buy-link" href="#">
                                <div class="buy-btn">
                                    <span>Buy/Sell</span>
                                </div>
                            </a>
                        </td>
                    </tr>`
                    num += 1;
            })
        })
}