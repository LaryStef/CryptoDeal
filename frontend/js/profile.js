import {
    Chart,
    DoughnutController,
    ArcElement
} from "chart.js";

const origin = location.origin;
const refreshTokensUrl = new URL("api/auth/refresh-tokens", origin);
const profileDataUrl = new URL("api/user", origin);
const sessionUrl = new URL("api/sessions", origin);
const cryptoStatisticsUrl = new URL("api/user/statistics/cryptocurrency", origin);

const textHoverColor = "#8935a2";
const contrastColor = "#8FFF06";

class BalanceUrl {
    constructor(origin, type, ids) {
        let urlConstructor = new URL(`api/user/balance/${type}/ids`, origin);
        for (let id of ids) {
            urlConstructor.searchParams.append("id", id);
        }

        this.url = urlConstructor;
    }

    get() {
        return this.url;
    }
}

function convertNumberForUser(number) {
    if (number > 1_000_000_000) return (Math.round(number / 10_000_000) / 100).toString() + "B";
    if (number > 1_000_000) return (Math.round(number / 10_000) / 100).toString() + "M";
    if (number > 1000) return (Math.round(number / 10) / 100).toString() + "K";
    return (Math.round(number * 100) / 100).toString();
}

function loadChart(doughnutData, walletWorth) {
    Chart.register(
        DoughnutController,
        ArcElement
    );
    Chart.register({
    	id: 'doughnut-centertext',
        beforeDraw: function(chart) {
            if (chart.config.options.elements.center) {
                const ctx = chart.ctx;

                const centerConfig = chart.config.options.elements.center;
                const fontStyle = centerConfig.fontStyle || 'Arial';
                const txt = centerConfig.text;
                const color = centerConfig.color || '#000';
                const maxFontSize = centerConfig.maxFontSize || 75;
                const sidePadding = centerConfig.sidePadding || 20;
                const sidePaddingCalculated = (sidePadding / 100) * (chart._metasets[chart._metasets.length-1].data[0].innerRadius * 2)
                ctx.font = "30px " + fontStyle;

                const stringWidth = ctx.measureText(txt).width;
                const elementWidth = (chart._metasets[chart._metasets.length-1].data[0].innerRadius * 2) - sidePaddingCalculated;            

                const widthRatio = elementWidth / stringWidth;
                const newFontSize = Math.floor(30 * widthRatio);
                const elementHeight = (chart._metasets[chart._metasets.length-1].data[0].innerRadius * 2);

                let fontSizeToUse = Math.min(newFontSize, elementHeight, maxFontSize);
                let minFontSize = centerConfig.minFontSize;
                const lineHeight = centerConfig.lineHeight || 25;
                let wrapText = false;

                if (minFontSize === undefined) {
                    minFontSize = 20;
                }

                if (minFontSize && fontSizeToUse < minFontSize) {
                    fontSizeToUse = minFontSize;
                    wrapText = true;
                }

                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                const centerX = ((chart.chartArea.left + chart.chartArea.right) / 2);
                let centerY = ((chart.chartArea.top + chart.chartArea.bottom) / 2);
                ctx.font = fontSizeToUse + "px " + fontStyle;
                ctx.fillStyle = color;

                if (!wrapText) {
                    ctx.fillText(txt, centerX, centerY);
                    return;
                }

                const words = txt.split(' ');
                let line = '';
                let lines = [];

                for (let n = 0; n < words.length; n++) {
                    const testLine = line + words[n] + ' ';
                    const metrics = ctx.measureText(testLine);
                    const testWidth = metrics.width;
                    if (testWidth > elementWidth && n > 0) {
                        lines.push(line);
                        line = words[n] + ' ';
                    } else {
                        line = testLine;
                    }
                }

                centerY -= (lines.length / 2) * lineHeight;

                for (let n = 0; n < lines.length; n++) {
                    ctx.fillText(lines[n], centerX, centerY);
                    centerY += lineHeight;
                }
                ctx.fillText(line, centerX, centerY);
            }
        }
    });
    Chart.defaults.font.family = "Ubuntu Mono";

    const config = {
        type: 'doughnut',
        data: doughnutData,
        options: {
            layout: {
                padding: 10,
            },
            plugins: {
                legend: {
                    position: 'bottom',
                }
            },
            responsive: true,
            maintainAspectRatio: false,
            elements: {
                center: {
                    text: walletWorth,
                    color: contrastColor,
                    fontStyle: 'Arial',
                    sidePadding: 40,
                    minFontSize: 15,
                    maxFontSize: 20,
                    lineHeight: 15,
                },
                arc: {
                    backgroundColor: textHoverColor,
                }
            }
        }
    };
    return new Chart(document.getElementById("doughnut").getContext('2d'), config);
}

function loadCryptoStatistics(data) {
    document.getElementById("spent-value").innerText = convertNumberForUser(data["spent"]) + "$";
    document.getElementById("derived-value").innerText = convertNumberForUser(data["derived"]) + "$";
    let cryptocurrencies = data["cryptocurrencies"].sort((a, b) => b.amount * b.price - a.amount * a.price);
    const walletWorth = convertNumberForUser(
        cryptocurrencies.reduce((acc, cryptocurrency) => acc + cryptocurrency.amount * cryptocurrency.price, 0)
    );
    document.getElementById("worth-value").innerText = walletWorth + "$";
    if (Math.round(data["change"] * 100) / 100 >= 0) {
        document.getElementById("worth-change").innerText = "+" + Math.round(data["change"] * 100) / 100 + "%";
        document.getElementById("worth-change").classList.add("change-pos");
    } else {
        document.getElementById("worth-change").innerText = Math.round(data["change"] * 100) / 100 + "%";
        document.getElementById("worth-change").classList.add("change-neg");
    }

    if (cryptocurrencies.length == 0) {
        document.getElementById("st-block-1").innerHTML = `
            <div class="crypto-block-header">
                <h3 style="font-size: 1.5rem">Cryptocurrency statistics not availible (Buy any cryptocurrency to see statistics)</h3>
            </div>`
        return;
    }
    loadCrytoTable(cryptocurrencies);
    loadChart(formDoughnutData(cryptocurrencies), walletWorth);
}

function formDoughnutData(cryptocurrencies) {
    const colors = [
        "#f4e500",
        "#f18e1c",
        "#e32322",
        "#6d398b",
        "#2a71b0",
        "#008e5b",
    ];

    const legend = document.getElementById("legend-list");
    let doughnutData = []
    for (let i = 0; i < cryptocurrencies.length ; i++) {
        if (i == 5) {
            legend.innerHTML += `<li class="legend-el" id="legend-${i + 1}">
                <div class="color-rect" style="background-color: ${colors[i]};"></div>
                <span>Other</span></li>`
            doughnutData[i] = 0;
            for (let j = i; j < cryptocurrencies.length; j++) {
                doughnutData[i] += cryptocurrencies[j].amount * cryptocurrencies[j].price;
            }
            break;
        }
        doughnutData.push(cryptocurrencies[i].amount * cryptocurrencies[i].price);
        legend.innerHTML += `<li class="legend-el" id="legend-${i+1}">
            <div class="color-rect" style="background-color: ${colors[i]};"></div>
            <span>${cryptocurrencies[i].name}</span><img class="legend-img" src="${cryptocurrencies[i].logoUrl}" alt=""></li>`
    }

    return {
        datasets: [{
            data: doughnutData,
            backgroundColor: colors.slice(0, cryptocurrencies.length),
            hoverOffset: 20,
        }]
    }
}

function loadCrytoTable(cryptocurrencies) {
    let table = document.getElementById("crypto-list");
    for (let i = 0; i < cryptocurrencies.length; i++) {
        let profitCell = "";
        if (cryptocurrencies[i].profit >= 0) {
            profitCell = `<td class="tc change-pos">+${Math.round(cryptocurrencies[i].profit * 100) / 100}%</td>`;
        } else {
            profitCell = `<td class="tc change-neg">${Math.round(cryptocurrencies[i].profit * 100) / 100}%</td>`;
        }
        let changeCell = "";
        if (cryptocurrencies[i].change >= 0) {
            changeCell = `<td class="tc change-pos">+${Math.round(cryptocurrencies[i].change * 100) / 100}%</td>`;
        } else {
            changeCell = `<td class="tc change-neg">${Math.round(cryptocurrencies[i].change * 100) / 100}%</td>`;
        }
        table.innerHTML += `
                <tr class="row">
                <td class="tc">${i+1}</td>
                <td class="tc">
                    <div class="crypto-name-wrap">
                        <img class="crypto-logo" src="${cryptocurrencies[i].logoUrl}" alt="">
                        <span class="crypto-name">${cryptocurrencies[i].name}</span>
                    </div>
                </td>
                <td class="tc">${cryptocurrencies[i].ticker}</td>
                <td class="tc">${convertNumberForUser(cryptocurrencies[i].price)}</td>
                <td class="tc">${Math.round(cryptocurrencies[i].amount * 1000) / 1000}</td>
                <td class="tc">${convertNumberForUser(cryptocurrencies[i].amount * cryptocurrencies[i].price)}</td>
                ${profitCell}
                ${changeCell}
            </tr>`;
    }
}

function getDeviceData() {
    let browser = "unknown browser";
    let os = "unknown os";
    let osVersion = "";

    let userAgent = navigator.userAgent;

    if (userAgent.indexOf("Edg") > -1) {
        browser = "Microsoft Edge";
    } else if (userAgent.indexOf("Chrome") > -1) {
        browser = "Chrome";
    } else if (userAgent.indexOf("Firefox") > -1) {
        browser = "Firefox";
    } else if (userAgent.indexOf("Safari") > -1) {
        browser = "Safari";
    } else if (userAgent.indexOf("Opera") > -1) {
        browser = "Opera";
    } else if (
        userAgent.indexOf("Trident") > -1 ||
        userAgent.indexOf("MSIE") > -1
    ) {
        browser = "Internet Explorer";
    }

    const clientStrings = [
        {s: "Windows 10", r: /(Windows 10.0|Windows NT 10.0)/},
        {s: "Windows 8.1", r: /(Windows 8.1|Windows NT 6.3)/},
        {s: "Windows 8", r: /(Windows 8|Windows NT 6.2)/},
        {s: "Windows 7", r: /(Windows 7|Windows NT 6.1)/},
        {s: "Windows Vista", r: /Windows NT 6.0/},
        {s: "Windows Server 2003", r: /Windows NT 5.2/},
        {s: "Windows XP", r: /(Windows NT 5.1|Windows XP)/},
        {s: "Windows 2000", r: /(Windows NT 5.0|Windows 2000)/},
        {s: "Windows ME", r: /(Win 9x 4.90|Windows ME)/},
        {s: "Windows 98", r: /(Windows 98|Win98)/},
        {s: "Windows 95", r: /(Windows 95|Win95|Windows_95)/},
        {s: "Windows NT 4.0", r: /(Windows NT 4.0|WinNT4.0|WinNT|Windows NT)/},
        {s: "Windows CE", r: /Windows CE/},
        {s: "Windows 3.11", r: /Win16/},
        {s: "Android", r: /Android/},
        {s: "Open BSD", r: /OpenBSD/},
        {s: "Sun OS", r: /SunOS/},
        {s: "Chrome OS", r: /CrOS/},
        {s: "Linux", r: /(Linux|X11(?!.*CrOS))/},
        {s: "iOS", r: /(iPhone|iPad|iPod)/},
        {s: "Mac OS X", r: /Mac OS X/},
        {s: "Mac OS", r: /(Mac OS|MacPPC|MacIntel|Mac_PowerPC|Macintosh)/},
        {s: "QNX", r: /QNX/},
        {s: "UNIX", r: /UNIX/},
        {s: "BeOS", r: /BeOS/},
        {s: "OS/2", r: /OS\/2/},
        {
            s: "Search Bot",
            r: /(nuhk|Googlebot|Yammybot|Openbot|Slurp|MSNBot|Ask Jeeves\/Teoma|ia_archiver)/,
        },
    ];
    for (let id in clientStrings) {
        let cs = clientStrings[id];
        if (cs.r.test(userAgent)) {
            os = cs.s;
            break;
        }
    }

    if (/Windows/.test(os)) {
        osVersion = /Windows (.*)/.exec(os)[1];
        os = "Windows";
    }

    switch (os) {
        case "Mac OS":
        case "Mac OS X":
        case "Android":
            osVersion = /(?:Android|Mac OS|Mac OS X|MacPPC|MacIntel|Mac_PowerPC|Macintosh) ([\.\_\d]+)/.exec(userAgent)[1];
            break;

        case "iOS":
            osVersion = /OS (\d+)_(\d+)_?(\d+)?/.exec(nVer);
            osVersion = osVersion[1] + "." + osVersion[2] + "." + (osVersion[3] | 0);
            break;
    }

    return browser + ", " + os + osVersion;
}

if (isTokensRefreshRequired()) {
    refreshTokens();
} else {
    loadProfile();
}

async function refreshTokens() {
    let response = await fetch(refreshTokensUrl, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-SCRF-TOKEN": getCookie("refresh_scrf_token"),
            Device: getDeviceData(),
        },
    });

    if (response.status === 200) {
        loadProfile();
    }
}

function isTokensRefreshRequired() {
    let access = getCookie("access_token");

    if (
        access != "" &&
        Math.floor(Date.now() / 1000) < Number(JSON.parse(atob(access.split(".")[1])).exp) - 1
    ) {
        return false;
    }
    return true;
}

function getCookie(cookie) {
    cookie += "=";
    let cookies = document.cookie.split("; ");
    let token = "";

    cookies.forEach((element) => {
        if (element.substring(0, cookie.length) === cookie) {
            token = element.substring(cookie.length, element.length);
        }
    });
    return token;
}

function loadProfile() {
    loadSessions();

    let authClasses = document.getElementById("auth-button").classList;
    let profileClasses = document.getElementById("profile-button").classList;
    authClasses.add("display-off");
    profileClasses.remove("display-off");
    loadMainInfo();
}

function loadMainInfo() {
    let access = getCookie("access_token");
    let payload = JSON.parse(atob(access.split(".")[1]));

    document.getElementById("name").innerText = payload.name;
    document.getElementById("username").innerText = payload.name;

    const avatarUrl = new URL(
        `/static/png/Alien${payload.alien_number}.png`,
        location.origin
    );
    document.getElementById("avatar").src = avatarUrl;
    document.getElementById("main-avatar").src = avatarUrl;

    const balanceUrl = new BalanceUrl(origin, "currency", ["USD"]);
    fetch(balanceUrl.get(), {
        method: "GET",
        credentials: "same-origin",
        headers: {
            "X-SCRF-TOKEN": getCookie("access_scrf_token"),
        },
    })
        .then((response) => response.json())
        .then((data) => {
            const balance = data["balance"]["USD"];
            document.getElementById("usd-balance").innerText = "Balance: " + convertNumberForUser(balance) + "$";
        })
    
    fetch(cryptoStatisticsUrl, {
        method: "GET",
        credentials: "same-origin",
        headers: {
            "X-SCRF-TOKEN": getCookie("access_scrf_token"),
        },
    })
        .then((response) => response.json())
        .then((data) => loadCryptoStatistics(data));
}

function loadSessions(clearFirst = false) {
    fetch(profileDataUrl, {
        method: "GET",
        credentials: "same-origin",
        headers: {
            "X-SCRF-TOKEN": getCookie("access_scrf_token"),
        },
    })
        .then((response) => response.json())
        .then((data) => {
            const sessions = data.userData.sessions;

            let table = document.getElementById("ses-table");

            if (clearFirst) {
                table.innerHTML = `
                    <caption>Manage your sessions</caption>
                    <tr>
                        <th class="session-head-sell">Device</th>
                        <th class="session-head-sell">Last activity(UTC)</th>
                        <th class="session-head-sell">
                            <button class="term-all" id="term-all">terminate all</button>
                        </th>
                    </tr>`
            }

            let sessionNum = 0;
            sessions.forEach((session) => {
                if (session.isCurrent) {
                    document.getElementById("logout-btn").setAttribute("sessionId", session.sessionId);

                    table.innerHTML += `<tr class="row">
                        <td class="session-cell">${session.device}</td>
                        <td class="session-cell">${session.lastActivity}</td>
                        <td class="session-cell cur-ses">current</td>
                    </tr>`;
                } else {
                    sessionNum += 1;
                    if (sessionNum >= 9) {
                        return;
                    }
                    table.innerHTML += `<tr class="row">
                        <td class="session-cell">${session.device}</td>
                        <td class="session-cell">${session.lastActivity}</td>
                        <td class="session-cell">
                            <button class="term-btn" sessionId=${session.sessionId}>terminate</button>
                        </td>
                    </tr>`;
                }
            });
        });
}

document.getElementById("set-btn").onclick = openSettingsWindow;
document.getElementById("cancel-set").onclick = closeSettingsWindow;

document.getElementById("ses-table").addEventListener("click", (event) => {
    if (isTokensRefreshRequired()) {
        refreshTokens();
    }
    if (event.target.classList.contains("term-btn")) {
        
        let sessionId = event.target.attributes.sessionid.value;

        fetch(sessionUrl + "/" + sessionId, {
            method: "DELETE",
            credentials: "same-origin",
            headers: {
                "X-SCRF-TOKEN": getCookie("access_scrf_token"),
            },
        }).then((response) => {
            if (response.status === 200) {
                loadSessions(true);
            }
        });
    } else if (event.target.classList.contains("term-all")) {
        
        fetch(sessionUrl + "/all", {
            method: "DELETE",
            credentials: "same-origin",
            headers: {
                "X-SCRF-TOKEN": getCookie("access_scrf_token"),
            },
        }).then((response) => {
            if (response.status === 200) {
                loadSessions(true);
            }
        });
    }
});

document.getElementById("logout-btn").addEventListener("click", () => {
    if (isTokensRefreshRequired()) {
        refreshTokens();
    }

    fetch(sessionUrl + "/my", {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
            "X-SCRF-TOKEN": getCookie("access_scrf_token"),
        },
    }).then((response) => {
        if (response.status === 200) {
            window.location.replace(origin);
        }
    });
});

document.onkeydown = function (evt) {
    let isEscape = false;
    if ("key" in evt) {
        isEscape = evt.key === "Escape" || evt.key === "Esc";
    } else {
        isEscape = evt.keyCode === 27;
    }
    if (isEscape) {
        closeSettingsWindow();
    }
};

function openSettingsWindow() {
    let window = document.getElementById("set-win");
    window.style.left = "50%";
    document.getElementById("main").style.filter = "brightness(0.5)";
    document.getElementById("navbar").style.filter = "brightness(0.5)";
}

function closeSettingsWindow() {
    let window = document.getElementById("set-win");
    window.style.left = "-50%";
    document.getElementById("main").style.filter = "brightness(1)";
    document.getElementById("navbar").style.filter = "brightness(1)";
}
